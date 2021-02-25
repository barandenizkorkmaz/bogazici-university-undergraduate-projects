from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import tokenization, normalization, structures, queryUtils, evaluation

isDocsFound = structures.searchExistingFile('TREC-COVID_DOCS.pickle')
print("Is 'TREC-COVID_DOCS.pickle' found?: ",isDocsFound)

if not isDocsFound:
    docs = tokenization.tokenization()
    print("Tokenization has been successfully done...")
    docs = normalization.normalization_manager(docs)
    print("Normalization has been successfully done...")
    tokenization.saveDocs(docs)

docs = tokenization.loadDocs()
docIds = structures.getDocIds(docs)
corpus = structures.getCorpusList(docs)
del docs

vectorizer = TfidfVectorizer()
tfidfMatrix =  vectorizer.fit_transform(corpus)
print("(Number of Documents, Vocabulary Size): ",tfidfMatrix.shape)

querySet = queryUtils.getQuerySet("test")
querySet = normalization.normalizeQuerySet(querySet)

results = dict()
for query in querySet:
    queryString = querySet[query]
    queryTFIDFVector = vectorizer.transform([queryString])
    cosineSimilarityVector = cosine_similarity(queryTFIDFVector, tfidfMatrix)[0]
    queryResult = list()
    for docId, cosineSimilarity in zip(docIds, cosineSimilarityVector):
        queryResult.append([docId, cosineSimilarity])
    results[query] = queryResult

# Rank documents for each query by cosineSimilarity. (For analysis purposes)
for queryId in results:
    resultsList = results[queryId]
    resultsList.sort(key=lambda x: x[1], reverse=True)
    results[queryId] = resultsList

evaluation.getResultsFile(results)