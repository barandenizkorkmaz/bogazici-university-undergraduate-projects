import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as LA
from mpl_toolkits.mplot3d import Axes3D
import math
import datetime

import data_handler
import log_reg_utils
import feature_extraction_utils
import plot_utils

#CONSTANTS
MATRIX_SIZE=16

TRAINING_DATA = np.load('train_data.npy')
TRAINING_DATA = [np.reshape(element, (MATRIX_SIZE,MATRIX_SIZE)) for element in TRAINING_DATA]
Y_TRAINING = np.load('train_labels.npy')

TEST_DATA = np.load('test_data.npy')
TEST_DATA = [np.reshape(element, (MATRIX_SIZE,MATRIX_SIZE)) for element in TEST_DATA]
Y_TEST = np.load('test_labels.npy')

#TASK 1: FEATURE EXTRACTION

#1.1

DIGIT_1 = TRAINING_DATA[6]
DIGIT_5 = TRAINING_DATA[-4]
plot_utils.show_images(DIGIT_1,DIGIT_5)

#1.2 REPRESENTATION 1
INTENSITY_TRAINING = [np.average(element) for element in TRAINING_DATA]
INTENSITY_TEST = [np.average(element) for element in TEST_DATA]

SYMMETRY_Y_TRAINING = [-1*LA.norm(np.subtract(element,np.flip(element,1)),'fro') for element in TRAINING_DATA]
SYMMETRY_Y_TEST = [-1*LA.norm(np.subtract(element,np.flip(element,1)),'fro') for element in TEST_DATA]

FEATURES_REP_1_TRAINING = [INTENSITY_TRAINING,SYMMETRY_Y_TRAINING]
FEATURES_REP_1_TEST = [INTENSITY_TEST,SYMMETRY_Y_TEST]

#1.3
#Reference:https://stackoverflow.com/questions/41099887/conditional-marker-matplotlib
fig = plt.figure()
ax = fig.add_subplot(121)
positive_class_training,negative_class_training = data_handler.scatter_plot_helper(Y_TRAINING,FEATURES_REP_1_TRAINING)
ax.scatter(positive_class_training[0], positive_class_training[1], c='b', marker='o',label='Positive Class')
ax.scatter(negative_class_training[0], negative_class_training[1], c='r', marker='x',label='Negative Class')
ax.set_xlabel('Intensity')
ax.set_ylabel('Symmetry About y-Axis')
plt.title("Scatter Plot for Training Data")
ax.legend()
ax = fig.add_subplot(122)
positive_class_test,negative_class_test = data_handler.scatter_plot_helper(Y_TEST,FEATURES_REP_1_TEST)
ax.scatter(positive_class_test[0], positive_class_test[1], c='b', marker='o',label='Positive Class')
ax.scatter(negative_class_test[0], negative_class_test[1], c='r', marker='x',label='Negative Class')
ax.set_xlabel('Intensity')
ax.set_ylabel('Symmetry About y-Axis')
plt.title("Scatter Plot for Test Data")
ax.legend()
plt.show()

#1.4 REPRESENTATION 2

#NOTE: DO WE NEED 3 2-D Scatter Plots and 1 3-D Scatter Plot?

DARKNESS_TRAINING = [feature_extraction_utils.darkness_distribution_analysis(element) for element in TRAINING_DATA]
DARKNESS_TEST = [feature_extraction_utils.darkness_distribution_analysis(element) for element in TEST_DATA]

BRIGHTNESS_TRAINING = [feature_extraction_utils.brightness_distribution_analysis(element) for element in TRAINING_DATA]
BRIGHTNESS_TEST = [feature_extraction_utils.brightness_distribution_analysis(element) for element in TEST_DATA]

SYMMETRY_X_TRAINING = [-1*LA.norm(np.subtract(element,np.flip(element,0)),'fro') for element in TRAINING_DATA]
SYMMETRY_X_TEST = [-1*LA.norm(np.subtract(element,np.flip(element,0)),'fro') for element in TEST_DATA]

