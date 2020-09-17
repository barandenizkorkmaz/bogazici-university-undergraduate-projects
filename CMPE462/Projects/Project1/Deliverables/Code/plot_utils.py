import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

from mpl_toolkits.mplot3d.axes3d import get_test_data
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

def show_images(DIGIT1,DIGIT2):
    plt.figure(figsize=(8, 4))
    plt.subplot(121)
    plt.imshow(DIGIT1)
    plt.title("Image: Digit 1")
    plt.subplot(122)
    plt.imshow(DIGIT2)
    plt.title("Image: Digit 5")
    plt.show()

def error_vs_time_visualization(TUNED_PARAMETER_LIST,ERRORS,ITERATION_COUNTS,TITLE,TUNED_PARAMETER):
    ITERATION_COUNTS = [[x for x in range(1, it + 1)] for it in ITERATION_COUNTS]
    col = 1
    fig = plt.figure(1)
    plt.suptitle('Error v Iterations for '+str(TITLE))
    for (tuned_parameter, error, iteration) in zip(TUNED_PARAMETER_LIST, ERRORS, ITERATION_COUNTS):
        ax = fig.add_subplot(len(TUNED_PARAMETER_LIST), 1, col)
        ax.plot(iteration, error)
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Error")
        ax.set_title(TUNED_PARAMETER+": " + str(tuned_parameter),fontsize=8)
        col = col + 1
    plt.show()

def error_vs_w_3d_visualization(ERRORS,WEIGHTS,TUNED_PARAMETER_LIST,TITLE,TUNED_PARAMETER):
    row = 1
    for (tuned_parameter, errors, weights) in zip(TUNED_PARAMETER_LIST, ERRORS, WEIGHTS):
        X=[weight[0][1] for weight in weights]
        Y=[weight[0][2] for weight in weights]
        X=np.array(X)
        Y=np.array(Y)
        Z=np.array(errors)
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot(X, Y, Z, label='E(w) v w')
        ax.set_xlabel("W1")
        ax.set_ylabel("W2")
        ax.set_zlabel("Error")
        ax.set_title("Error vs Weights for " + str(TITLE) +"\n"+TUNED_PARAMETER +" : " + str(tuned_parameter))
        ax.legend(loc='lower left')
        row = row + 1
    plt.show()


def accuracy_plots(TRAINING_ACCURACY,TEST_ACCURACY,TUNED_PARAMETER_LIST,TITLE,TUNED_PARAMETER):
    #Rounding
    TRAINING_ACCURACY_ROUNDED = [ round(100*elem, 3) for elem in TRAINING_ACCURACY ]
    TEST_ACCURACY_ROUNDED = [ round(100*elem, 3) for elem in TEST_ACCURACY ]
    #Rounding
    x = np.arange(len(TUNED_PARAMETER_LIST))  # the label locations
    width = 0.2  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, TRAINING_ACCURACY_ROUNDED, width, label='Training')
    rects2 = ax.bar(x + width / 2, TEST_ACCURACY_ROUNDED, width, label='Test')
    ax.set_ylabel('Accuracy')
    ax.set_title('Accuracy per ' + TUNED_PARAMETER + ' for ' + TITLE)
    ax.set_xticks(x)
    ax.set_xticklabels(TUNED_PARAMETER_LIST)
    ax.legend()
    autolabel(rects1, ax)
    autolabel(rects2, ax)
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

def cross_validation_plots(current_accuracy, current_stdev, current_lambda_range, iteration_count, representation, mode):
    #Rounding
    current_accuracy_rounded = [round(100*elem, 3) for elem in current_accuracy]
    current_stdev_rounded = [round(100*elem, 3) for elem in current_stdev]
    current_lambda_range_rounded = [round(elem, 6) for elem in current_lambda_range] #discuss this
    #Rounding
    x = np.arange(len(current_lambda_range))
    width = 0.2
    fig, ax = plt.subplots(2)
    if mode:
        plt.suptitle("Bar Chart and Table for Cross Validation for " + representation + " - Iteration " + str(iteration_count))
    else:
        plt.suptitle("Bar Chart and Table for Cross Validation for " + representation)
    rects1 = ax[0].bar(x - width / 2, current_accuracy_rounded, width, label='Accuracy')
    rects2 = ax[0].bar(x + width / 2, current_stdev_rounded, width, label='Std Dev')
    ax[0].set_ylabel('Accuracy')
    ax[0].set_xticks(x)
    ax[0].set_xticklabels(current_lambda_range_rounded)
    ax[0].legend()
    autolabel(rects1, ax[0])
    autolabel(rects2, ax[0])

    clust_data = []
    clust_data.append(current_lambda_range_rounded)
    clust_data.append(current_accuracy_rounded)
    clust_data.append(current_stdev_rounded)
    # collabel = current_lambda_range
    rowlabel = ("Lambda", "Accuracy", "Std Dev")
    ax[1].axis('tight')
    ax[1].axis('off')
    the_table = ax[1].table(cellText=clust_data, rowLabels=rowlabel, cellLoc='center', loc='center')
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(10)
    fig.tight_layout()
    plt.show()