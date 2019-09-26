import numpy as np
from matplotlib import pyplot as plt


def plotTotal(idList):
    labels = [obj.name for obj in idList]
    owes = [obj.owes_total for obj in idList]

    # round complete list
    owes_tmp = [round(elem, 3) for elem in owes]
    owes = owes_tmp

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars
    
    # disable toolbar
    plt.rcParams['toolbar'] = 'None'

    fig, ax = plt.subplots()
    rects1 = ax.bar(x, owes, width)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Beverages')
    ax.set_xlabel('ID')
    ax.set_title('Total bought beverages this semester')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)

    fig.tight_layout()

    return plt
