from nltk.corpus import stopwords
import pickle

def get_stopwords():
    return stopwords.words('english')

def saveStopwords(fileName='stopwords.pickle'):
    with open(fileName,'wb') as f:
        pickle.dump(get_stopwords(),f,pickle.HIGHEST_PROTOCOL)

saveStopwords()