FEATURES_REP_2_TRAINING = [SYMMETRY_X_TRAINING,BRIGHTNESS_TRAINING,DARKNESS_TRAINING]
FEATURES_REP_2_TEST = [SYMMETRY_X_TEST,BRIGHTNESS_TEST,DARKNESS_TEST]

#
# 3D Plot
#

fig = plt.figure(figsize=plt.figaspect(0.5))
ax = fig.add_subplot(121,projection='3d')
positive_class_training,negative_class_training = data_handler.scatter_plot_helper(Y_TRAINING,FEATURES_REP_2_TRAINING)
ax.scatter(positive_class_training[0], positive_class_training[1], positive_class_training[2], c='b', marker='o',label='Positive Class')
ax.scatter(negative_class_training[0], negative_class_training[1], negative_class_training[2], c='r', marker='x',label='Negative Class')
ax.set_xlabel('Sym-x')
ax.set_ylabel('Brightness')
ax.set_zlabel('Darkness')
plt.title("Scatter Plot for Training Data")
ax.legend()
ax = fig.add_subplot(122,projection='3d')
positive_class_test,negative_class_test = data_handler.scatter_plot_helper(Y_TEST,FEATURES_REP_2_TEST)
ax.scatter(positive_class_test[0], positive_class_test[1], positive_class_test[2], c='b', marker='o',label='Positive Class')
ax.scatter(negative_class_test[0], negative_class_test[1], negative_class_test[2], c='r', marker='x',label='Negative Class')
ax.set_xlabel('Sym-x')
ax.set_ylabel('Brightness')
ax.set_zlabel('Darkness')
plt.title("Scatter Plot for Test Data")
ax.legend()
plt.show()


#
# CORRELATION ANALYSIS FOR REPRESENTATION 1
#
fig, ax = plt.subplots()
x = np.arange(1)
cor_rep_1_train = np.array([np.corrcoef(FEATURES_REP_1_TRAINING[0],FEATURES_REP_1_TRAINING[1])[0][1]])
cor_rep_1_test = np.array([np.corrcoef(FEATURES_REP_1_TEST[0],FEATURES_REP_1_TEST[1])[0][1]])
#Rounding
cor_rep_1_train_rounded = [round(elem, 3) for elem in cor_rep_1_train]
cor_rep_1_test_rounded = [round(elem, 3) for elem in cor_rep_1_test]
#Rounding
width = 0.2  # the width of the bars
rects1 = ax.bar(x - width / 2, cor_rep_1_train_rounded, width, label='Rep. 1 Training Data')
rects2 = ax.bar(x + width / 2, cor_rep_1_test_rounded, width, label='Rep. 1 Test Data')
ax.set_ylabel('Correlation')
ax.set_title('Correlation Analysis of Features for Representation 1')
ax.set_xticks(x)
ax.set_xticklabels(['Intensity vs Symmetry About y-Axis'])
ax.legend()
plot_utils.autolabel(rects1, ax)
plot_utils.autolabel(rects2, ax)
fig.tight_layout()
plt.show()

#
# CORRELATION ANALYSIS FOR REPRESENTATION 2
#
fig, ax = plt.subplots()
x = np.arange(3)
cor_rep_2_train = np.array([np.corrcoef(FEATURES_REP_2_TRAINING[0],FEATURES_REP_2_TRAINING[1])[0][1],np.corrcoef(FEATURES_REP_2_TRAINING[0],FEATURES_REP_2_TRAINING[2])[0][1],np.corrcoef(FEATURES_REP_2_TRAINING[1],FEATURES_REP_2_TRAINING[2])[0][1]])
cor_rep_2_test = np.array([np.corrcoef(FEATURES_REP_2_TEST[0],FEATURES_REP_2_TEST[1])[0][1],np.corrcoef(FEATURES_REP_2_TEST[0],FEATURES_REP_2_TEST[2])[0][1],np.corrcoef(FEATURES_REP_2_TEST[1],FEATURES_REP_2_TEST[2])[0][1]])
#Rounding
cor_rep_2_train_rounded = [round(elem, 3) for elem in cor_rep_2_train]
cor_rep_2_test_rounded = [round(elem, 3) for elem in cor_rep_2_test]
#Rounding
width = 0.2  # the width of the bars
rects1 = ax.bar(x - width / 2, cor_rep_2_train_rounded, width, label='Rep. 2 Training Data')
rects2 = ax.bar(x + width / 2, cor_rep_2_test_rounded, width, label='Rep. 2 Test Data')
ax.set_ylabel('Correlation')
ax.set_title('Correlation Analysis of Features for Representation 2')
ax.set_xticks(x)
ax.set_xticklabels(['Sym-x vs Brightness','Sym-x vs Darkness','Brightness vs Darkness'])
ax.legend()
plot_utils.autolabel(rects1, ax)
plot_utils.autolabel(rects2, ax)
fig.tight_layout()
plt.show()

