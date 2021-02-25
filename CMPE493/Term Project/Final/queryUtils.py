import math
import string
import xml.etree.ElementTree as ET
import json
import pickle

import normalization

def getQueries():
    tree = ET.parse('topics-rnd5.xml')
    root = tree.getroot()
    queryDict = dict()
    for child in root.findall('topic'):
        id = child.get('number')
        queryDict[id] = {}
        queryDict[id]['query'] = child.find('query').text
        queryDict[id]['question'] = child.find('question').text
        queryDict[id]['narrative'] = child.find('narrative').text
    return queryDict

def getQuerySet(subset:str):
    queries = getQueries()
    querySet = dict()
    if subset.lower() == "training":
        for key in queries:
            if int(key) % 2 == 1:
                querySet[key] = queries[key]['query'] + " " + queries[key]['question'] + " " + queries[key]['narrative']
    elif subset.lower() == "test":
        for key in queries:
            if int(key) % 2 == 0:
                querySet[key] = queries[key]['query'] + " " + queries[key]['question'] + " " + queries[key]['narrative']
    else:
        for key in queries:
            querySet[key] = queries[key]['query'] + " " + queries[key]['question'] + " " + queries[key]['narrative']
    return querySet