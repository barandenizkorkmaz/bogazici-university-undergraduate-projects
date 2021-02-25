import math
import os
import pickle
import shutil

"""
Constructs vocabulary by corpus that has undergone through data preprocessing.
The dictionary has been constructed either for descriptions or genres.
Returns: List of strings where each value occurs just once and sorted in ascending
order.
"""
def getVocabulary(corpus:dict, key: str) -> list :
    vocabulary = list()
    for url in corpus:
        vocabulary.extend(corpus[url][key])
    setVocabulary = set(vocabulary)
    vocabulary = list(setVocabulary)
    vocabulary.sort()
    return vocabulary
"""
Returns the tuple of dictionaries. While vocabularyTermIndexMapping maps the vocabulary
terms into their indices, vocabularyIndexTermMapping maps vocabulary indices into vocabulary terms
where they are located in the list of vocabulary.
"""
def getVocabularyMappings(vocabulary: list):
    vocabularyTermIndexMapping = dict()
    vocabularyIndexTermMapping = dict()
    for i, word in enumerate(vocabulary):
        vocabularyTermIndexMapping[word] = i
        vocabularyIndexTermMapping[i] = word
    return vocabularyTermIndexMapping, vocabularyIndexTermMapping

"""
Computes TF vectors of length vocabulary for each book by their descriptions or genres.
Please note that the order of terms in TF lists are the same as the order in vocabulary.
Returns: Dict
    TFDict = {
        'url1' : list(TFs) (length = |V|)
        'url2' : list(TFs) (length = |V|)
        ...
        'urlN' : list(TFs) (length = |V|)
    }
"""
def computeTF(corpus: dict, vocabularyTermIndexMapping : dict, key : str) -> dict :
    TFDict = dict()
    for url in corpus:
        TFDict[url] = [0] * len(vocabularyTermIndexMapping.keys())
        for word in corpus[url][key]:
            if word in vocabularyTermIndexMapping:
                TFDict[url][vocabularyTermIndexMapping[word]] += 1
        for i in range(len(TFDict[url])):
            rawTF = TFDict[url][i]
            if rawTF != 0:
                TFDict[url][i] = 1 + math.log(float(rawTF),10)
    return TFDict

"""
Computes IDF values for each term in vocabulary for the descriptions or genres of the books.
Returns: Dict
    IDFDict = {
        'term1' : IDF1,
        'term2' : IDF2,
        ...
        'termN' : IDFN
    }
"""
def computeIDF(corpus: dict, vocabularyTermIndexMapping: dict, key : str) -> dict :
    IDFDict = dict.fromkeys(vocabularyTermIndexMapping.keys(), 0)
    N = len(corpus)
    for url in corpus:
        markedWords = dict()
        for word in corpus[url][key]:
            if word not in markedWords:
                IDFDict[word] += 1
                markedWords[word] = True
    for word, DFt in IDFDict.items():
        IDFDict[word] = math.log(N / float(DFt), 10)
    return IDFDict

"""
Computes TF-IDF vectors of length vocabulary for each book by their descriptions or genres.
Please note that the order of terms in TF-IDF lists are the same as the order in vocabulary.
Returns: Dict
    TFDict = {
        'url1' : list(TF-IDFs) (length = |V|)
        'url2' : list(TF-IDFs) (length = |V|)
        ...
        'urlN' : list(TF-IDFs) (length = |V|)
    }
"""
def computeTFIDF(TFDict: dict, IDFDict: dict, vocabularyIndexTermMapping: dict) -> dict :
    TFIDFDict = dict()
    for url, TFList in TFDict.items():
        TFIDFDict[url] = TFList
        for i, TF in enumerate(TFList):
            IDF = IDFDict[vocabularyIndexTermMapping[i]]
            TFIDF = TF * IDF
            TFIDFDict[url][i] = TFIDF
    return TFIDFDict

# Computes the length of a vector.
def computeVectorLength(vector: list) -> float:
    res = 0.0
    for value in vector:
        res += math.pow(value, 2)
    return math.sqrt(res)

# Computes the Euclidean product of two vectors.
def computeVectorProduct(vector1 : list, vector2 : list) -> float:
    res = 0.0
    if len(vector1) != len(vector2):
        return False
    for val1, val2 in zip(vector1, vector2):
        res += val1 * val2
    return res
