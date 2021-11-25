import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer


# Returns clean tokens from a tweet given
def stopwords_stemmer(tweet):
    tokens = nltk.word_tokenize(tweet)
    stoplist = stopwords.words['spanish']
    stoplist += []
    clean_tokens = tokens.copy()

    for token in tokens:
        if token in stoplist:
            clean_tokens.remove(token)
    
    stemmer = SnowballStemmer("spanish")
    for i in range(len(clean_tokens)):
        clean_tokens[i] = stemmer.stem(clean_tokens[i])
    
    return clean_tokens

def cosine(q, doc):
    return np.dot(q, doc) / (np.linalg.norm(q) * np.linalg.norm(doc))