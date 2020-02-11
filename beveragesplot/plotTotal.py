import numpy as np
from matplotlib import pyplot as plt
from pdb import set_trace
import random


def autolabel(rects, result_as_int=False):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for bar in rects:
        height = bar.get_height()
        pos_y = bar.get_y()
        if not height:
            continue
        if result_as_int:
            height = int(height)
        plt.annotate(
                str(height),
                xy=(bar.get_x() + bar.get_width() / 2, pos_y + height / 2),
                ha='center',
                xytext=(0, 0),
                textcoords="offset points",
                va='center',
                color='black')


def plot_single_number(title, data, filename):
    plt.style.use('dark_background')

    fig = plt.figure()

    plt.annotate(
            data,
            xy=(0.5, 0.5),
            ha='center',
            va='center',
            xytext=(0, 0),
            size=190,
            textcoords="offset pixels",
            color='white')

    # Add some text for labels, title and custom x-pltis tick labels, etc.
    plt.title(title, size=60)
    plt.axis('off')

    my_dpi = 96
    fig.tight_layout(pad=0)
    fig.set_size_inches(1280/my_dpi, 1024/my_dpi)
    fig.savefig('images/' + filename)


def plot_one_dimensional(title, ylabel, xlabel, labels, data, filename):
    labels_temp = []
    data_temp = []

    for index, entry in enumerate(data):
        if entry:
            labels_temp.append(labels[index])
            data_temp.append(entry)

    labels = labels_temp
    data = data_temp

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
    plt.xticks(x, labels, rotation=45)
    plt.grid(axis='y')

    my_dpi = 96
    fig.tight_layout(pad=0)
    fig.set_size_inches(1280/my_dpi, 1024/my_dpi)
    fig.savefig('images/' + filename, dpi=my_dpi, bbox_inches='tight')


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

    data = list(zip(*drinks_per_id_normalized))
    data = np.array(data)

    for i in range(len(all_drinks)):
        offset = np.zeros(len(data[0]))
        for j in range(i):
            offset += data[j]
        bar = plt.bar(
                x,
                data[i],
                width,
                bottom=offset)

        autolabel(bar, True)

    # Add some text for labels, title and custom x-pltis tick labels, etc.
    plt.ylabel('Anzahl')
    plt.xlabel('Fachschaftsmitglieder')
    plt.title('Getränkevielfalt\n'
              'wer trinkt was?')
    plt.xticks(x, labels, rotation=45)
    plt.legend(all_drinks)
    plt.grid(axis='y')

    axes = plt.gca()
    ylim = axes.get_ylim()
    axes.set_ylim([0, ylim[1]+1])

    my_dpi = 96
    fig.tight_layout(pad=0)
    fig.set_size_inches(1280/my_dpi, 1024/my_dpi)
    fig.savefig('images/detail.png', dpi=my_dpi, bbox_inches='tight')


def plot_debt_sum(entries):
    labels = [obj.name for obj in entries]
    owes = [obj.owes_total for obj in entries]

    plot_single_number(
            'Schulden gesamt',
            '{:.2f}€'.format(sum(owes)),
            'owelist_total.png')


def plot_payed_sum(entries):
    payments = [obj.payments for obj in entries]

    total_money = 0

    for payment in payments:
        for pay in payment:
            total_money += payment[pay]

    plot_single_number(
            'Bereits gezahlt',
            '{:.2f}€'.format(total_money),
            'payed_total.png')


def plot_bottles_sum(entries, type=None):
    labels = [obj.name for obj in entries]
    drinks = [obj.drinks for obj in entries]

    bottles_total = 0

    for drink in drinks:
        for d in drink:
            if d == 'Kaffee':
                continue
            elif type:
                if d != type:
                    continue
            bottles_total += drink[d]

    plot_single_number(
            f'verkaufte Flaschen\n{type if type else ""}',
            f'{str(bottles_total)}',
            f'bottles{"_"+type if type else ""}_total.png')


