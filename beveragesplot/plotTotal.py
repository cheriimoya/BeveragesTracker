import numpy as np
from matplotlib import pyplot as plt
from pdb import set_trace


def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, -25),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=20
                    )


def plot_one_dimensional(title, ylabel, xlabel, labels, data, filename):
    x = np.arange(len(labels))  # the label locations
    width = 0.70  # the width of the bars

    plt.style.use('dark_background')

    fig, ax = plt.subplots()
    rects1 = ax.bar(x, data, width)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    autolabel(rects1, ax)

    my_dpi = 96
    fig.tight_layout()
    fig.set_size_inches(1280/my_dpi, 1024/my_dpi)

    fig.savefig(filename, dpi=my_dpi)


def plot_liters(entries):
    labels = [obj.name for obj in entries]
    drinks = [obj.drinks for obj in entries]

    liters_total = []

    for drink in drinks:
        liter = 0
        for d in drink:
            liter += drink[d]
        liters_total.append(round(liter * 0.5, 2))

    plot_one_dimensional(
            'Literkonsum der Mitglieder\nwer sind die Suffköpfe?',
            'in Litern',
            'Fachschaftsmitglieder',
            labels,
            liters_total,
            'liters.png')


def plotTotal(entries):
    labels = [obj.name for obj in entries]
    owes = [obj.owes_total for obj in entries]

    plot_one_dimensional(
            'Schuldenberg der Fachschaftsmitglieder\nWO IST UNSER GELD ???',
            'in Euro',
            'Fachschaftsmitglieder',
            labels,
            owes,
            'owes.png')
