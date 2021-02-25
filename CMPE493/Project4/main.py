import data_handler,model_utils, feature_selection, evaluation_utils
from model import Model

print("Importing Training Set")
corpus = data_handler.getCorpus("training")

print("Constructing Vocabulary for Model 1")
vocabulary = data_handler.getVocabulary(corpus)
print("Size of vocabulary when all words are used as features: {}".format(len(vocabulary)))

print("Constructing Vocabulary for Model 2: w/Mutual Information")
vocabulary_2 = feature_selection.selectFeatures(feature_selection.computeVocabularyMI(corpus,vocabulary))
print("The k most discriminating words (where k = 100) based on Mutual Information:")
print(vocabulary_2)

priorProbabilities = model_utils.getPriorProbabilities(corpus)
print("Constructing Model 1: Regular Model")
conditionalProbabilities_1 = model_utils.getConditionalProbabilities(corpus,vocabulary,alpha=1)
print("Constructing Model 2: Model w/Mutual Information")
conditionalProbabilities_2 = model_utils.getConditionalProbabilities(corpus,vocabulary_2,alpha=1)

model_1 = Model(1,priorProbabilities,conditionalProbabilities_1)
model_2 = Model(2,priorProbabilities,conditionalProbabilities_2)

print("Importing Test Set")
test_x, test_y = data_handler.getDataset(data_handler.getCorpus(subset='test'))

print("Model 1 Predicts...")
classProbabilities_1, classPredictions_1 = model_1.predict(test_x,vocabulary)

print("Model 2 Predicts...")
classProbabilities_2, classPredictions_2 = model_2.predict(test_x,vocabulary_2)

# Evaluate the models.
model_1.evaluate(test_y,classPredictions_1)
model_2.evaluate(test_y,classPredictions_2)

p = evaluation_utils.approximateRandomizationTest(y_actual=test_y, y_predicted1= classPredictions_1, y_predicted2= classPredictions_2)