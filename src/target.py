import numpy as np
import pandas as pd
from tensorflow.keras.utils import to_categorical


def labels(target, years, prog):
    frames = []
    for year in years:
        year_data = pd.read_csv(target.format(year=year, prog=prog), header=0, sep=",")
        year_data = year_data["VIS_Cat"]
        frames.append(year_data)
    targets = pd.concat(frames)
    categorical_targets = to_categorical(targets)

    return categorical_targets


def weight_bias(vis):

    # Scaling by total/2 helps keep the loss to a similar magnitude.
    # The sum of the weights of all examples stays the same.
    neg, pos = np.bincount(vis)
    total = neg + pos

    weight_for_0 = (1 / neg) * (total / 2.0)
    weight_for_1 = (1 / pos) * (total / 2.0)

    class_weight = {0: weight_for_0, 1: weight_for_1}
    initial_bias = np.log([pos / neg])

    return class_weight, initial_bias
