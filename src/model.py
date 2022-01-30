from tensorflow import keras
from tensorflow.keras import Input
import METRICS, DROPOUT, FILTERS
import FogNet


def fognet_ntiers(
    stack_shape, filters=FILTERS, dropout=DROPOUT, metrics=METRICS, output_bias=None
):
    if output_bias is not None:
        output_bias = keras.initializers.Constant(output_bias)
    model = FogNet.FogNet(stack_shape, filters, dropout, 2)
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
        loss=keras.losses.CategoricalCrossentropy(),
        metrics=metrics,
    )

    return model