"""
#TASK2: LOGISTIC REGRESSION
"""

"""
#2.1 Implementing the Logistic Regression.
"""

# Forming the training and test data for Rep 1 and Rep 2.
X_TRAINING_REP_1 = data_handler.form_input_data(FEATURES=FEATURES_REP_1_TRAINING)
X_TEST_REP_1 = data_handler.form_input_data(FEATURES=FEATURES_REP_1_TEST)

X_TRAINING_REP_2 = data_handler.form_input_data(FEATURES=FEATURES_REP_2_TRAINING)
X_TEST_REP_2 = data_handler.form_input_data(FEATURES=FEATURES_REP_2_TEST)
LEARNING_RATES_REP_1 = [0.001,0.005,0.01,0.05,0.12]
LEARNING_RATES_REP_2 = [0.001,0.005,0.01,0.05,0.12]
#
# REPRESENTATION 1
#


_,WEIGHTS_REP_1,ERRORS_REP_1,ITERATION_COUNTS_REP_1 = log_reg_utils.logistic_regression_manager(X=X_TRAINING_REP_1,Y=Y_TRAINING,LEARNING_RATES=LEARNING_RATES_REP_1,LAMBDA=None)
#
# PLOT: E(w) vs Time During Iterations
#
plot_utils.error_vs_time_visualization(LEARNING_RATES_REP_1,ERRORS_REP_1,ITERATION_COUNTS_REP_1,"Representation 1","LR")

#
# PLOT: E(w) vs W During Iterations
#

plot_utils.error_vs_w_3d_visualization(ERRORS_REP_1,WEIGHTS_REP_1,LEARNING_RATES_REP_1,"Representation 1","LR")

#
# Accuracy Plots for REPRESENTATION 1
#
W_OPTIMAL_REP_1,LEARNING_RATE_OPTIMAL_REP_1 = log_reg_utils.get_optimal_weights(X_TRAINING_REP_1,X_TEST_REP_1,Y_TRAINING,Y_TEST,WEIGHTS_REP_1,LEARNING_RATES_REP_1,'Representation 1','LR')

Y_Predicted_Training_REP_1 = log_reg_utils.predict(X_TRAINING_REP_1,W_OPTIMAL_REP_1)
Y_Predicted_Test_REP_1 = log_reg_utils.predict(X_TEST_REP_1,W_OPTIMAL_REP_1)

Accuracy_Training_REP_1 = log_reg_utils.accuracy_score(Y_TRAINING,Y_Predicted_Training_REP_1)
Accuracy_Test_REP_1 = log_reg_utils.accuracy_score(Y_TEST,Y_Predicted_Test_REP_1)

plot_utils.accuracy_plots([Accuracy_Training_REP_1],[Accuracy_Test_REP_1],[LEARNING_RATE_OPTIMAL_REP_1],'Representation 1',"LR")


#
# REPRESENTATION 2
#


