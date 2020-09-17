import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def plot_rss_v_threshold(rss_values,threshold_values,index,feature_labels):
    fig = plt.figure()
    ax = plt.scatter(threshold_values, rss_values)
    plt.xlabel("Threshold")
    plt.ylabel("RSS")
    plt.title("Rss vs Threshold Value for Feature {}".format(feature_labels[index]))
    plt.show()

def cross_validation_plot(depths,r2_scores,std_devs):
    #Rounding
    r2_scores = [round(elem, 5) for elem in r2_scores]
    std_devs = [round(elem, 5) for elem in std_devs]
    x = np.arange(len(depths))
    width = 0.2
    fig, ax = plt.subplots(2)
    plt.suptitle("Cross Validation: Mean and Std Dev of R-Squared vs Depth")
    rects1 = ax[0].bar(x - width / 2, r2_scores, width, label='Mean')
    rects2 = ax[0].bar(x + width / 2, std_devs, width, label='Std Dev')
    ax[0].set_ylabel('Mean and Std Dev of R-Squared')
    ax[0].set_xlabel('Depth')
    ax[0].set_xticks(x)
    ax[0].set_xticklabels(depths)
    ax[0].legend(loc='lower right')
    autolabel(rects1, ax[0])
    autolabel(rects2, ax[0])
    data = list()
    data.append(depths)
    data.append(r2_scores)
    data.append(std_devs)
    rowlabel = ("Depth", "Mean", "Std Dev")
    ax[1].axis('tight')
    ax[1].axis('off')
    table = ax[1].table(cellText=data, rowLabels=rowlabel, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    fig.tight_layout()
    plt.show()

# REFERENCE: https://matplotlib.org/3.2.1/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
def autolabel(rects,ax):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

def r2_plots(r2_training,r2_test,depths):
    #Rounding
    r2_score_training = [round(elem, 5) for elem in r2_training]
    r2_score_test = [round(elem, 5) for elem in r2_test]
    x = np.arange(len(r2_training))  # the label locations
    width = 0.2  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, r2_score_training, width, label='Training')
    rects2 = ax.bar(x + width / 2, r2_score_test, width, label='Test')
    if len(depths)==1:
        ax.set_title('R-Squared Values (Depth={})'.format(depths[0]))
    else:
        ax.set_title('R-Squared vs Depth')
    ax.set_ylabel('R-Squared Score')
    ax.set_xlabel('Depth')
    ax.set_xticks(x)
    ax.set_xticklabels(depths)
    ax.legend(loc='lower right')
    autolabel(rects1, ax)
    autolabel(rects2, ax)
    fig.tight_layout()
    plt.show()