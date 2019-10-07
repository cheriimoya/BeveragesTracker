import numpy as np
from matplotlib import pyplot as plt
from pdb import set_trace


def plotTotal(idList, persons):
    labels = [obj.name for obj in idList]


    owes = [obj.owes_total for obj in idList]


    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    plt.style.use('dark_background')

    # disable toolbar
    plt.rcParams['toolbar'] = 'None'

    fig, ax = plt.subplots()
    rects1 = ax.bar(x/2, owes, width)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('in Euro', fontsize=20)
    ax.set_xlabel('Fachschaftsmitglieder', fontsize=20)
    ax.set_title('Schuldenberg der Fachschaftsmitglieder\n'
                 'WO IST UNSER GELD ???', fontsize=20)
    ax.set_xticks(x/2)
    ax.set_xticklabels(labels, fontsize=20)
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, -25),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=20
                        )

    autolabel(rects1)

    fig.tight_layout()

    return plt
