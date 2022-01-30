import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import sklearn
import numpy as np
from sklearn.metrics import confusion_matrix


mpl.rcParams["figure.figsize"] = (12, 10)
colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]


def plot_loss(history, label, n):
    # Use a log scale on y-axis to show the wide range of values.
    plt.semilogy(
        history.epoch, history.history["loss"], color=colors[n], label="Train " + label
    )
    plt.semilogy(
        history.epoch,
        history.history["val_loss"],
        color=colors[n],
        label="Val " + label,
        linestyle="--",
    )
    plt.xlabel("Epoch")
    plt.ylabel("Loss")


def plot_metrics(history):
    metrics = ["loss", "prc", "precision", "recall"]
    for n, metric in enumerate(metrics):
        name = metric.replace("_", " ").capitalize()
        plt.subplot(2, 2, n + 1)
        plt.plot(history.epoch, history.history[metric], color=colors[0], label="Train")
        plt.plot(
            history.epoch,
            history.history["val_" + metric],
            color=colors[0],
            linestyle="--",
            label="Val",
        )
        plt.xlabel("Epoch")
        plt.ylabel(name)
        if metric == "loss":
            plt.ylim([0, plt.ylim()[1]])
        elif metric == "auc":
            plt.ylim([0.8, 1])
        else:
            plt.ylim([0, 1])

        plt.legend()


def plot_cm(labels, predictions, p=0.5):
    cm = confusion_matrix(labels, predictions > p)
    plt.figure(figsize=(5, 5))
    sns.heatmap(cm, annot=True, fmt="d")
    plt.title("Confusion matrix @{:.2f}".format(p))
    plt.ylabel("Actual label")
    plt.xlabel("Predicted label")

    print("Legitimate Transactions Detected (True Negatives): ", cm[0][0])
    print("Legitimate Transactions Incorrectly Detected (False Positives): ", cm[0][1])
    print("Fraudulent Transactions Missed (False Negatives): ", cm[1][0])
    print("Fraudulent Transactions Detected (True Positives): ", cm[1][1])
    print("Total Fraudulent Transactions: ", np.sum(cm[1]))


def plot_roc(name, labels, predictions, **kwargs):
    fp, tp, _ = sklearn.metrics.roc_curve(labels, predictions)

    plt.plot(100 * fp, 100 * tp, label=name, linewidth=2, **kwargs)
    plt.xlabel("False positives [%]")
    plt.ylabel("True positives [%]")
    plt.xlim([-0.5, 20])
    plt.ylim([80, 100.5])
    plt.grid(True)
    plt.legend(loc="lower right")
    ax = plt.gca()
    ax.set_aspect("equal")


def plot_prc(name, labels, predictions, **kwargs):
    precision, recall, _ = sklearn.metrics.precision_recall_curve(labels, predictions)

    plt.plot(precision, recall, label=name, linewidth=2, **kwargs)
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.grid(True)
    plt.legend(loc="lower right")
    ax = plt.gca()
    ax.set_aspect("equal")
