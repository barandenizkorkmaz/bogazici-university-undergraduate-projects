import math
import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
import datetime
import data_handler
import plot_utils

def sigmoid(s):
    return 1 / (1 + np.exp(-s))

def error(X,Y,W,N,Lambda):
    result = 0.0
    for (x1,y1) in zip(X,Y):
        exp = np.exp(-1*y1*(W.dot(x1.reshape(X.shape[1],1))))
        result = result + math.log((1+exp),math.e)
    result = result / N
    if not(Lambda == None) and not(Lambda == 0.0):
        result += Lambda/2 * pow(LA.norm(W),2)
    return result

def gradient(X,Y,W,N,Lambda):
    result = np.zeros(X.shape[1]).reshape(1,X.shape[1])
    for (x1,y1) in zip(X,Y):
        result = result + -1*y1*(x1.reshape(1,X.shape[1]))*sigmoid(-1*y1*W.dot(x1.reshape(X.shape[1],1)))
    result = np.divide(result,N)
    if not(Lambda == None) and not(Lambda == 0.0):
        result += np.multiply(W,Lambda)
    return result

def logistic_regression(X,Y,W,N,LEARNING_RATE,LAMBDA):
    ERRORS = []
    WEIGHTS = []
    epsilon = pow(10, -4)
    error_next = error(X, Y, W, N, LAMBDA)
    while True:
        gradient_w = gradient(X, Y, W, N, LAMBDA)
        W_next = W - LEARNING_RATE * gradient_w
        error_current = error_next
        ERRORS.append(error_current)
        WEIGHTS.append(W)
        error_next = error(X, Y, W_next, N, LAMBDA)
        if epsilon > abs(error_next - error_current):
            break
        W = W_next
    return W, ERRORS, WEIGHTS

def logistic_regression_manager(X,Y,LEARNING_RATES,LAMBDA):
    ERRORS = []
    WEIGHTS_LIST = []
    W_OPTIMAL = []
    for learning_rate in LEARNING_RATES:
        W = np.random.randn(1, X.shape[1])
        W_OPTIMAL, CURRENT_LOSS, WEIGHTS = logistic_regression(X=X, Y=Y, W=W, N=len(Y), LEARNING_RATE=learning_rate, LAMBDA=LAMBDA)
        ERRORS.append(CURRENT_LOSS)
        WEIGHTS_LIST.append(WEIGHTS)
    MINIMUM_ERRORS = [element[-1] for element in ERRORS]
    ITERATION_COUNTS = [len(ERRORS[i]) for i in range(len(LEARNING_RATES))]
    return W_OPTIMAL,WEIGHTS_LIST,ERRORS,ITERATION_COUNTS

def regularization_manager(X,Y,LEARNING_RATE,LAMBDA_LIST):
    ERRORS = []
    WEIGHTS_LIST = []
    W_OPTIMAL = []
    for regularization_coeff in LAMBDA_LIST:
        W = np.random.randn(1, X.shape[1])
        W_OPTIMAL, CURRENT_LOSS, WEIGHTS = logistic_regression(X=X, Y=Y, W=W, N=len(Y), LEARNING_RATE=LEARNING_RATE, LAMBDA=regularization_coeff)
        ERRORS.append(CURRENT_LOSS)
        WEIGHTS_LIST.append(WEIGHTS)
    MINIMUM_ERRORS = [element[-1] for element in ERRORS]
    ITERATION_COUNTS = [len(ERRORS[i]) for i in range(len(LAMBDA_LIST))]
    return W_OPTIMAL,WEIGHTS_LIST,ERRORS,ITERATION_COUNTS

def predict(X,W):
    RESULT = []
    for s in W.dot(np.transpose(X)):
        RESULT.append(sigmoid(s))
    return np.array(RESULT).reshape(1,len(X))

def accuracy_score(Y_Target,Y_Predicted):
    correct = 0.0
    for (y_pred,y_targ) in zip(Y_Predicted[0],Y_Target):
        estimation = 1 if y_pred>0.5 else -1
        if estimation == y_targ:
            correct += 1.0
    return (correct/len(Y_Target))

