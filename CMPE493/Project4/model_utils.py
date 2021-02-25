# Returns the number of documents in a corpus.
def getNumDocuments(corpus: dict) -> int:
    totalNumDocuments = 0
    for label in corpus:
        totalNumDocuments += len(corpus[label])
    return totalNumDocuments

"""
Returns the prior probability values for each classes.
Returns:
    dict:
        Key:
            Class label. (0 for legitimate, 1 for spam)
            Type: int
        Value:
            Prior probability.
            Type: float
"""
def getPriorProbabilities(corpus: dict) -> dict:
    priorProbabilities = dict()
    totalNumDocuments = getNumDocuments(corpus)
    for label in corpus:
        docs_j = len(corpus[label])
        priorProbabilities[label] = float(docs_j)/totalNumDocuments
    return priorProbabilities

"""
Returns the conditional probability values for every word in a given vocabulary.
Returns:
    dict:
        Key:
            Class label. (0 for legitimate, 1 for spam)
            Type: int
        Value:
            Dictionary
            Key:
                A word in a given vocabulary.
                Type: string
            Value:
                Conditional probability value.
                Type: float
"""
def getConditionalProbabilities(corpus: dict, vocabulary: list, alpha = 1) -> dict:
    conditionalProbabilities = dict()
    sizeOfVocabulary = len(vocabulary)
    for label in corpus:
        conditionalProbabilities[label] = dict()
        text_j = ' '.join(corpus[label])
        text_j = text_j.split()
        n = len(text_j)
        for word in vocabulary:
            n_k = 0
            for word_text in text_j:
                if word_text == word:
                    n_k += 1
            probability = float(n_k + alpha)/(n + alpha * sizeOfVocabulary)
            conditionalProbabilities[label][word] = probability
    return conditionalProbabilities