import os

import config

# Class definitions declared by the programmer.
CLASSES = {
        "legitimate": 0,
        "spam": 1
    }

"""
Returns the corpus for a subset where subset is either training or test.
Arguments:
    subset:
        The argument declares the subset that will be read. Its value is in {'training','test'}.
        Type: string
Returns:
    corpus:
        The dictionary that holds the list of documents belonging to the classes.
        Type: dict
        Format:
            {
                0: list(str)
                1: list(str)
            }
"""
def getCorpus(subset:str) -> dict:
    global CLASSES
    corpus = dict()
    PATH = config.TRAINING_SET_PATH if subset=="training" else config.TEST_SET_PATH
    for key, label in CLASSES.items():
        corpus[label] = list()
        class_path = os.path.join(PATH,key)
        for filename in os.listdir(class_path):
            with open(os.path.join(class_path, filename), 'r', encoding='latin-1') as f:
                lines = f.readlines()
                tmp = [line.strip() for line in lines]
                text = " ".join(tmp)
                tmp = text.split()
                tmp = tmp[1:] #Eliminates 'Subject:' part of the document.
                text = " ".join(tmp)
                corpus[label].append(text)
    return corpus

"""
Returns the input and class labels for a subset which is either training or test.
Arguments:
    corpus:
        The dictionary that holds the list of documents belonging to the classes.
        Type: dict
        Format:
            {
                0: list(str)
                1: list(str)
            }
Returns:
    tuple:
        x:
            List of documents in the subset.
            Type: list(str)
        y:
            List of class labels
            Type: list(int)
"""
def getDataset(corpus:dict) -> tuple:
    x = list()
    y = list()
    for label, docs in corpus.items():
        x.extend(docs)
        y.extend([label] * len(docs))
    return x, y

"""
Returns the vocabulary from a given corpus.
Arguments:
    corpus:
        The dictionary that holds the list of documents belonging to the classes.
        Type: dict
        Format:
            {
                0: list(str)
                1: list(str)
            }
Returns:
    vocabulary:
        List of unique words in the corpus
        Type: list(str)
"""
def getVocabulary(corpus:dict) -> list:
    vocabulary = list()
    for label, docs in corpus.items():
        text_j = ' '.join(docs)
        text_j_words = text_j.split()
        text_j_vocabulary = set(text_j_words)
        vocabulary.extend(list(text_j_vocabulary))
    return vocabulary