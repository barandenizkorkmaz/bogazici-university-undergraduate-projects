import matplotlib.pyplot as plt
import numpy as np

color = ['r','b','g']
marker = ['o','o','o']

def scatter_plot_util(data,labels,ax):
    distinct_labels = sorted(list(set(labels)))
    scatter_data = []
    for i in range(len(distinct_labels)):
        scatter_data.append([])
        for j in range(2):
            scatter_data[i].append([])
    for X,Y in zip(data,labels):
        class_index = distinct_labels.index(Y)
        scatter_data[class_index][0].append(X[0])
        scatter_data[class_index][1].append(X[1])
    for i in range(len(distinct_labels)):
        ax.scatter(scatter_data[i][0],scatter_data[i][1],c=color[i],marker=marker[i],label='Class ' + str(distinct_labels[i]))

def information_loss_plot(information_loss,d):
    information_loss_rounded = [round(elem,3) for elem in information_loss]
    x = np.arange(len(d))  # the label locations
    width = 0.5  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x, information_loss_rounded, width, label='Information Loss')
    ax.set_ylabel('Information Loss')
    ax.set_xlabel('d: New Dimensionality')
    ax.set_title('Information Loss vs d (New Dimensionality)')
    ax.set_xticks(x)
    ax.set_xticklabels(d)
    ax.legend()
    autolabel(rects1, ax)
    fig.tight_layout()
    plt.show()

# REFERENCE: https://matplotlib.org/3.2.1/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
def autolabel(rects,ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')