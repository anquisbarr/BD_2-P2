import nltk
import pickle
import json
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from collections import Counter
from math import log
from queue import PriorityQueue

# Global path
bin_path = './data/bin/'
json_path = './data/json_files/'

# Initialization
terms_dict = {}
files_dict = {}
tweets_dict = {}
terms_df_dict = {}
n_tweets = 0
n_terms = 0

# Opening .dat files and loading data
terms_dict = pickle.load(open(bin_path + 'terms_dict.dat','rb'))
files_dict = pickle.load(open(bin_path + 'files_dict.dat','rb'))
tweets_dict = pickle.load(open(bin_path + 'tweets_dict.dat','rb'))
terms_df_dict = pickle.load(open(bin_path + 'terms_df_dict.dat','rb'))
n_tweets = pickle.load(open(bin_path + 'n_tweets.dat','rb'))
n_terms = pickle.load(open(bin_path + 'n_terms.dat','rb'))

# Returns clean tokens from a tweet given
def stopwords_stemmer(tweet):
    tokens = nltk.word_tokenize(tweet)
    stoplist = stopwords.words('spanish')
    stoplist += ['/…','--','RT','`','@','|','¿','?', '¡', '!', '.', ',', ';', '«', '»', ':', '(', ')', '"','#', '$', '^', '&', '*', '%','IndianArmyPeoplesArmy']
    clean_tokens = tokens.copy()

    for token in tokens:
        if token in stoplist:
            clean_tokens.remove(token)
    
    stemmer = SnowballStemmer("spanish")
    for i in range(len(clean_tokens)):
        clean_tokens[i] = stemmer.stem(clean_tokens[i])
    
    return clean_tokens

# Calculations utility funcions
def cosine(q, q_norm, doc, doc_norm):
    dot = float(0)
    for term_id in q:
        if (term_id in doc):
            dot += q[term_id] * doc[term_id]
    return dot/(q_norm*doc_norm)

def norm(tweet_list):
    val = np.array(list(tweet_list.values()))
    return np.linalg.norm(val)

# Query parser function, looking for term in the terms_dict and storing their term_id and tf_idf
def queryParser(query):
    q = stopwords_stemmer(query)
    term_freq = Counter(q)
    result = {}
    for term in term_freq:
        if (term in terms_dict):
            term_id = terms_dict[term]
            tf = term_freq[term]
            df = terms_df_dict[term_id]
            tf_idf = log(1+tf,10)*log(n_terms/df,10)
            result[term_id] = tf_idf
    return result
    
# Gets k (tweet_id,cosine) for query given
def searchKNN(q,k):
    priority_queue = PriorityQueue()
    q = queryParser(q)
    q_norm = norm(q)
    for tweet_id in tweets_dict:
        doc = tweets_dict[tweet_id][1]
        doc_norm = tweets_dict[tweet_id][2]
        cosine_val = cosine(q,q_norm,doc,doc_norm)
        if (priority_queue.qsize() < k):
            priority_queue.put((cosine_val,tweet_id))
        else:
            top_prio = priority_queue.get()
            if (cosine_val > top_prio[0]):
                priority_queue.put((cosine_val,tweet_id))
            else:
                 priority_queue.put(top_prio)
    result = [0] * k
    i = k -1
    while not priority_queue.empty():
        data = priority_queue.get()
        result[i] = data
        i -= 1
    return result

# Return a single tweet in JSON format given a doc
def retrieve_tweet(tweet_id):
    file_id = tweets_dict[tweet_id][0]
    filename = files_dict[file_id]
    with open (json_path + 'ucl/' + filename, encoding='utf8') as file:
        json_content = json.load(file)
        for tweet in json_content:
            if tweet['id'] == tweet_id:
                return json.dumps(tweet)

def retrieve_tweets(query,k):
    result = []
    distances = searchKNN(query,k)
    for pairs in distances:
        dist  = pairs[0]
        doc = pairs[1]
        result.append(json.loads(retrieve_tweet(doc)))
    return json.dumps(result)