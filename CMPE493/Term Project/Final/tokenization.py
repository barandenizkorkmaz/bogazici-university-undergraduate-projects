import os
import sys
import pickle
import csv

# REFERENCE: https://stackoverflow.com/questions/52937859/read-csv-file-line-by-line-python
def tokenization(file_name='metadata.csv'):
    docs = dict()
    with open (file_name,'r') as csv_file:
        reader =csv.reader(csv_file)
        next(reader) # skip first row
        for row in reader:
            cord_uid = row[0]
            title = row[3]
            abstract = row[8]
            if cord_uid in docs:
                if len(title) > len(docs[cord_uid]['TITLE']):
                    docs[cord_uid]['TITLE'] = title
                if len(abstract) > len(docs[cord_uid]['ABSTRACT']):
                    docs[cord_uid]['ABSTRACT'] = abstract
            else:
                docs[cord_uid] = {'TITLE': title,
                              'ABSTRACT': abstract}
    for docId in docs:
        title = docs[docId]['TITLE']
        abstract = docs[docId]['ABSTRACT']
        docs[docId]['TITLE'] = title.split()
        docs[docId]['ABSTRACT'] = abstract.split()
    return docs

def saveDocs(docs,fileName = 'TREC-COVID_DOCS.pickle'):
    with open(fileName, 'wb') as f:
        pickle.dump(docs, f, protocol=pickle.HIGHEST_PROTOCOL)

def loadDocs(fileName = 'TREC-COVID_DOCS.pickle'):
    with open(fileName, 'rb') as f:
        return pickle.load(f)