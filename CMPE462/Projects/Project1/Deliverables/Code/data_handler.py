import numpy as np

N=16

#Make sure that the arrays in the list are of the same dimension.
def form_input_data(FEATURES):
    result = np.array(FEATURES).T
    result = np.insert(result, 0, 1, axis=1)
    return result

def combine_data(X,Y):
    Y = np.array(Y).reshape(len(Y),1)
    return np.hstack((X,Y))

def split_data(DATA):
    X,Y=[],[]
    for elem in DATA:
       X.append(elem[:-1])
       Y.append(elem[-1])
    return np.array(X).reshape(len(DATA),DATA.shape[1]-1),np.array(Y).reshape(len(DATA),1)

def s_fold_division(s,DATA):
    return np.array_split(DATA,s)

def get_min_index(LIST):
    min_value = LIST[0]
    min_index = 0
    for i in range(1,len(LIST)):
        if LIST[i]<min_value:
            min_index = i
            min_value = LIST[i]
    return min_index

def get_max_index(LIST):
    max_value = LIST[0]
    max_index = 0
    for i in range(1,len(LIST)):
        if LIST[i]>max_value:
            max_index = i
            max_value = LIST[i]
    return max_index

def scatter_plot_helper(LABELS,FEATURES):
    POSITIVE_CLASS,NEGATIVE_CLASS = [],[]
    for i in range(len(FEATURES)):
        POSITIVE_CLASS.append([])
        NEGATIVE_CLASS.append([])
    for i in range(len(LABELS)):
        if LABELS[i] == 1:
            for j in range(len(POSITIVE_CLASS)):
                POSITIVE_CLASS[j].append(FEATURES[j][i])
        else:
            for j in range(len(NEGATIVE_CLASS)):
                NEGATIVE_CLASS[j].append(FEATURES[j][i])
    return POSITIVE_CLASS,NEGATIVE_CLASS