def plot_liter_sum(entries):
    labels = [obj.name for obj in entries]
    drinks = [obj.drinks for obj in entries]

    liters_total = []

    for drink in drinks:
        liter = 0
        for d in drink:
            if d == 'Kaffee':
                liter += drink[d] * 0.3
            else:
                liter += drink[d] * 0.5
        liters_total.append(round(liter, 2))

    plot_single_number(
            'Literkonsum gesamt',
            f'{str(round(sum(liters_total), 2))} L',
            'liters_total.png')


def plot_liters(entries):
    labels = [obj.name for obj in entries]
    drinks = [obj.drinks for obj in entries]

    liters_total = []

    for drink in drinks:
        liter = 0
        for d in drink:
            if d == 'Kaffee':
                liter += drink[d] * 0.3
            else:
                liter += drink[d] * 0.5
        liters_total.append(round(liter, 2))

    plot_one_dimensional(
            'Literkonsum der Mitglieder\nwer sind die Suffköpfe?',
            'in Litern',
            'Fachschaftsmitglieder',
            labels,
            liters_total,
            'liters.png')


def plot_total_owe_list(entries):
    labels = [obj.name for obj in entries]
    owes = [obj.owes_total for obj in entries]

    plot_one_dimensional(
            'Schuldenberg der Fachschaftsmitglieder\nWO IST UNSER GELD ???',
            'in Euro',
            'Fachschaftsmitglieder',
            labels,
            owes,
            'owes.png')


def plot_specific_drink(entries, drink):
    drinks = [obj.drinks for obj in entries]
    labels = [obj.name for obj in entries]

    # lists with owes (for drink and name)
    drink_owe = []
    label_owe = []

    # create list with number of bought drinks (specified in parameter)
    for item in drinks:
        if drink in item:
            drink_owe.append(item[drink])
        else:
            drink_owe.append(0)

    # list of names who bought specified drink
    for idx, name in enumerate(labels):
        if drink_owe[idx]:
            label_owe.append(name)

    plot_one_dimensional(
            'Konsum von ' + drink,
            'Anzahl an Getränken',
            'Fachschaftsmitglieder',
            label_owe,
            [x for x in drink_owe if x is not 0],
            drink + '.png')


def plot_pie(entries):
    # Data to plot
    drinks = [obj.drinks for obj in entries]

    drinks_per_id = []
    list_of_drinks = []
    number_drinks = []

    for drink in drinks:
        drink_types = {}
        for d in drink:
            if d not in list_of_drinks:
                list_of_drinks.append(d)
            if d not in drink_types:
                drink_types[d] = 0
            drink_types[d] += drink[d]
        drinks_per_id.append(drink_types)

    for idx, drink in enumerate(list_of_drinks):
        for x in drinks_per_id:
            if drink in x:
                try:
                    tmp = number_drinks[idx]
                except:
                    tmp = 0

                if not tmp:
                    number_drinks.append(0)
                number_drinks[idx] += x[drink]

    # calculate percentage of each drink number and round it
    number_drinks = [round(((x * 100) / sum(number_drinks)), 2) for x in number_drinks]

    explode = []

    for idx, x in enumerate(number_drinks):
        explode.append(random.randrange(0,9,1)/10)

    #explode = [0.1] * len(number_drinks)
    #explode[0] = 0.1

    plt.style.use('dark_background')
    fig = plt.figure()

    plt.pie(number_drinks, textprops={'color': 'red'}, explode=explode, labels=list_of_drinks, autopct='%1.1f%%',
            shadow=False, startangle=140)

    plt.axis('equal')

    my_dpi = 96
    fig.tight_layout(pad=0)
    fig.set_size_inches(1280/my_dpi, 1024/my_dpi)
    fig.savefig('images/pie.png', dpi=my_dpi, bbox_inches='tight')