"""
Computes the cosine similarity values between vector pairs of query and books.
Returns: Dict
    Key: String (URL of Query)
    Values: Dict
        Key: String (URL)
        Value: Float (Cosine Similarity)
"""
def computeQueryBookCosineSimilarityDict(TFIDFDict:dict, TFIDFDictQuery: dict) -> dict:
    queryBookCosineSimilarityDict = dict()
    for queryUrl, TFIDFVectorQuery in TFIDFDictQuery.items():
        queryBookCosineSimilarityDict[queryUrl] = dict()
        for urlTarget, TFIDFVectorTarget in TFIDFDict.items():
            if queryUrl != urlTarget:
                lengthTFIDFVectorQuery = computeVectorLength(TFIDFVectorQuery)
                lengthTFIDFVectorTarget = computeVectorLength(TFIDFVectorTarget)
                if lengthTFIDFVectorQuery == 0 or lengthTFIDFVectorTarget == 0:
                    queryBookCosineSimilarityDict[queryUrl][urlTarget] = 0.0
                else:
                    cosineSimilarity = computeVectorProduct(TFIDFVectorQuery, TFIDFVectorTarget) / (lengthTFIDFVectorQuery * lengthTFIDFVectorTarget)
                    queryBookCosineSimilarityDict[queryUrl][urlTarget] = cosineSimilarity
    return queryBookCosineSimilarityDict

# This function has been written for testing purposes.
def checkSetIntersections(corpus: dict, key = 'DESC') -> dict:
    intersectionDict = dict()
    for urlSrc in corpus:
        intersectionDict[urlSrc] = dict()
        descSetSrc = set(corpus[urlSrc][key])
        for urlTarget in corpus:
            if urlSrc != urlTarget:
                descSetTarget = set(corpus[urlTarget][key])
                intersectionSet = descSetSrc.intersection(descSetTarget)
                intersectionDict[urlSrc][urlTarget] = len(intersectionSet)
    return intersectionDict

# Verifies whether the cosine similarity has been computed correctly.
# This function has been written for testing purposes.
def verifyCosineSimilarity(cosineSimilarityDict: dict, intersectionDict: dict) -> bool:
    for urlSrc in cosineSimilarityDict:
        for urlTarget in cosineSimilarityDict[urlSrc]:
            cosineSimilarity = cosineSimilarityDict[urlSrc][urlTarget]
            intersectionLength = intersectionDict[urlSrc][urlTarget]
            if cosineSimilarity == 0 and intersectionLength != 0:
                return False
            elif cosineSimilarity != 0 and intersectionLength == 0:
                return False
    return True

"""
Computes overall cosine similarity results by combining cosine similarities computed
for descriptions and genres of the query and book pairs.
Returns: Dict
    Key: String (URL of Query)
    Values: Dict
        Key: String (URL)
        Value: Float (Cosine Similarity)
"""
def getOverallCosineSimilarityResults(queryBookCosineSimilarityDictDesc:dict,queryBookCosineSimilarityDictGenres:dict,alpha:float) -> dict:
    overallCosineSimilarityDict = dict()
    for srcUrl in queryBookCosineSimilarityDictDesc:
        cosineSimilarityResultsDesc = queryBookCosineSimilarityDictDesc[srcUrl]
        cosineSimilarityResultsGenres = queryBookCosineSimilarityDictGenres[srcUrl]
        overallCosineSimilarityResults = dict()
        for targetUrl in cosineSimilarityResultsDesc:
            cosineSimilarityDesc = cosineSimilarityResultsDesc[targetUrl]
            cosineSimilarityGenre = cosineSimilarityResultsGenres[targetUrl]
            cosineSimilarity = (alpha * cosineSimilarityDesc) + ((1-alpha) * cosineSimilarityGenre)
            overallCosineSimilarityResults[targetUrl] = cosineSimilarity
        overallCosineSimilarityDict[srcUrl] = overallCosineSimilarityResults
    return overallCosineSimilarityDict

