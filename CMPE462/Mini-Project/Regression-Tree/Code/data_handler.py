import numpy as np

def form_data(X,Y):
    X,Y = np.array(X),np.array(Y)
    Y = Y.reshape(len(Y), 1)
    return np.hstack((X, Y))

def split_data(DATA):
    DATA = np.array(DATA)
    x = []
    y = []
    for row in DATA:
        x.append(row[:-1])
        y.append(row[-1])
    return np.array(x),np.array(y)

def feature_unique_values(X):
    dict = {}
    for (i,row) in enumerate(X):
        cur = []
        for elem in row:
            if elem not in cur:
                cur.append(elem)
        cur.sort()
        dict[i] = cur
    return dict

def feature_index(FEATURE_NAMES):
    dict = {}
    for (i,elem) in enumerate(FEATURE_NAMES):
        dict[elem] = i
    return dict