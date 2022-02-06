from distutils.sysconfig import PREFIX
from tensorflow import keras
import os

FILTERS = 32
DROPOUT = 0.3
EPOCHS = 100
BATCH_SIZE = 2048


METRICS = [
    keras.metrics.TruePositives(name="tp"),
    keras.metrics.FalsePositives(name="fp"),
    keras.metrics.TrueNegatives(name="tn"),
    keras.metrics.FalseNegatives(name="fn"),
    keras.metrics.BinaryAccuracy(name="accuracy"),
    keras.metrics.Precision(name="precision"),
    keras.metrics.Recall(name="recall"),
    keras.metrics.AUC(name="auc"),
    keras.metrics.AUC(name="prc", curve="PR"),  # precision-recall curve
]

STACK = {
    "PhG1": os.path.join(
        "/home/pegah/ideas-packages/fog-forecast/Data/NAM/npz/{prog}HOURS/INPUT",
        "NETCDF_NAM_CUBE" + "_{year}_" + "PhG1" + "_{prog}",
    ),
    "PhG2": os.path.join(
        "/home/pegah/ideas-packages/fog-forecast/Data/NAM/npz/{prog}HOURS/INPUT",
        "NETCDF_NAM_CUBE" + "_{year}_" + "PhG2" + "_{prog}",
    ),
    "PhG3": os.path.join(
        "/home/pegah/ideas-packages/fog-forecast/Data/NAM/npz/{prog}HOURS/INPUT",
        "NETCDF_NAM_CUBE" + "_{year}_" + "PhG3" + "_{prog}",
    ),
    "PhG4": os.path.join(
        "/home/pegah/ideas-packages/fog-forecast/Data/NAM/npz/{prog}HOURS/INPUT",
        "NETCDF_NAM_CUBE" + "_{year}_" + "PhG4" + "_{prog}",
    ),
}

TARGET = os.path.join(
    "/home/pegah/ideas-packages/fog-forecast/Data/NAM/npz/{prog}HOURS/TARGET",
    "target" + "{year}_" + "_{prog}",
)


YEARS = {
    "training": [
        "2009",
        "2010",
        "2011",
        "2012",
        "2013",
        "2014",
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2020",
    ],
    "validating": [
        "2009",
        "2010",
        "2011",
        "2012",
        "2013",
        "2014",
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2020",
    ],
    "testing": [
        "2009",
        "2010",
        "2011",
        "2012",
        "2013",
        "2014",
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2020",
    ],
}

PROG = 24