"""
Returns top K recommendations for the query URLs.
Returns: Dict
    Key: String (Query URL)
    Value: List<String> - List of book URLs sorted in descending order by their similarity values.
"""
def getTopKRecommendations(cosineSimilarityDict: dict, K = 18) -> dict :
    recommendations = dict()
    for urlSrc in cosineSimilarityDict:
        recommendations[urlSrc] = list()
        for urlTarget, similarity in cosineSimilarityDict[urlSrc].items():
            recommendations[urlSrc].append([urlTarget,similarity])
    for urlSrc in recommendations:
        recommendationsList = recommendations[urlSrc]
        recommendationsList.sort(key=lambda x: x[1], reverse=True)
        recommendations[urlSrc] = recommendationsList
    for urlSrc in recommendations:
        recommendationsList = recommendations[urlSrc]
        recommendationsList = recommendationsList[:K]
        recommendationsList = [recommendation[0] for recommendation in recommendationsList]
        recommendations[urlSrc] = recommendationsList
    return recommendations

# Saves the model components in the folder 'Assignment3Model/{KEY}'
# KEY is 'DESC' or 'GENRES'
def saveModel(key,vocabulary,IDFDict,TFIDFDict):
    os.makedirs(os.path.join(os.getcwd(),'Assignment3Model/{}'.format(key)))
    with open(os.path.join(os.getcwd(),'Assignment3Model/{}/vocabulary.pickle'.format(key)), 'wb') as f:
        pickle.dump(vocabulary,f,pickle.HIGHEST_PROTOCOL)
    with open(os.path.join(os.getcwd(), 'Assignment3Model/{}/IDFDict.pickle'.format(key)), 'wb') as f:
        pickle.dump(IDFDict, f, pickle.HIGHEST_PROTOCOL)
    with open(os.path.join(os.getcwd(), 'Assignment3Model/{}/TFIDFDict.pickle'.format(key)), 'wb') as f:
        pickle.dump(TFIDFDict, f, pickle.HIGHEST_PROTOCOL)

# Loads the model components in the folder 'Assignment3Model/{KEY}'
# KEY is 'DESC' or 'GENRES'
def loadModel(key):
    vocabulary = list()
    IDFDict = dict()
    TFIDFDict = dict()
    with open(os.path.join(os.getcwd(),'Assignment3Model/{}/vocabulary.pickle'.format(key)), 'rb') as f:
        vocabulary = pickle.load(f)
    with open(os.path.join(os.getcwd(), 'Assignment3Model/{}/IDFDict.pickle'.format(key)), 'rb') as f:
        IDFDict = pickle.load(f)
    with open(os.path.join(os.getcwd(), 'Assignment3Model/{}/TFIDFDict.pickle'.format(key)), 'rb') as f:
        TFIDFDict = pickle.load(f)
    return vocabulary, IDFDict, TFIDFDict

# Deletes the previously saved model folder named 'Assignment3Model'.
def deleteModel():
    try:
        shutil.rmtree(os.path.join(os.getcwd(),'Assignment3Model'))
        print("Previously saved model deleted!")
    except Exception as e:
        print("No previously saved model found!")

# Enables reading multiple queries from a file.
def getQueryList(fileName = 'query.txt') -> list:
    queryList = list()
    with open(fileName, 'r') as f:
        for line in f:
            line = line.strip()
            queryList.append(line)
    print(queryList)
    return queryList

# Prints the content of a query book.
def printBook(queryMetadata: dict, query: str):
    print("\nThe content of the book for query: {}".format(query))
    for key in queryMetadata:
        title = queryMetadata[key]['TITLE']
        authorsList = queryMetadata[key]['AUTHORS']
        description = queryMetadata[key]['DESC']
        recommendationsList = queryMetadata[key]['RECOMMENDATIONS']
        genresList = queryMetadata[key]['GENRES']
        print("Book URL: {}".format(key))
        print("Title: {}".format(title))
        print("Authors:",end=' ')
        printList(authorsList)
        print("Description: {}".format(description))
        print("Recommendations:",end=' ')
        printList(recommendationsList)
        print("Genres:",end=' ')
        printList(genresList)

# Prints the content of a list.
def printList(myList:list):
    for i in range(len(myList) - 1):
        print(myList[i],end=', ')
    print(myList[-1])

# Prints the predicted recommendations.
def printRecommendations(predictedRecommendations: dict, metadata: dict):
    print("\nPredicted Recommendations:")
    for url, recommendationsList in predictedRecommendations.items():
        for i, recommendation in enumerate(recommendationsList):
            print("{}) {} - ".format(i+1,metadata[recommendation]['TITLE']),end='')
            printList(metadata[recommendation]['AUTHORS'])