import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import enchant
ps = PorterStemmer()

d = enchant.Dict("en_US")

def getKeywords(fileName = 'keywords.txt'):
    keywordsList = list()
    with open("keywords.txt", 'r') as f:
        for line in f.readlines():
            keywordsList.append(line.strip())
    return keywordsList

keywords = getKeywords()

def download_stopwords():
    nltk.download()

def get_stopwords():
    return stopwords.words('english')

def normalization_manager(documents:dict):
    for document in documents:
        for zone in documents[document]:
            tokens = documents[document][zone]
            documents[document][zone] = normalization(tokens)
    return documents

def normalization(tokens:list):
    tokens = caseFolding(tokens)
    tokens = punctuationRemoval(tokens)
    tokens = stopwordRemoval(tokens)
    tokens = numericRemoval(tokens)
    tokens = shortTokenRemoval(tokens)
    return tokens

def caseFolding(tokens:list):
    newTokens = [token.lower() for token in tokens]
    return newTokens

def punctuationRemoval(tokens:list):
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))  # map punctuation to space
    newTokens = [token.translate(translator) for token in tokens]  # Punctuation Removal
    str_tokens = " ".join(token for token in newTokens)  # Retokenize the tokens that include any whitespaces after punctuation removal.
    newTokens = str_tokens.split()
    return newTokens

def stopwordRemoval(tokens:list):
    stopwords = get_stopwords()
    newTokens = [token for token in tokens if token not in stopwords]
    return newTokens

def numericRemoval(tokens:list): # Preserves keywords!
    keywords = getKeywords()
    newTokens = [x for x in tokens if x in keywords or not any(c.isdigit() for c in x)]
    return newTokens

def normalizeQuerySet(querySet:dict):
    for queryId in querySet:
        query = querySet[queryId]
        queryTokens = query.split()
        queryTokens = normalization(queryTokens)
        querySet[queryId] = ' '.join(queryTokens)
    return querySet

def shortTokenRemoval(tokens:list):
    newTokens = [token for token in tokens if len(token) > 2]
    return newTokens