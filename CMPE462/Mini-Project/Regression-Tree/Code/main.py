import numpy as np
from sklearn.datasets import load_boston
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

import data_handler
import regression_tree_utils
import plot_utils

# Task 1: Dataset
boston = load_boston()
DATA = np.column_stack([boston['data'], boston['target']])
np.random.seed(85)
np.random.shuffle(DATA)
xData, yData = DATA[:,:-1], DATA[:,-1]
xTrain, yTrain = xData[:400], yData[:400]
xTest, yTest = xData[400:], yData[400:]
del xData, yData, DATA

training_data = data_handler.form_data(xTrain,yTrain)
test_data = data_handler.form_data(xTest,yTest)
feature_labels = np.concatenate((boston['feature_names'],['Target']))
feature_names = boston['feature_names']
feature_index = data_handler.feature_index(feature_names)

corr_matrix = np.corrcoef(training_data.T)
plt.figure()
sns.heatmap(corr_matrix, vmin=-1, vmax=1, xticklabels=feature_labels,yticklabels=feature_labels)
plt.show()

# Task 2: Regression Tree
# 2.1 Feature Analysis
regression_tree_utils.find_split_by_feature(feature_index['B'],training_data,True,feature_labels)
regression_tree_utils.find_split_by_feature(feature_index['LSTAT'],training_data,True,feature_labels)

# 2.2 & 2.3 Implementing Regression Tree
initial_tree = regression_tree_utils.train_tree(training_data,1,3)
yTrainPredicted_Init, yTest_Predicted_Init = regression_tree_utils.predict(initial_tree,training_data) ,regression_tree_utils.predict(initial_tree,test_data)
plot_utils.r2_plots([r2_score(yTrain,yTrainPredicted_Init)],[r2_score(yTest,yTest_Predicted_Init)],[3])

# Task 3: Evaluation
# 3.1 Cross Validation
depth_levels = [3,4,5,6,7,8,9,10]
b_depth,mean_r2,std_r2 = regression_tree_utils.cross_validation(data=training_data,s=5,depths=depth_levels)
plot_utils.cross_validation_plot(depth_levels,mean_r2,std_r2)

# 3.2 Final Tree
final_tree = regression_tree_utils.train_tree(training_data,1,b_depth)
yTrain_Predicted_Final, yTest_Predicted_Final = regression_tree_utils.predict(final_tree,training_data), regression_tree_utils.predict(final_tree,test_data)
plot_utils.r2_plots([r2_score(yTrain,yTrain_Predicted_Final)],[r2_score(yTest,yTest_Predicted_Final)],[b_depth])

# APPENDIX
# A.1
r2_training, r2_test = list(),list()
for depth in depth_levels:
    tree = regression_tree_utils.train_tree(training_data,1,depth)
    yTrain_Predicted = regression_tree_utils.predict(tree, training_data)
    yTest_Predicted = regression_tree_utils.predict(tree, test_data)
    r2_training.append(r2_score(yTrain,yTrain_Predicted))
    r2_test.append(r2_score(yTest, yTest_Predicted))
plot_utils.r2_plots(r2_training,r2_test,depth_levels)