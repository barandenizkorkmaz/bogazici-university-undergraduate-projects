import sys
import scrapingUtils, preprocessing, queryUtils, evaluationUtils

# The provided user input.
query = str(sys.argv[1])
queryList = [query]

# Load previously fetched content of books from Goodreads, which will be used to get the fields like
# title and author of books to output.
metadata = preprocessing.loadMetadata()

# Fetch and save the content of book given in the URL, and apply same preprocessing stages.
queryMetadata = scrapingUtils.getMetadata(queryList)
queryUtils.printBook(queryMetadata, query)
queryCorpus = preprocessing.getCorpus(queryMetadata)
queryCorpus = preprocessing.tokenize(queryCorpus)
queryCorpus = preprocessing.normalization_manager(queryCorpus)

# Get ground truth recommendations for the query book.
actualRecommendations = evaluationUtils.getGoodreadsRecommendations(queryMetadata)

# Load model for descriptions and compute TF-IDF vector for query.
vocabularyDesc, IDFDictDesc, TFIDFDictDesc = queryUtils.loadModel('DESC')
vocabularyTermIndexMappingDesc, vocabularyIndexTermMappingDesc = queryUtils.getVocabularyMappings(vocabularyDesc)
TFDictQueryDesc = queryUtils.computeTF(queryCorpus,vocabularyTermIndexMappingDesc,key='DESC')
TFIDFDictQueryDesc = queryUtils.computeTFIDF(TFDictQueryDesc, IDFDictDesc, vocabularyIndexTermMappingDesc)

# Compute cosine similarities for the pairs of query and books in the metadata.
queryBookCosineSimilarityDictDesc = queryUtils.computeQueryBookCosineSimilarityDict(TFIDFDictDesc, TFIDFDictQueryDesc)
del vocabularyDesc, IDFDictDesc, TFIDFDictDesc, vocabularyTermIndexMappingDesc, vocabularyIndexTermMappingDesc, TFDictQueryDesc, TFIDFDictQueryDesc

# Load model for genres and compute TF-IDF vector for query.
vocabularyGenres, IDFDictGenres, TFIDFDictGenres = queryUtils.loadModel('GENRES')
vocabularyTermIndexMappingGenres, vocabularyIndexTermMappingGenres = queryUtils.getVocabularyMappings(vocabularyGenres)
TFDictQueryGenres = queryUtils.computeTF(queryCorpus,vocabularyTermIndexMappingGenres,key='GENRES')
TFIDFDictQueryGenres = queryUtils.computeTFIDF(TFDictQueryGenres, IDFDictGenres, vocabularyIndexTermMappingGenres)

# Compute cosine similarities for the pairs of query and books in the metadata.
queryBookCosineSimilarityDictGenres = queryUtils.computeQueryBookCosineSimilarityDict(TFIDFDictGenres, TFIDFDictQueryGenres)
del vocabularyGenres, IDFDictGenres, TFIDFDictGenres, vocabularyTermIndexMappingGenres, vocabularyIndexTermMappingGenres, TFDictQueryGenres, TFIDFDictQueryGenres

# Compute overall cosine similarities by combining the similarities for descriptions and genres using alpha.
ALPHA = 0.625
overallCosineSimilarityDict = queryUtils.getOverallCosineSimilarityResults(queryBookCosineSimilarityDictDesc,queryBookCosineSimilarityDictGenres,alpha=ALPHA)

# Get top 18 recommendations and print.
predictedRecommendations = queryUtils.getTopKRecommendations(overallCosineSimilarityDict,K=18)
queryUtils.printRecommendations(predictedRecommendations, metadata)

# Evaluation
precision, averagePrecisionAtN = evaluationUtils.evaluate(predictedRecommendations,actualRecommendations)
evaluationUtils.printEvaluations(ALPHA,precision,averagePrecisionAtN,K=18)