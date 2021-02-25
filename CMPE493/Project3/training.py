import sys
import scrapingUtils, preprocessing, queryUtils

# The provided user input.
fileName = str(sys.argv[1])

# Delete the previously saved data including content of books fetched and encoded,
# and the model itself.
isMetadataFound = scrapingUtils.searchMetadata()
print("Is previously saved metadata found?\n",isMetadataFound)

if isMetadataFound:
    scrapingUtils.deleteMetadata()

queryUtils.deleteModel()

# Fetch and save the content of books from the URLs provided in the file.
bookURLS = scrapingUtils.getBookURLs(fileName=fileName)
metadata = scrapingUtils.getMetadata(bookURLS)
scrapingUtils.saveMetadata(metadata)

# Construct corpus by applying tokenization and normalization onto the previously
# fetched content of books.
corpus = preprocessing.getCorpus(metadata)
corpus = preprocessing.tokenize(corpus)
corpus = preprocessing.normalization_manager(corpus)
del metadata

# Build and save the model for descriptions based on TF-IDF weighting scheme.
vocabularyDesc = queryUtils.getVocabulary(corpus, key='DESC')
vocabularyTermIndexMappingDesc, vocabularyIndexTermMappingDesc = queryUtils.getVocabularyMappings(vocabularyDesc)
TFDictDesc = queryUtils.computeTF(corpus, vocabularyTermIndexMappingDesc, key='DESC')
IDFDictDesc = queryUtils.computeIDF(corpus,vocabularyTermIndexMappingDesc, key='DESC')
TFIDFDictDesc = queryUtils.computeTFIDF(TFDictDesc, IDFDictDesc, vocabularyIndexTermMappingDesc)
queryUtils.saveModel('DESC',vocabularyDesc,IDFDictDesc,TFIDFDictDesc)
del vocabularyDesc, vocabularyIndexTermMappingDesc, vocabularyTermIndexMappingDesc, TFDictDesc, IDFDictDesc, TFIDFDictDesc

# Build and save the model for genres based on TF-IDF weighting scheme.
vocabularyGenres = queryUtils.getVocabulary(corpus, key='GENRES')
vocabularyTermIndexMappingGenres, vocabularyIndexTermMappingGenres = queryUtils.getVocabularyMappings(vocabularyGenres)
TFDictGenres = queryUtils.computeTF(corpus, vocabularyTermIndexMappingGenres, key='GENRES')
IDFDictGenres = queryUtils.computeIDF(corpus,vocabularyTermIndexMappingGenres, key='GENRES')
TFIDFDictGenres = queryUtils.computeTFIDF(TFDictGenres, IDFDictGenres, vocabularyIndexTermMappingGenres)
queryUtils.saveModel('GENRES',vocabularyGenres,IDFDictGenres,TFIDFDictGenres)
del vocabularyGenres, vocabularyIndexTermMappingGenres, vocabularyTermIndexMappingGenres, TFDictGenres, IDFDictGenres, TFIDFDictGenres