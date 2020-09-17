import scipy.io as sio
import libsvm.svmutil as svm
import libsvm.svm
import numpy as np
import math
import matplotlib.pyplot as plt
import utils
import random
import cvxopt

#
# CONFIGURATIONS
#

svm_cost_config = [0.1,1,10,100,1000]

hard_margin_svm_config = {'svm_type': 0, 'C': math.pow(10,9), 'eps': math.pow(10,-5)}

kernel_config = {1:{'kernel_type': 0, 'degree': 0, 'gamma': 0, 'coef0': 0, 'eps': 0.1},
                 2: {"kernel_type": 1, "degree": 2, "gamma": 1, "coef0": 0, "eps": 0.1},
                 3: {"kernel_type": 1, "degree": 3, "gamma": 1, "coef0": 0, "eps": 0.1},
                 4: {"kernel_type": 1, "degree": 4, "gamma": 1, "coef0": 0, "eps": 0.1},
                 5:{"kernel_type": 2, "degree": 0, "gamma": 0.001, "coef0": 0, "eps": 0.1},
                 6:{"kernel_type": 2, "degree": 0, "gamma": 0.01, "coef0": 0, "eps": 0.1},
                 7:{"kernel_type": 2, "degree": 0, "gamma": 0.1, "coef0": 0, "eps": 0.1},
                 8:{"kernel_type": 2, "degree": 0, "gamma": 1, "coef0": 0, "eps": 0.1},
                 9:{"kernel_type": 2, "degree": 0, "gamma": 10, "coef0": 0, "eps": 0.1},
                 10:{"kernel_type": 3, "degree": 0, "gamma": 0.001, "coef0": 0, "eps": 0.1},
                 11:{"kernel_type": 3, "degree": 0, "gamma": 0.01, "coef0": 0, "eps": 0.1},
                 12:{"kernel_type": 3, "degree": 0, "gamma": 0.1, "coef0": 0, "eps": 0.1},
                 13:{"kernel_type": 3, "degree": 0, "gamma": 1, "coef0": 0, "eps": 0.1},
                 14:{"kernel_type": 3, "degree": 0, "gamma": 10, "coef0": 0, "eps": 0.1}
                 }


kernel_codes = {0 : 'Linear', 1: 'Polynomial', 2: 'RBF', 3: 'Sigmoid'}

#
# IMPORT DATA
#

data_dict = sio.loadmat('data.mat')
X_training, Y_training, X_test, Y_test = utils.rearrange_data(data_dict)

#
# TASK 1: Hard-Margin SVM
#

param = svm.svm_parameter('-q')
problem = svm.svm_problem(Y_training, X_training)

param.svm_type = hard_margin_svm_config['svm_type']
param.C = hard_margin_svm_config['C']
param.eps = hard_margin_svm_config['eps']

model = svm.svm_train(problem, param)
training_labels, training_accuracy, training_values = svm.svm_predict(Y_training, X_training, model,'-q')
test_labels, test_accuracy, test_values = svm.svm_predict(Y_test, X_test, model,'-q')

hard_margin_sv_list = model.get_SV()
hard_margin_results = [training_accuracy[0],test_accuracy[0],len(hard_margin_sv_list)]
utils.hard_margin_plot(hard_margin_results,hard_margin_svm_config)

#
# TASK 2: Soft-Margin SVM
#
param = svm.svm_parameter('-q')
problem = svm.svm_problem(Y_training, X_training)
task_2_results = []
task_3_results = []
support_vector_candidates = []
non_support_vector_candidates = []
for i in range(len(svm_cost_config)):
    task_2_results.append([])
    support_vector_candidates.append([])
    non_support_vector_candidates.append([])

for index,j in enumerate(kernel_config):
    kernel_description = utils.get_kernel_description(kernel_config[j])
    task_3_results.append([kernel_description])

for i,current_c in enumerate(svm_cost_config):
    param.C = current_c
    for index,j in enumerate(kernel_config.keys()):
        param.kernel_type = kernel_config[j]['kernel_type']
        param.degree = kernel_config[j]['degree']
        param.gamma = kernel_config[j]['gamma']
        param.coef0 = kernel_config[j]['coef0']
        param.eps = kernel_config[j]['eps']
        model = svm.svm_train(problem, param)
        training_labels, training_accuracy, training_values = svm.svm_predict(Y_training, X_training, model,'-q')
        test_labels, test_accuracy, test_values = svm.svm_predict(Y_test, X_test, model,'-q')
        nSV = len(model.get_SV())
        task_2_results[i].append([kernel_codes[kernel_config[j]['kernel_type']], kernel_config[j]['degree'],
                                  kernel_config[j]['gamma'], kernel_config[j]['coef0'],
                                  kernel_config[j]['eps'], round(training_accuracy[0], 3),
                                  round(test_accuracy[0], 3), nSV])
        task_3_results[index].append(nSV)
        support_vector_indices = model.get_sv_indices()
        non_support_vector_indices = [i for i in range(1,151) if i not in support_vector_indices]
        support_vector_candidates[i].append(random.choice(support_vector_indices))
        if len(non_support_vector_indices) == 0:
            non_support_vector_candidates[i].append(None)
        else:
            non_support_vector_candidates[i].append(random.choice(non_support_vector_indices))


