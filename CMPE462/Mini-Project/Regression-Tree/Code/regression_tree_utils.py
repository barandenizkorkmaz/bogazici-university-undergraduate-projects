import numpy as np
import math
from sklearn.metrics import r2_score

import data_handler
import plot_utils

def rss(y_left,y_right):
    avg_left, avg_right = np.average(y_left),np.average(y_right)
    rss = 0.0
    for elem_left in y_left:
        rss += math.pow(elem_left-avg_left,2)
    for elem_right in y_right:
        rss += math.pow(elem_right-avg_right,2)
    return rss

def split_feature_by_threshold(index,value,data_set):
    left,right = [],[]
    for row in data_set:
        if row[index] <= value:
            left.append(row)
        else:
            right.append(row)
    return np.array(left),np.array(right)

def find_split_by_feature(index,data_set,enable_plot=False,feature_labels=None):
    b_threshold, b_rss, b_left, b_right = 0.0, float('inf'), None, None
    xTrain, yTrain = data_handler.split_data(data_set)
    xTrain_T = np.transpose(xTrain)
    threshold_candidates = data_handler.feature_unique_values(xTrain_T)[index]
    rss_values = []
    thresholds = []
    for threshold in threshold_candidates:
        left,right = split_feature_by_threshold(index,threshold,data_set)
        _,left_y = data_handler.split_data(left)
        _,right_y = data_handler.split_data(right)
        if len(left_y)==0 or len(right_y)==0:
            continue
        current_rss = rss(left_y,right_y)
        thresholds.append(threshold)
        rss_values.append(current_rss)
        if current_rss < b_rss:
            b_threshold , b_rss , b_left , b_right = threshold, current_rss, left, right
    if enable_plot==True:
        plot_utils.plot_rss_v_threshold(rss_values,thresholds,index,feature_labels)
    return b_threshold, b_rss, b_left, b_right

def split_node(data_set):
    b_feature, b_threshold, b_rss, b_left , b_right =0, 0.0, float('inf'), None, None
    data_set = np.array(data_set)
    for i in range(data_set.shape[1]-1):
        cur_threshold, cur_rss,cur_left,cur_right = find_split_by_feature(i,data_set)
        if cur_rss < b_rss:
            b_feature, b_threshold, b_rss, b_left, b_right = i, cur_threshold, cur_rss, cur_left, cur_right
    #print("Best split for current data set: feature: {}, Threshold: {}, RSS: {:.10}".format(b_feature,b_threshold,b_rss))
    return {'feature': b_feature,'threshold': b_threshold,'rss': b_rss,'left': b_left,'right': b_right}

def set_leaf(data):
    x,y = data_handler.split_data(data)
    return sum(y)/len(y)

def split_tree(node, min_size, max_depth, current_depth):
    left_data = node['left']
    right_data = node['right']
    if current_depth==max_depth:
        node['left'] = set_leaf(left_data)
        node['right'] = set_leaf(right_data)
        return
    #left child
    if len(node['left']) <= min_size:
        node['left'] = set_leaf(left_data)
    else:
        node['left'] = split_node(left_data)
        split_tree(node['left'],min_size,max_depth,current_depth+1)
    #right child
    if len(node['right']) <= min_size:
        node['right'] = set_leaf(right_data)
    else:
        node['right'] = split_node(right_data)
        split_tree(node['right'],min_size,max_depth,current_depth+1)

def train_tree(training_data,min_size, max_depth):
    root = split_node(training_data)
    split_tree(root,min_size,max_depth,1)
    return root

def cross_validation(data,s,depths):
    folds = np.array_split(data,s)
    training_data_list = []
    b_depth, b_r2score = None, float('-inf')
    for i in range(s):
        training_data = []
        for j in range(s):
            if not j==i:
                training_data += list(folds[j])
        training_data_list.append(np.array(training_data))
    mean_r2_scores = []
    std_r2_scores = []
    for depth in depths:
        current_r2_scores = []
        for i in range(s):
            training_data = training_data_list[i]
            test_data = folds[i]
            _,y_test = data_handler.split_data(test_data)
            tree = train_tree(training_data,1,depth)
            y_predict = predict(tree,test_data)
            current_r2_score = r2_score(y_test,y_predict)
            current_r2_scores.append(current_r2_score)
        avg_r2_score = np.average(current_r2_scores)
        if avg_r2_score>b_r2score:
            b_depth = depth
            b_r2score = avg_r2_score
        mean_r2_scores.append(np.average(current_r2_scores))
        std_r2_scores.append(np.std(current_r2_scores))
    return b_depth,mean_r2_scores,std_r2_scores

def predict_sample(node,sample):
    if sample[node['feature']] <= node['threshold']:
        if isinstance(node['left'], dict):
            return predict_sample(node['left'], sample)
        else:
            return node['left']
    else:
        if isinstance(node['right'], dict):
            return predict_sample(node['right'], sample)
        else:
            return node['right']

def predict(root,data):
    return [predict_sample(root,sample) for sample in data]