_,WEIGHTS_REP_2,ERRORS_REP_2,ITERATION_COUNTS_REP_2 = log_reg_utils.logistic_regression_manager(X=X_TRAINING_REP_2,Y=Y_TRAINING,LEARNING_RATES=LEARNING_RATES_REP_2,LAMBDA=None)
#
# PLOT: E(w) vs Time During Iterations
#
plot_utils.error_vs_time_visualization(LEARNING_RATES_REP_2,ERRORS_REP_2,ITERATION_COUNTS_REP_2,"Representation 2","LR")
#
# PLOT: E(w) vs W During Iterations
#

plot_utils.error_vs_w_3d_visualization(ERRORS_REP_2,WEIGHTS_REP_2,LEARNING_RATES_REP_2,"Representation 2","LR")
#
# Accuracy Plots for REPRESENTATION 2
#
W_OPTIMAL_REP_2,LEARNING_RATE_OPTIMAL_REP_2 = log_reg_utils.get_optimal_weights(X_TRAINING_REP_2,X_TEST_REP_2,Y_TRAINING,Y_TEST,WEIGHTS_REP_2,LEARNING_RATES_REP_2,'Representation 2','LR')
Y_Predicted_Training_REP_2 = log_reg_utils.predict(X_TRAINING_REP_2,W_OPTIMAL_REP_2)
Y_Predicted_Test_REP_2 = log_reg_utils.predict(X_TEST_REP_2,W_OPTIMAL_REP_2)

Accuracy_Training_REP_2 = log_reg_utils.accuracy_score(Y_TRAINING,Y_Predicted_Training_REP_2)
Accuracy_Test_REP_2 = log_reg_utils.accuracy_score(Y_TEST,Y_Predicted_Test_REP_2)

plot_utils.accuracy_plots([Accuracy_Training_REP_2],[Accuracy_Test_REP_2],[LEARNING_RATE_OPTIMAL_REP_2],'Representation 2',"LR")


#
# 2.2 Regularization
#
#REGULARIZATION for REPRESENTATION 1
LEARNING_RATE_REP_1_REG = 0.05
LAMBDA_LIST_1 = [0,0.5,0.05,0.005,0.0005]
W_OPTIMAL_REP_1_REG,WEIGHTS_REP_1_REG,ERRORS_REP_1_REG,ITERATION_COUNTS_REP_1_REG = log_reg_utils.regularization_manager(X=X_TRAINING_REP_1,Y=Y_TRAINING,LEARNING_RATE=LEARNING_RATE_REP_1_REG,LAMBDA_LIST=LAMBDA_LIST_1)
plot_utils.error_vs_time_visualization(LAMBDA_LIST_1,ERRORS_REP_1_REG,ITERATION_COUNTS_REP_1_REG,"Representation 1 by Regularization","Lambda")
plot_utils.error_vs_w_3d_visualization(ERRORS_REP_1_REG,WEIGHTS_REP_1_REG,LAMBDA_LIST_1,"Representation 1 by Regularization","Lambda")
#Accuracy for REP 1 by Regularization
W_OPTIMAL_REP_1_REG,LAMBDA_OPTIMAL_REP_1_REG = log_reg_utils.get_optimal_weights(X_TRAINING_REP_1,X_TEST_REP_1,Y_TRAINING,Y_TEST,WEIGHTS_REP_1_REG,LAMBDA_LIST_1,'Representation 1 by Regularization','Lambda')
Y_Predicted_Training_REP_1_REG = log_reg_utils.predict(X_TRAINING_REP_1,W_OPTIMAL_REP_1_REG)
Y_Predicted_Test_REP_1_REG = log_reg_utils.predict(X_TEST_REP_1,W_OPTIMAL_REP_1_REG)

Accuracy_Training_REP_1_REG = log_reg_utils.accuracy_score(Y_TRAINING,Y_Predicted_Training_REP_1_REG)
Accuracy_Test_REP_1_REG = log_reg_utils.accuracy_score(Y_TEST,Y_Predicted_Test_REP_1_REG)

plot_utils.accuracy_plots([Accuracy_Training_REP_1_REG],[Accuracy_Test_REP_1_REG],[LAMBDA_OPTIMAL_REP_1_REG],'Representation 1 by Regularization',"Lambda")



