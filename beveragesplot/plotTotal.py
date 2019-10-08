import numpy as np
from matplotlib import pyplot as plt
from pdb import set_trace


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        plt.annotate(str(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, -25),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=20
                    )


def plot_one_dimensional(title, ylabel, xlabel, labels, data, filename):
    x = np.arange(len(labels))  # the label locations
    width = 0.70  # the width of the bars

    plt.style.use('dark_background')

    fig = plt.figure()
    rects1 = plt.bar(x, data, width)
    
    autolabel(rects1)

    # Add some text for labels, title and custom x-pltis tick labels, etc.
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.xticks(x, labels)

    my_dpi = 96
    fig.tight_layout(pad=0)
    fig.set_size_inches(1280/my_dpi, 1024/my_dpi)
    fig.savefig(filename, dpi=my_dpi, bbox_inches='tight')


def plot_liters_detailed(entries):
    labels = [obj.name for obj in entries]
    drinks = [obj.drinks for obj in entries]

    drinks_per_id = []
    all_drinks = []

    for drink in drinks:
        drink_types = {}
        for d in drink:
            if d not in all_drinks:
                all_drinks.append(d)
            if d not in drink_types:
                drink_types[d] = 0
            drink_types[d] += drink[d]
        drinks_per_id.append(drink_types)

    drinks_per_id_normalized = []
    for index, drinks in enumerate(drinks_per_id):
        this_persons_drinks = []
        for d in all_drinks:
            if d in drinks_per_id[index]:
                this_persons_drinks.append(drinks_per_id[index][d])
            else:
                this_persons_drinks.append(0)
        drinks_per_id_normalized.append(this_persons_drinks)

    x = np.arange(len(labels))  # the label locations
    width = 0.70  # the width of the bars

    plt.style.use('dark_background')

    fig = plt.figure()

    colors = ['r', 'g', 'b', 'c', 'y', 'm']

    data = list(zip(*drinks_per_id_normalized))
    data = np.array(data)

    for i in range(len(all_drinks)):
        offset = np.zeros(len(data[0]))
        for j in range(i):
            offset += data[j]
        plt.bar(
                x,
                data[i],
                width,
                bottom=offset,
                color=colors[i])

    # Add some text for labels, title and custom x-pltis tick labels, etc.
    plt.ylabel('Anzahl')
    plt.xlabel('Fachschaftsmitglieder')
    plt.title('Getränkevielfalt\n'
                 'wer trinkt was?')
    plt.xticks(x, labels)
    plt.legend(all_drinks)

    axes = plt.gca()
    ylim = axes.get_ylim()
    axes.set_ylim([0, ylim[1]+1])

    my_dpi = 96
    fig.tight_layout(pad=0)
    fig.set_size_inches(1280/my_dpi, 1024/my_dpi)
    fig.savefig('detail.png', dpi=my_dpi, bbox_inches='tight')


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
