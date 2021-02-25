import os

def searchExistingFile(file_name):
    return os.path.exists(file_name)

def getCorpusList(docs:dict):
    docIds = getDocIds(docs) # Sorted
    corpus = list()
    for docId in docIds:
        textList = list()
        title = docs[docId]['TITLE']
        abstract = docs[docId]['ABSTRACT']
        for elem in title:
            textList.append(elem)
        for elem in abstract:
            textList.append(elem)
        corpus.append(' '.join(textList))
    return corpus

def getDocIds(docs:dict):
    return sorted(docs.keys())