def get_optimal_weights(X_TRAINING,X_TEST,Y_TRAINING,Y_TEST,WEIGHTS_LIST,TUNED_PARAMETER_LIST,TITLE,TUNED_PARAMETER):
    TRAINING_ACCURACY = []
    TEST_ACCURACY = []
    for weights in WEIGHTS_LIST:
        final_weight = weights[-1]
        y_predicted_training = predict(X_TRAINING,final_weight)
        y_predicted_test = predict(X_TEST,final_weight)
        training_accuracy = accuracy_score(Y_TRAINING,y_predicted_training)
        test_accuracy = accuracy_score(Y_TEST,y_predicted_test)
        TRAINING_ACCURACY.append(training_accuracy)
        TEST_ACCURACY.append(test_accuracy)
    #Plotting
    plot_utils.accuracy_plots(TRAINING_ACCURACY,TEST_ACCURACY,TUNED_PARAMETER_LIST,TITLE,TUNED_PARAMETER)
    max_index = data_handler.get_max_index(TEST_ACCURACY)
    return WEIGHTS_LIST[max_index][-1],TUNED_PARAMETER_LIST[max_index]

def cross_validation(X,Y,LAMBDA,s):
    data_set = data_handler.combine_data(X,Y)
    np.random.shuffle(data_set)
    X,Y = data_handler.split_data(data_set)
    pieces_x = data_handler.s_fold_division(s,X)
    pieces_y = data_handler.s_fold_division(s,Y)
    X_I_TRAINING_LIST = []
    Y_I_TRAINING_LIST = []
    for i in range(s):
        x_i_training = []
        y_i_training = []
        for j in range(s):
            if j==i:
                continue
            x_i_training += list(pieces_x[j])
            y_i_training += list(pieces_y[j])
        X_I_TRAINING_LIST.append(np.array(x_i_training))
        Y_I_TRAINING_LIST.append(np.array(y_i_training))
    accuracy_result = []
    stdev_result = []
    w_init = np.random.randn(1,X.shape[1])
    LEARNING_RATE = [0.05]
    for lmbda in LAMBDA:
        current_accuracy = []
        for i in range(s):
            x_i_training = X_I_TRAINING_LIST[i]
            y_i_training = Y_I_TRAINING_LIST[i]
            x_i_test = np.array(pieces_x[i])
            y_i_test = np.array(pieces_y[i])
            w_optimal,_,_ = logistic_regression(x_i_training,y_i_training,w_init,len(y_i_training),LEARNING_RATE,lmbda)
            y_i_predict = predict(x_i_test,w_optimal)
            accuracy_i = accuracy_score(y_i_test,y_i_predict)
            current_accuracy.append(accuracy_i)
        accuracy_result.append(np.average(current_accuracy))
        stdev_result.append(np.std(current_accuracy))
    return accuracy_result,stdev_result

def cross_validation_manager(X, Y, s, lambda_list, mode, representation):
    iteration_count = 0
    optimal_accuracy = 0.0
    optimal_lambda = 0.0
    lower_limit = 0.0
    upper_limit = 1.0
    while True:
        iteration_count += 1
        current_lambda_range = [(i) * (upper_limit-lower_limit) * 0.2 + lower_limit for i in range(s)] if mode else lambda_list
        current_accuracy_result, current_stdev_result = cross_validation(X, Y, current_lambda_range, s)
        current_accuracy = max(current_accuracy_result)
        current_accuracy_index = current_accuracy_result.index(current_accuracy)
        mean_limit = current_lambda_range[current_accuracy_index]
        accuracy_difference = current_accuracy - optimal_accuracy
        if optimal_accuracy >= current_accuracy or accuracy_difference < math.pow(10, -5) or (not mode):
            plot_utils.cross_validation_plots(current_accuracy_result, current_stdev_result, current_lambda_range, iteration_count, representation, mode)
            break
        else:
            plot_utils.cross_validation_plots(current_accuracy_result, current_stdev_result, current_lambda_range, iteration_count, representation, mode)
            optimal_accuracy = current_accuracy
            optimal_lambda = mean_limit
            delta = (upper_limit - lower_limit)/10
            upper_limit = mean_limit + delta
            lower_limit = mean_limit - delta if (mean_limit - 0.2 > 0.0) else 0.0
            continue
    return optimal_lambda