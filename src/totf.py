from asyncio.log import logger
import numpy as np
import tensorflow as tf
import pandas as pd
import logging
import json
from params import SRCFILES, TARGETFILES, DESTFILES, YEARS, PROG, PRIORITY_CLASS


logger = logging.getLogger("example_logger")


def labels(target, year, prog, priority_class):
    label_year = pd.read_csv(target.format(year=year, prog=prog), header=0, sep=",")
    label_year = label_year["VIS_Cat"]
    label_year[label_year != priority_class] = "Y"
    label_year[label_year == priority_class] = "N"
    label_year[label_year != "Y"] = 0
    label_year[label_year == "Y"] = 1
    return label_year.to_numpy()


def stack_ntiers(srcfile_stack, year, prog):
    preds_stack = []
    stack_shape = {}
    for srcfile in srcfile_stack:
        preds = np.load(
            srcfile["path"].format(prog=prog, year=year),
            mmap_mode=None,
            allow_pickle=False,
            fix_imports=True,
            encoding="ASCII",
        )["arr_0"]
        preds = np.expand_dims(preds, axis=-1)
        preds_stack.append(preds)
        stack_shape.update({srcfile["name"]: preds.shape[1:]})
    return preds_stack, stack_shape


def save_tfrecords(
    srcfile_stack, srcfile_targets, years, prog, priority_class, desfile, choice
):
    desfile = desfile.format(prog=prog)
    with tf.io.TFRecordWriter(desfile) as writer:
        for year in years[choice]:
            preds_stack, stack_shape = stack_ntiers(srcfile_stack, year, prog)
            label_year = labels(srcfile_targets, year, prog, priority_class)
            for sample in range(preds_stack[0].shape[0]):
                values = []
                for preds in preds_stack:
                    values.append(preds[sample].astype(np.float64).tobytes())
                features = tf.train.Features(
                    feature={
                        "data": tf.train.Feature(
                            bytes_list=tf.train.BytesList(value=values)
                        ),
                        "label": tf.train.Feature(
                            int64_list=tf.train.Int64List(value=[label_year[sample]])
                        ),
                    }
                )
                example = tf.train.Example(features=features)
                serialized = example.SerializeToString()
                writer.write(serialized)
    return stack_shape


def main():
    if __name__ == "__main__":
        for choice in ["training", "validating", "testing"]:
            stack_shape = save_tfrecords(
                SRCFILES, TARGETFILES, YEARS, PROG, PRIORITY_CLASS, DESTFILES, choice
            )
            with open("params/preds.json", "w") as fp:
                json.dump(stack_shape, fp, sort_keys=True, indent=4)


main()
