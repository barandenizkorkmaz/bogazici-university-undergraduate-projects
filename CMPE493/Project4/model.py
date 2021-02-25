import math

import evaluation_utils

# Class definition for Multinomial Naive Bayes model.
class Model():
    # A model holds the precomputed priorProbability and conditionalProbability values given an extracted vocabulary.
    def __init__(self, id:int, priorProbabilities:dict, conditionalProbabilities:dict):
        self.id = id
        self.priorProbabilities = priorProbabilities
        self.conditionalProbabilities = conditionalProbabilities

    # Returns the class prediciton for a document based on class probability values computed for different classes.
    def getClassPrediction(self, classProbabilities: dict) -> int:
        prediction = -1
        maxProbability = -math.inf
        for label, probability in classProbabilities.items():
            if probability > maxProbability:
                prediction = label
                maxProbability = probability
        return prediction

    # Predict the labels for a test set based on an extracted vocabulary.
    def predict(self, test: list, vocabulary) -> tuple:
        #
        # Apply data preprocessing on the test set if you performed any data preprocessing in training data...
        #
        classProbabilities = dict()
        classPredictions = list()
        for i, doc in enumerate(test):
            classProbabilities[i] = dict()
            for label in self.priorProbabilities:
                priorProbability = self.priorProbabilities[label]
                result = 0.0
                result += math.log(priorProbability, 10)
                for word in doc.split():
                    if word in vocabulary:
                        result += math.log(self.conditionalProbabilities[label][word],10)
                classProbabilities[i][label] = result
            classPredictions.append(self.getClassPrediction(classProbabilities[i]))
        return classProbabilities, classPredictions

    # Evaluates the performance of model in terms of precision, recall, and f-measure.
    def evaluate(self,actual:list,predicted:list):
        print("\nEvaluation Results for Model ID: {}\n".format(self.id))
        CLASSES = {
            "legitimate": 0,
            "spam": 1
        }
        avgPrecision, precisions = evaluation_utils.precision(actual,predicted)
        avgRecall, recalls = evaluation_utils.recall(actual,predicted)
        avgF1Score, f1Scores = evaluation_utils.f1_score(actual, predicted)
        for key, label in CLASSES.items():
            print("Performance Metrics\nClass: {}\nPrecision: {}\nRecall: {}\nF-Measure: {}\n".format(key,precisions[label],recalls[label],f1Scores[label]))
        print("Macro-Averaged Performance Metrics\nPrecision: {}\nRecall: {}\nF-Measure: {}\n".format(avgPrecision,avgRecall,avgF1Score))