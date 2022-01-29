import os
import xarray as xr
import tensorflow as tf
import tempfile
import numpy as np
import argparse
import logging
import apache_beam as beam
import sys
import shutil
from datetime import datetime, timedelta
from NAM import VARIABLES


def _array_feature(value, min_value=None, max_value=None):
    if isinstance(value, type(tf.constant(0))):  # if value is tensor
        value = value.numpy()  # get value of tensor
    """Wrapper for inserting ndarray float features into Example proto."""
    value = np.nan_to_num(value.flatten())  # nan, -inf, +inf to numbers
    if None not in (min_value, max_value):
        value = np.clip(value, min_value, max_value)  # clip to valid
    logging.info("Range of image values {} to {}".format(np.min(value), np.max(value)))
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))


def _bytes_feature(value):
    """Returns a bytes_list from a string / byte."""
    if isinstance(value, type(tf.constant(0))):
        value = value.numpy()  # BytesList won't unpack a string from an EagerTensor.
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def _string_feature(value):
    return _bytes_feature(value.encode("utf-8"))


def generate_filenames_variables(basetime: str, prog: int, vars):
    for var in vars:
        dt = datetime.strptime(basetime, "%Y%m%d%H")
        no_hour = dt.strftime("%Y%m%d")
        logging.info(
            "Hourly records from basetime: {} and prognosis: {} ".format(dt, prog)
        )
        # NAM/gribs/nam_218_20200601_0000_000_TMP_2_m_above_ground.grib2
        f = "NAM/gribs/nam_218_{}_{:04d}_{:03d}_{}.gri2".format(
            no_hour, dt.hour, prog, var
        )
        yield f


def generate_basetimes_progs(
    startdate: str, enddate: str, basetime_hour: int, progs: int
):
    start_dt = datetime.strptime(startdate, "%Y%m%d")
    end_dt = datetime.strptime(enddate, "%Y%m%d")
    logging.info(
        "Basetimes from {} to {} for basetime hour {}".format(
            start_dt, end_dt, basetime_hour
        )
    )
    dt = start_dt + timedelta(hours=basetime_hour)
    while dt < end_dt:
        # print(dt)
        for prog in range(progs):
            f = [dt.strftime("%Y%m%d%H"), prog]
            yield f
        dt = dt + timedelta(days=1)


def generate_shuffled_basetimes_progs(
    startdate: str, enddate: str, basetime_hour: int, progs: int
):
    """
    shuffle the files so that a batch of records doesn't contain highly correlated entries
    """
    basetimes_progs = [
        f for f in generate_basetimes_progs(startdate, enddate, basetime_hour, progs)
    ]
    np.random.shuffle(basetimes_progs)
    return basetimes_progs


def create_tfrecord(basetime_prog: tuple, vars: list):
    basetime = basetime_prog[0]
    prog = basetime_prog[-1]
    filenames = generate_filenames_variables(basetime, prog, vars)
    channels = len(vars)
    try:
        feature = {}
        for filename in filenames:
            with tempfile.TemporaryDirectory() as tmpdirname:
                TMPFILE = "{}/read_grib".format(tmpdirname)
                tf.io.gfile.copy(filename, TMPFILE, overwrite=True)
                ds = xr.open_dataset(
                    TMPFILE, engine="cfgrib", backend_kwargs={"indexpath": ""}
                )
                variables = list(ds.keys())
                for variable in variables:
                    data_var = ds.data_vars[variable]
                    feature.update({variable: _array_feature(data_var.data)})
                    size = np.array(
                        [
                            ds.data_vars[variable].sizes["y"],
                            ds.data_vars[variable].sizes["x"],
                            channels,
                        ]
                    )
                    basetime = _string_feature(str(data_var.time.data))
                    validtime = _string_feature(str(data_var.valid_time.data))
                feature.update(
                    {
                        "size": tf.train.Feature(
                            int64_list=tf.train.Int64List(value=size)
                        ),
                        "basetime": basetime,
                        "validtime": validtime,
                    }
                )
        # create a TF Record with the raw data
        tfexample = tf.train.Example(features=tf.train.Features(feature=feature))
        yield tfexample.SerializeToString()
    except:
        e = sys.exc_info()[0]
        logging.error(e)


def run_job(options):
    # start the pipeline
    opts = beam.pipeline.PipelineOptions(flags=[], **options)
    with beam.Pipeline(options["runner"], options=opts) as p:
        # create examples
        examples = (
            p
            | ""
            >> beam.Create(
                generate_shuffled_basetimes_progs(
                    options["startdate"],
                    options["enddate"],
                    options["basetime_hour"],
                    options["progs"],
                )
            )
            | "create_tfr"
            >> beam.FlatMap(lambda x: create_tfrecord(x, options["variables"]))
        )
        # write out tfrecords
        _ = examples | "write_tfr" >> beam.io.tfrecordio.WriteToTFRecord(
            os.path.join(options["outdir"], "tfrecord")
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create TF Records from NAM files")

    parser.add_argument(
        "--project", default="", help="Specify AWS project to run on cloud"
    )

    parser.add_argument(
        "--outdir", required=True, help="output dir. could be local or on AWS"
    )

    parser.add_argument("--startdate", typ=str, required=True, help="eg 20200915")
    parser.add_argument(
        "--enddate", type=str, required=True, help="eg 20200916 -- this is exclusive"
    )
    parser.add_argument(
        "--basetime-hour", type=int, required=True, help="eg 0, 6, 12, 18"
    )
    parser.add_argument(
        "--progs", type=int, required=True, help="eg 30 hours of prognoses"
    )

    # parse command-line args and add a few more
    logging.basicConfig(level=getattr(logging, "INFO", None))
    options = parser.parse_args().__dict__
    options["variables"] = VARIABLES
    outdir = options["outdir"]

    if not options["project"]:
        print("Launching local job ... hang on")
        shutil.rmtree(outdir, ignore_errors=True)
        os.makedirs(outdir)
        options["runner"] = "DirectRunner"
    else:
        pass

    run_job(options)
