from tensorflow import keras
from model import fognet_ntiers
from stack import stack_ntiers
from target import labels, weight_bias
from plot import plot_loss, plot_metrics, plot_cm, plot_roc, plot_prc
import os
import tempfile
from params import EPOCHS, BATCH_SIZE, STACK, TARGET, YEARS, PROG, PRIORITY_CLASS
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import logging

logger = logging.getLogger("example_logger")


mpl.rcParams["figure.figsize"] = (12, 10)
colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

training_stack_input, training_stack = stack_ntiers(STACK, YEARS["training"], PROG)
training_labels_cat, training_labels = labels(
    TARGET, YEARS["training"], PROG, PRIORITY_CLASS
)

validating_stack_input, validating_stack = stack_ntiers(
    STACK, YEARS["validating"], PROG
)
validating_labels_cat, validating_labels = labels(
    TARGET, YEARS["validating"], PROG, PRIORITY_CLASS
)

testing_stack_input, testing_stack = stack_ntiers(STACK, YEARS["testing"], PROG)
testing_labels_cat, testing_labels = labels(
    TARGET, YEARS["testing"], PROG, PRIORITY_CLASS
)

class_weight, initial_bias = weight_bias(training_labels.values.astype(np.int))

early_stopping = keras.callbacks.EarlyStopping(
    monitor="val_prc", verbose=1, patience=10, mode="max", restore_best_weights=True
)


model = fognet_ntiers(training_stack_input, output_bias=initial_bias)
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
