from utils.mnb import MultiNB
import json
import string
import pickle
import numpy as np
import nltk
import sklearn
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


wordnet_lemmatizer = WordNetLemmatizer()

allwords = set(nltk.corpus.words.words())

total_documents = 11314

with open("model/count_dict.json", "r") as f:
    word_count = json.load(f)
# print(len(word_count))

word_set = list(word_count.keys())

# print(word_set[0])

index_dict = {}  # Dictionary to store index for each word
i = 0
for word in word_set:
    index_dict[word] = i
    i += 1


def punc_f(text):
    text = text.replace("\n", " ")
    punc_rmv = "".join([char for char in text if char not in string.punctuation])

    return punc_rmv


def onlye_f(text):
    tknized = [i.lower() for i in word_tokenize(text) if i.lower() in allwords]

    return " ".join(tknized)


def stopword_f(text):
    stopword_rmv = [
        i for i in word_tokenize(text) if i not in stopwords.words("english")
    ]

    return " ".join(stopword_rmv)


def lem_f(text):
    lem_text = [wordnet_lemmatizer.lemmatize(word) for word in word_tokenize(text)]

    return " ".join(lem_text)


# Term Frequency
def termfreq(document, word):
    N = len(document)
    occurance = len([token for token in document if token == word])
    return occurance / N


# Inverse Document Frequency
def inverse_doc_freq(word):
    try:
        word_occurance = word_count[word]
    except:
        word_occurance = 1
    return np.log(total_documents / word_occurance)


def tf_idf_(sentence):
    tf_idf_vec = np.zeros((len(word_set),))
    for word in sentence:
        if word in word_set:
            tf = termfreq(sentence, word)
            idf = inverse_doc_freq(word)

            value = tf * idf
            tf_idf_vec[index_dict[word]] = value
    return tf_idf_vec


def predict_cat(text):
    """function to predict the category of the given post"""
    new_test = [text]

    test_n = []
    for sent in new_test:
        f = punc_f(sent)
        f = onlye_f(f)
        f = stopword_f(f)
        f = lem_f(f)
        test_n.append(f)

    X_test_v = []
    for sent in test_n:
        vec = tf_idf_(sent.split(" "))
        X_test_v.append(vec)
    X_test_v = np.array(X_test_v)

    with open("model/flyer_pkl2", "rb") as f:
        nb = pickle.load(f)

    predict_test = nb.predict(X_test_v)

    return predict_test[0]

    # print(predict_test[0])
    # print(nb.predict_proba)
    # print(nb.predict_proba(X_test_v))


# predict_cat("Stocks fall on Wall Street, giving back some recent gains")
