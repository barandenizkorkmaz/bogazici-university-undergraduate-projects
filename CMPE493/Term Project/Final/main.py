from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

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

print("Corpus loaded.")
sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
document_embeddings = sbert_model.encode(corpus)
print("Document embeddings calculated.")

querySet = queryUtils.getQuerySet("test")
querySet = normalization.normalizeQuerySet(querySet)

results = dict()
for queryId, queryStr in querySet.items():
    query_embedding = sbert_model.encode([queryStr])
    cosineSimilarityVector = cosine_similarity(query_embedding,document_embeddings)[0]
    queryResult = list()
    for docId, cosineSimilarity in zip(docIds, cosineSimilarityVector):
        queryResult.append([docId,cosineSimilarity])
    results[queryId] = queryResult

# Rank documents for each query by cosineSimilarity. (For analysis purposes)
for queryId in results:
    resultsList = results[queryId]
    resultsList.sort(key=lambda x: x[1], reverse=True)
    results[queryId] = resultsList

evaluation.getResultsFile(results)