#REGULARIZATION for REPRESENTATION 2
LEARNING_RATE_REP_2_REG = 0.05
LAMBDA_LIST_2 = [0,0.5,0.05,0.005,0.0005]
W_OPTIMAL_REP_2_REG,WEIGHTS_REP_2_REG,ERRORS_REP_2_REG,ITERATION_COUNTS_REP_2_REG = log_reg_utils.regularization_manager(X=X_TRAINING_REP_2,Y=Y_TRAINING,LEARNING_RATE=LEARNING_RATE_REP_2_REG,LAMBDA_LIST=LAMBDA_LIST_2)
plot_utils.error_vs_time_visualization(LAMBDA_LIST_2,ERRORS_REP_2_REG,ITERATION_COUNTS_REP_2_REG,"Representation 2 by Regularization","Lambda")
plot_utils.error_vs_w_3d_visualization(ERRORS_REP_2_REG,WEIGHTS_REP_2_REG,LAMBDA_LIST_2,"Representation 2 by Regularization","Lambda")
#Accuracy for REP 2 by Regularization
W_OPTIMAL_REP_2_REG,LAMBDA_OPTIMAL_REP_2_REG = log_reg_utils.get_optimal_weights(X_TRAINING_REP_2,X_TEST_REP_2,Y_TRAINING,Y_TEST,WEIGHTS_REP_2_REG,LAMBDA_LIST_2,'Representation 2 by Regularization','Lambda')
Y_Predicted_Training_REP_2_REG = log_reg_utils.predict(X_TRAINING_REP_2,W_OPTIMAL_REP_2_REG)
Y_Predicted_Test_REP_2_REG = log_reg_utils.predict(X_TEST_REP_2,W_OPTIMAL_REP_2_REG)

Accuracy_Training_REP_2_REG = log_reg_utils.accuracy_score(Y_TRAINING,Y_Predicted_Training_REP_2_REG)
Accuracy_Test_REP_2_REG = log_reg_utils.accuracy_score(Y_TEST,Y_Predicted_Test_REP_2_REG)

plot_utils.accuracy_plots([Accuracy_Training_REP_2_REG],[Accuracy_Test_REP_2_REG],[LAMBDA_OPTIMAL_REP_2_REG],'Representation 2 by Regularization','Lambda')

#
# 2.3 Cross Validation
#

LAMBDA_OPTIMAL_REP_1 = log_reg_utils.cross_validation_manager(X_TRAINING_REP_1,Y_TRAINING,s=5, lambda_list=[0, 0.1, 0.01, 0.05, 0.001, 0.005], mode=False, representation ="Representation 1")
LAMBDA_OPTIMAL_REP_2 = log_reg_utils.cross_validation_manager(X_TRAINING_REP_2,Y_TRAINING,s=5, lambda_list=[0, 0.1, 0.01, 0.05, 0.001, 0.005], mode=False, representation ="Representation 2")
#
#TASK3: EVALUATION
#
#
#3.1 Accuracy Analysis
#
#
# REPRESENTATION 1
#

_,WEIGHTS_REP_1,ERRORS_REP_1,ITERATION_COUNTS_REP_1 = log_reg_utils.logistic_regression_manager(X=X_TRAINING_REP_1,Y=Y_TRAINING,LEARNING_RATES=LEARNING_RATES_REP_1,LAMBDA=LAMBDA_OPTIMAL_REP_1)
#
# Accuracy Plots for REPRESENTATION 1
#
W_OPTIMAL_REP_1,LEARNING_RATE_OPTIMAL_REP_1 = log_reg_utils.get_optimal_weights(X_TRAINING_REP_1,X_TEST_REP_1,Y_TRAINING,Y_TEST,WEIGHTS_REP_1,LEARNING_RATES_REP_1,'Representation 1 Final','LR')
Y_Predicted_Training_REP_1 = log_reg_utils.predict(X_TRAINING_REP_1,W_OPTIMAL_REP_1)
Y_Predicted_Test_REP_1 = log_reg_utils.predict(X_TEST_REP_1,W_OPTIMAL_REP_1)

