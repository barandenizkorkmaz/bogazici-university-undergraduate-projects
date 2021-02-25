import math

import model_utils

"""
Computes mutual information value for a word.
"""
def computeMI(n_00:int, n_01:int, n_10:int, n_11:int, N:int) -> float:
    MI = 0.0
    if n_00 != 0:
        MI += (float(n_00)/N) * math.log(((float(n_00)/N)/(float(n_00+n_01)/N)*float(n_00+n_10)/N),2)
    if n_01 != 0:
        MI += (float(n_01)/N) * math.log(((float(n_01)/N)/(float(n_00+n_01)/N)*float(n_01+n_11)/N),2)
    if n_10 != 0:
        MI += (float(n_10) / N) * math.log(((float(n_10) / N) / (float(n_10 + n_11) / N) * float(n_00 + n_10) / N), 2)
    if n_11 != 0:
        MI += (float(n_11) / N) * math.log(((float(n_11) / N) / (float(n_10 + n_11) / N) * float(n_01 + n_11) / N), 2)
    return MI

"""
Computes mutual information value for every word in a vocabulary.
Returns:
    dict:
        Key: word
        Value: Mutual Information Value
"""
def computeVocabularyMI(corpus:dict, vocabulary:list) -> dict:
    vocabularyMI = dict()
    totalNumDocuments = model_utils.getNumDocuments(corpus)
    for token in vocabulary:
        n_00 = 0
        n_01 = 0
        n_10 = 0
        n_11 = 0
        for label, docs in corpus.items():
            for doc in docs:
                contains = 1 if token in doc.split() else 0
                if label == 0:
                    if contains == 1:
                        n_10 += 1
                    else:
                        n_00 += 1
                else:
                    if contains == 1:
                        n_11 += 1
                    else:
                        n_01 += 1
        MI = computeMI(n_00,n_01,n_10,n_11,totalNumDocuments)
        vocabularyMI[token] = MI
    return vocabularyMI

"""
Returns the top K (by default 100) words that has the highest mutual information values.
"""
def selectFeatures(vocabularyMI:dict, K = 100) -> list:
    vocabulary = list()
    results = list()
    for word, MI in vocabularyMI.items():
        results.append([word,MI])
    results.sort(key=lambda x: x[1],reverse=True)
    for i in range(K):
        vocabulary.append(results[i][0])
    return vocabulary