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
        "NETCDF_NAM_CUBE" + "_{year}_" + "PhG1" + "_{prog}.npz",
    ),
    "PhG2": os.path.join(
        "/home/pegah/ideas-packages/fog-forecast/Data/NAM/npz/{prog}HOURS/INPUT",
        "NETCDF_NAM_CUBE" + "_{year}_" + "PhG2" + "_{prog}.npz",
    ),
    "PhG3": os.path.join(
        "/home/pegah/ideas-packages/fog-forecast/Data/NAM/npz/{prog}HOURS/INPUT",
        "NETCDF_NAM_CUBE" + "_{year}_" + "PhG3" + "_{prog}.npz",
    ),
    "PhG4": os.path.join(
        "/home/pegah/ideas-packages/fog-forecast/Data/NAM/npz/{prog}HOURS/INPUT",
        "NETCDF_NAM_CUBE" + "_{year}_" + "PhG4" + "_{prog}.npz",
    ),
}

TARGET = os.path.join(
    "/home/pegah/ideas-packages/fog-forecast/Data/NAM/npz/{prog}HOURS/TARGET",
    "target" + "{year}_" + "{prog}.csv",
)


YEARS = {
    "training": ["2018"],
    "validating": ["2019"],
    "testing": ["2020"],
}

PROG = 24

PRIORITY_CLASS = 4
