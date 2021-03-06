import nltk
from nltk.corpus import stopwords
from gensim import corpora
import gensim
import numpy as np


def get_cleaned_tokens(text):
    """ Returns a list of tokens from text, cleaned 
        and with stopwords removed. """
    words = nltk.word_tokenize(text.lower())
    stops = set(stopwords.words("english"))
    tokens = [w.encode('ascii',errors='ignore').decode()
              for w in words if w[0].isalpha() and w not in stops]
    return tokens


class Corpus:
    def __init__(self, raw_texts,filter_extremes=True):
        texts = [get_cleaned_tokens(text)
                 for text in raw_texts]
        self.dictionary = corpora.Dictionary(texts)
        if filter_extremes:
            self.dictionary.filter_extremes()
        self.corpus = [self.dictionary.doc2bow(text) for text in texts]
        self.rev_dictionary = {v:k for k,v in self.dictionary.iteritems()}
        self.matrix = gensim.matutils.corpus2csc(self.corpus)
        
    def num(self,contains=None):
        if contains is None:
            return len(self.corpus)
        if type(contains) == str:
            try:
                k = self.rev_dictionary[contains]
                return self.matrix[k,:].getnnz()
            except:
                return 0
        else:
            keys = [self.rev_dictionary[word]
                    for word in contains if word in self.rev_dictionary]
            if len(keys) == 0:
                return 0
            entries = np.sum(self.matrix[keys,:],axis=0)
            return np.sum(entries > 0)
