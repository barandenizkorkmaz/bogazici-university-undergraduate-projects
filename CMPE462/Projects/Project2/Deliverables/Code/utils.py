import matplotlib.pyplot as plt
import numpy as np
# Return X_training, Y_training, X_test, Y_test, respectively.
def rearrange_data(data_dict):
    x_training = data_dict['X'][0:150]
    x_test = data_dict['X'][150:]
    y_training = []
    y_test = []
    y = data_dict['Y']
    for i in range(150):
        y_training.append(y[i][0])
    for i in range(120):
        y_test.append(y[i+150][0])
    return x_training, y_training, x_test, y_test


def remove_sample(X, Y, candidate):
    if candidate == None:
        return X, Y
    X_NEW = np.delete(np.array(X), candidate-1, axis=0)
    Y_NEW = np.delete(np.array(Y), candidate-1, axis=0)
    return X_NEW, Y_NEW

def get_kernel_description(dict):
    kernel_type = dict['kernel_type']
    degree = dict['degree']
    gamma = dict['gamma']
    coeff = dict['coef0']
    if kernel_type == 0:
        return 'Linear'
    elif kernel_type == 1:
        return 'Polynomial: Degree=' + str(degree) + ' Coef0=' + str(coeff)
    elif kernel_type == 2:
        return 'RBF: Gamma=' + str(gamma)
    elif kernel_type == 3:
        return 'Sigmoid: Gamma=' + str(gamma) + ' Coef0=' + str(coeff)
    else:
        return 'Invalid Kernel Type'

def hard_margin_plot(data, config):
    # Rounding
    TRAINING_ACCURACY_ROUNDED = [round(data[0] * 1.0/100, 3)]
    TEST_ACCURACY_ROUNDED = [round(data[1] * 1.0/100, 3)]
    # Rounding
    x = np.arange(1)  # the label locations
    width = 0.2  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, TRAINING_ACCURACY_ROUNDED, width, label='Training')
    rects2 = ax.bar(x + width / 2, TEST_ACCURACY_ROUNDED, width, label='Test')
    ax.set_ylabel('Accuracy')
    ax.set_title('Hard-Margin SVM: ' + 'C=' + str(config['C']) + ' Eps=' + str(config['eps']) + ' NSV=' + str(data[2]))
    ax.legend()
    ax.set_xticks([])
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


def results_per_c_plot(data, c, mode):
    fig, ax = plt.subplots(1)
    column_labels = ["Kernel Type", "Degree", "Gamma", "Coef0", "Eps", "Tr Acc", "Test Acc", "nSV"]
    if mode == 1:
        plt.title('Task 2 - Soft Margin SVM: Report for C = ' + str(c))
    elif mode == 2:
        plt.title('Task 4 - Removal of Support Vectors: Report for C = ' + str(c))
        column_labels.append('Removed Sample')
    elif mode == 3:
        plt.title('Task 4 - Removal of Non-Support Vectors: Report for C = ' + str(c))
        column_labels.append('Removed Sample')
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=data, colLabels=column_labels, cellLoc='center', loc='center')
    table.auto_set_font_size(True)
    table.auto_set_column_width(col=list(range(len(column_labels))))
    plt.show()

def kernel_vs_c_plot(data, c_list):
    fig, ax = plt.subplots(1)
    plt.title('Task 3 - Kernel vs C Analysis: Report')
    column_labels = ["Kernel Description"]
    for current_c in c_list:
        column_labels.append('C = ' +  str(current_c))

    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=data, colLabels=column_labels, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(column_labels))))
    plt.show()

def get_qp_params(X, Y):
    X_np = np.array(X, dtype=float)
    Y_np = np.array(Y, dtype=float)
    d = X_np.shape[1] #number of features
    N = X_np.shape[0] #number of samples

    Q = np.zeros(d+1, dtype=float).T
    P = np.zeros((d+1)**2, dtype=float).reshape(d+1, d+1)
    identity_matrix = np.identity(d, dtype=float)
    P[1:, 1:] = identity_matrix

    H = np.ones(N, dtype=float)*(-1)
    G = []

    for (x_i, y_i) in zip(X,Y):
        G.append(np.hstack(([y_i], np.multiply(x_i, y_i))))

    G = np.multiply(G,-1)
    return P,Q,G,H