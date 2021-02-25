import pickle
import string

# Loads the metadata.
def loadMetadata(fileName='metadataAss3.pickle'):
    with open(fileName, 'rb') as f:
        return pickle.load(f)

# Loads the stopwords.
def loadStopwords(fileName='stopwords.pickle'):
    with open(fileName, 'rb') as file:
        return pickle.load(file)

"""
Returns the corpus using metadata.
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
            'DESC': str
            'GENRES': list(str)
        },
        ...
    }
"""
def getCorpus(metadata:dict) -> dict:
    corpus = dict()
    for url in metadata:
        corpus[url] = dict()
        corpus[url]['DESC'] = metadata[url]['DESC']
        corpus[url]['GENRES'] = metadata[url]['GENRES']
    return corpus

# Applies tokenization.
def tokenize(corpus:dict) -> dict:
    for url in corpus:
        corpus[url]['DESC'] = corpus[url]['DESC'].split()
    return corpus

# Manages normalization for every token in corpus.
def normalization_manager(corpus:dict) -> dict:
    for url in corpus:
        tokens = corpus[url]['DESC']
        corpus[url]['DESC'] = normalization(tokens)
    return corpus

# Applies normalization for every token in corpus.
def normalization(tokens:list):
    tokens = caseFolding(tokens)
    tokens = punctuationRemoval(tokens)
    tokens = stopwordRemoval(tokens)
    tokens = shortTokenRemoval(tokens)
    return tokens

# Applies case-folding for every token in the given list.
def caseFolding(tokens:list):
    newTokens = [token.lower() for token in tokens]
    return newTokens

# Applies puncutation removal for every token in the given list.
def punctuationRemoval(tokens:list):
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))  # map punctuation to space
    newTokens = [token.translate(translator) for token in tokens]  # Punctuation Removal
    str_tokens = " ".join(token for token in newTokens)  # Retokenize the tokens that include any whitespaces after punctuation removal.
    newTokens = str_tokens.split()
    return newTokens

# Applies apostrophe removal for every token in the given list.
def apostropheRemoval(tokens:list):
    for token in tokens:
        token = token.replace("'"," ")
    str_tokens = " ".join(token for token in tokens)  # Retokenize the tokens that include any whitespaces after punctuation removal.
    newTokens = str_tokens.split()
    return newTokens

# Applies stopword removal for every token in the given list.
def stopwordRemoval(tokens:list):
    stopwords = loadStopwords()
    newTokens = [token for token in tokens if token not in stopwords]
    return newTokens

# Applies numeric removal for every token in the given list.
def numericRemoval(tokens:list):
    newTokens = [x for x in tokens if not any(c.isdigit() for c in x)]
    return newTokens

# Removes the tokens of length smaller than or equal to 2 for every token in the given list.
def shortTokenRemoval(tokens:list):
    newTokens = [token for token in tokens if len(token) > 2]
    return newTokens