Accuracy_Training_REP_1 = log_reg_utils.accuracy_score(Y_TRAINING,Y_Predicted_Training_REP_1)
Accuracy_Test_REP_1 = log_reg_utils.accuracy_score(Y_TEST,Y_Predicted_Test_REP_1)

plot_utils.accuracy_plots([Accuracy_Training_REP_1],[Accuracy_Test_REP_1],[LEARNING_RATE_OPTIMAL_REP_1],'Representation 1 Final','LR')

#
# REPRESENTATION 2
#
_,WEIGHTS_REP_2,ERRORS_REP_2,ITERATION_COUNTS_REP_2 = log_reg_utils.logistic_regression_manager(X=X_TRAINING_REP_2,Y=Y_TRAINING,LEARNING_RATES=LEARNING_RATES_REP_2,LAMBDA=LAMBDA_OPTIMAL_REP_2)
#
# Accuracy Plots for REPRESENTATION 2
#
W_OPTIMAL_REP_2,LEARNING_RATE_OPTIMAL_REP_2 = log_reg_utils.get_optimal_weights(X_TRAINING_REP_2,X_TEST_REP_2,Y_TRAINING,Y_TEST,WEIGHTS_REP_2,LEARNING_RATES_REP_2,'Representation 2','LR')
Y_Predicted_Training_REP_2 = log_reg_utils.predict(X_TRAINING_REP_2,W_OPTIMAL_REP_2)
Y_Predicted_Test_REP_2 = log_reg_utils.predict(X_TEST_REP_2,W_OPTIMAL_REP_2)

Accuracy_Training_REP_2 = log_reg_utils.accuracy_score(Y_TRAINING,Y_Predicted_Training_REP_2)
Accuracy_Test_REP_2 = log_reg_utils.accuracy_score(Y_TEST,Y_Predicted_Test_REP_2)

plot_utils.accuracy_plots([Accuracy_Training_REP_2],[Accuracy_Test_REP_2],[LEARNING_RATE_OPTIMAL_REP_2],'Representation 2 Final','LR')

#
#3.2 Visualization of Decision Boundary
#
#
# REPRESENTATION 1
#

slope_line = -1 * W_OPTIMAL_REP_1[0][1] / W_OPTIMAL_REP_1[0][2]
intercept = -1 * W_OPTIMAL_REP_1[0][0] / W_OPTIMAL_REP_1[0][2]

fig = plt.figure()
ax = fig.add_subplot(121)
line_training = np.add(np.multiply(INTENSITY_TRAINING,slope_line), intercept)
plt.plot(INTENSITY_TRAINING,line_training,'r')
positive_class_training,negative_class_training = data_handler.scatter_plot_helper(Y_TRAINING,FEATURES_REP_1_TRAINING)
ax.scatter(positive_class_training[0], positive_class_training[1], c='b', marker='o',label='Positive Class')
ax.scatter(negative_class_training[0], negative_class_training[1], c='r', marker='x',label='Negative Class')
ax.set_xlabel('Intensity')
ax.set_ylabel('Symmetry About y-Axis')
plt.title("Scatter Plot for Training Data")
ax.legend()
ax = fig.add_subplot(122)
line_test = np.add(np.multiply(INTENSITY_TEST,slope_line), intercept)
plt.plot(INTENSITY_TEST,line_test,'r')
positive_class_test,negative_class_test = data_handler.scatter_plot_helper(Y_TEST,FEATURES_REP_1_TEST)
ax.scatter(positive_class_test[0], positive_class_test[1], c='b', marker='o',label='Positive Class')
ax.scatter(negative_class_test[0], negative_class_test[1], c='r', marker='x',label='Negative Class')
ax.set_xlabel('Intensity')
ax.set_ylabel('Symmetry About y-Axis')
plt.title("Scatter Plot for Test Data")
ax.legend()
plt.show()