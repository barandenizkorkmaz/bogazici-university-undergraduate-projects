import queryUtils

"""
Returns the dictionary of recommendations for URL keys.
Input: Dict (METADATA)
    {
            'URL' : {
            'TITLE': str,
            'AUTHORS': list(str),
            'DESC': str
            'RECOMMENDATIONS': list(tuple(name,url))
            'GENRES': list(str)
        },
    ...
    }

Output: Dict (CORPUS)
    {
        'URL' : {
            'RECOMMENDATIONS': list(url)
        },
        ...
    }
"""
def getGoodreadsRecommendations(metadata:dict) -> dict:
    recommendations = dict()
    for url in metadata:
        recommendations[url] = metadata[url]['RECOMMENDATIONS']
    return recommendations

# Evaluates the current query results.
def evaluate(predictedRecommendations:dict, actualRecommendations:dict):
    numQueries = len(predictedRecommendations)
    precisionDict = dict()
    averagePrecisionAtNDict = dict()
    for queryUrl in predictedRecommendations:
        predicted = predictedRecommendations[queryUrl]
        actual = actualRecommendations[queryUrl]
        precisionDict[queryUrl] = computePrecision(predicted,actual)
        averagePrecisionAtNDict[queryUrl] = computeAveragePrecisionAtN(predicted,actual)
    precision = sum(precisionDict.values())/numQueries
    averagePrecisionAtNDict = sum(averagePrecisionAtNDict.values())/numQueries
    return precision, averagePrecisionAtNDict

# Computes precision.
def computePrecision(predicted:list, actual:list) -> float:
    numRelevantRecommendations = len(set(predicted).intersection(set(actual)))
    numOfRecommendations = len(predicted)
    return float(numRelevantRecommendations)/numOfRecommendations

# Computes AP@N where N is 18 in our system.
def computeAveragePrecisionAtN(predicted:list ,actual: list) -> float:
    precisions = list()
    m = len(set(predicted).intersection(set(actual)))
    if m == 0:
        return 0.0
    N = len(predicted)
    for i in range(N):
        if predicted[i] in actual:
            currentPrecision = computePrecision(predicted[:i+1],actual)
            precisions.append(currentPrecision)
    verify = (m == len(precisions))
    #print("computeAveragePrecisionAtN correctly implemented? ",verify)
    return sum(precisions)/m

# Prints the recommendations for a query.
def printRecommendations(recommendations:dict,desc:str):
    for key, recommendationsList in recommendations.items():
        print("{} Recommendations For: {}".format(desc,key))
        for i, url in enumerate(recommendationsList):
            print("{}: {}".format(i+1,url))

# Prints the common recommendations in actual and predicted recommendations.
# This function has been written for testing purposes.
def printCommonRecommendations(actualRecommendations:dict,predictedRecommendations:dict):
    for key, recommendationsList in predictedRecommendations.items():
        print(key)
        for elem in recommendationsList:
            if elem in actualRecommendations[key]:
                print(elem)

# Prints the evaluation results for different predetermined set of alpha values.
def crossValidation(queryBookCosineSimilarityDictDesc: dict, queryBookCosineSimilarityDictGenres:dict, actualRecommendations: dict):
    alphas = [0.55,0.575,0.6,0.625,0.65,0.675,0.7]
    for alpha in alphas:
        overallCosineSimilarityDict = queryUtils.getOverallCosineSimilarityResults(queryBookCosineSimilarityDictDesc,
                                                                                   queryBookCosineSimilarityDictGenres,
                                                                                   alpha=alpha)
        predictedRecommendations = queryUtils.getTopKRecommendations(overallCosineSimilarityDict, K=18)
        precision, averagePrecisionAtN = evaluate(predictedRecommendations, actualRecommendations)
        print("Alpha: ",alpha)
        print("Precision: ", precision)
        print("AP@18: ", averagePrecisionAtN)

# Prints the evaluation results.
def printEvaluations(alpha, precision, averagePrecisionAtN, K=18):
    print("\nEVALUATION")
    print("Alpha: {}".format(alpha))
    print("Precision: {}".format(precision))
    print("AP@{}: {}".format(K,averagePrecisionAtN))