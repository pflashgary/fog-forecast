from tensorflow import keras
from model import fognet_ntiers
from stack import stack_6tier
from target import labels, assign_weights
from plot import plot_loss, plot_metrics, plot_cm, plot_roc, plot_prc
import os
import tempfile
import EPOCHS, BATCH_SIZE
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams["figure.figsize"] = (12, 10)
colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

training_stack_shape, training_stack = stack_6tier()
validating_stack_shape, validating_stack = stack_6tier()
testing_stack_shape, testing_stack = stack_6tier()

training_labels, validating_labels, testing_labels = labels()

class_weight, initial_bias = assign_weights()


early_stopping = keras.callbacks.EarlyStopping(
    monitor="val_prc", verbose=1, patience=10, mode="max", restore_best_weights=True
)


model = fognet_ntiers(training_stack_shape, output_bias=initial_bias)
careful_bias_history = model.fit(
    training_stack,
    training_labels,
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=(validating_stack, validating_labels),
    verbose=0,
)


plot_loss(careful_bias_history, "Careful Bias", 1)


initial_weights = os.path.join(tempfile.mkdtemp(), "initial_weights")
model.save_weights(initial_weights)

model = fognet_ntiers(training_stack_shape)
model.load_weights(initial_weights)

baseline_history = model.fit(
    training_stack,
    training_labels,
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    callbacks=[early_stopping],
    validation_data=(validating_stack, validating_labels),
)

plot_metrics(baseline_history)

train_predictions_baseline = model.predict(training_stack, batch_size=BATCH_SIZE)
test_predictions_baseline = model.predict(testing_stack, batch_size=BATCH_SIZE)


baseline_results = model.evaluate(
    testing_stack, testing_labels, batch_size=BATCH_SIZE, verbose=0
)

plot_cm(testing_labels, test_predictions_baseline)


weighted_model = fognet_ntiers()
weighted_model.load_weights(initial_weights)

weighted_history = weighted_model.fit(
    training_stack,
    training_labels,
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    callbacks=[early_stopping],
    validation_data=(validating_stack, validating_labels),
    # The class weights go here
    class_weight=class_weight,
)

plot_metrics(weighted_history)


train_predictions_weighted = weighted_model.predict(
    training_stack, batch_size=BATCH_SIZE
)
test_predictions_weighted = weighted_model.predict(testing_stack, batch_size=BATCH_SIZE)

weighted_results = weighted_model.evaluate(
    testing_stack, testing_labels, batch_size=BATCH_SIZE, verbose=0
)

plot_cm(testing_labels, test_predictions_weighted)


plot_roc("Train Baseline", training_labels, train_predictions_baseline, color=colors[0])
plot_roc(
    "Test Baseline",
    testing_labels,
    test_predictions_baseline,
    color=colors[0],
    linestyle="--",
)

plot_roc("Train Weighted", training_labels, train_predictions_weighted, color=colors[1])
plot_roc(
    "Test Weighted",
    testing_labels,
    test_predictions_weighted,
    color=colors[1],
    linestyle="--",
)

plot_prc("Train Baseline", training_labels, train_predictions_baseline, color=colors[0])
plot_prc(
    "Test Baseline",
    testing_labels,
    test_predictions_baseline,
    color=colors[0],
    linestyle="--",
)

plot_prc("Train Weighted", training_labels, train_predictions_weighted, color=colors[1])
plot_prc(
    "Test Weighted",
    testing_labels,
    test_predictions_weighted,
    color=colors[1],
    linestyle="--",
)