#
# TASK 2: PLOT
#

for i,current_c in enumerate(svm_cost_config):
    utils.results_per_c_plot(task_2_results[i], current_c, mode = 1)

#
# TASK 3
#
utils.kernel_vs_c_plot(task_3_results, svm_cost_config)

#
# TASK 4
#
task_4_results_SV = []
task_4_results_NSV = []

for i in range(len(svm_cost_config)):
    task_4_results_SV.append([])
    task_4_results_NSV.append([])

#
#SUPPORT VECTOR REMOVAL
#
for i,current_c in enumerate(svm_cost_config):
    param.C = current_c
    for index,j in enumerate(kernel_config.keys()):
        X, Y = utils.remove_sample(X_training, Y_training, support_vector_candidates[i][index])
        param = svm.svm_parameter('-q')
        problem = svm.svm_problem(Y, X)
        param.kernel_type = kernel_config[j]['kernel_type']
        param.degree = kernel_config[j]['degree']
        param.gamma = kernel_config[j]['gamma']
        param.coef0 = kernel_config[j]['coef0']
        param.eps = kernel_config[j]['eps']
        model = svm.svm_train(problem, param)
        training_labels, training_accuracy, training_values = svm.svm_predict(Y, X, model,'-q')
        test_labels, test_accuracy, test_values = svm.svm_predict(Y_test, X_test, model,'-q')
        nSV = len(model.get_SV())
        task_4_results_SV[i].append([kernel_codes[kernel_config[j]['kernel_type']], kernel_config[j]['degree'],
                                  kernel_config[j]['gamma'], kernel_config[j]['coef0'],
                                  kernel_config[j]['eps'], round(training_accuracy[0], 3),
                                  round(test_accuracy[0], 3), nSV, support_vector_candidates[i][index]])
#
#NONSUPPORT VECTOR REMOVAL
#
for i,current_c in enumerate(svm_cost_config):
    param.C = current_c
    for index,j in enumerate(kernel_config.keys()):
        X, Y = utils.remove_sample(X_training, Y_training, non_support_vector_candidates[i][index])
        param = svm.svm_parameter('-q')
        problem = svm.svm_problem(Y, X)
        param.kernel_type = kernel_config[j]['kernel_type']
        param.degree = kernel_config[j]['degree']
        param.gamma = kernel_config[j]['gamma']
        param.coef0 = kernel_config[j]['coef0']
        param.eps = kernel_config[j]['eps']
        model = svm.svm_train(problem, param)
        training_labels, training_accuracy, training_values = svm.svm_predict(Y, X, model,'-q')
        test_labels, test_accuracy, test_values = svm.svm_predict(Y_test, X_test, model,'-q')
        nSV = len(model.get_SV())
        task_4_results_NSV[i].append([kernel_codes[kernel_config[j]['kernel_type']], kernel_config[j]['degree'],
                                  kernel_config[j]['gamma'], kernel_config[j]['coef0'],
                                  kernel_config[j]['eps'], round(training_accuracy[0], 3),
                                  round(test_accuracy[0], 3), nSV, non_support_vector_candidates[i][index]])


#
# TASK 4: PLOT
#
for i,current_c in enumerate(svm_cost_config):
    utils.results_per_c_plot(task_4_results_SV[i], current_c, mode = 2)
    utils.results_per_c_plot(task_4_results_NSV[i], current_c, mode = 3)

#
#BONUS TASK
#
#
#Toy Example
#
X_toy = np.array([[0.0,0.0],[2.0,2.0],[2.0,0.0],[3.0,0.0]])
Y_toy = np.array([-1.0,-1.0,1.0,1.0])
P_toy, Q_toy, G_toy, H_toy = utils.get_qp_params(X_toy, Y_toy)
P_toy, Q_toy, G_toy, H_toy = cvxopt.matrix(P_toy),cvxopt.matrix(Q_toy),cvxopt.matrix(G_toy),cvxopt.matrix(H_toy)
solution_toy = cvxopt.solvers.qp(P=P_toy, q=Q_toy, G=G_toy, h=H_toy)
print(solution_toy['x'])