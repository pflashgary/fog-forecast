import numpy as np


def labels():
    pass


def assign_weights(vis):

    # Scaling by total/2 helps keep the loss to a similar magnitude.
    # The sum of the weights of all examples stays the same.
    neg, pos = np.bincount(vis)
    total = neg + pos

    weight_for_0 = (1 / neg) * (total / 2.0)
    weight_for_1 = (1 / pos) * (total / 2.0)

    class_weight = {0: weight_for_0, 1: weight_for_1}
    initial_bias = np.log([pos / neg])

    return class_weight, initial_bias
