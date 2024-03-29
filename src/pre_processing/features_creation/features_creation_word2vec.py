# Word2Vec Function
import gensim
from gensim.models import Word2Vec
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

def get_word2vec_features(text_data):
    # split the text data into sentences
    sentences = [sentence.split() for sentence in text_data]

    # train a Word2Vec model on the sentences
    model = Word2Vec(sentences, min_count=1, vector_size=100, workers=4)

    # get the Word2Vec vectors for the words in the vocabulary
    vectors = model.wv.vectors

    # get the vocabulary of the Word2Vec model
    vocab = model.wv.key_to_index.keys()

    # create a TF-IDF vectorizer
    tfidf = TfidfVectorizer()
    tfidf.fit(text_data)

    # transform the text data into a TF-IDF matrix
    tfidf_matrix = tfidf.transform(text_data)

    # compute the TF-IDF weighted Word2Vec vectors
    weighted_vectors = []
    for i, word in enumerate(vocab):
        tfidf_score = tfidf.idf_[tfidf.vocabulary_[word]] if word in tfidf.vocabulary_ else 1
        weighted_vector = vectors[i] * tfidf_score
        weighted_vectors.append(weighted_vector)

    # create a dictionary mapping words to vectors
    word_to_vec = dict(zip(vocab, weighted_vectors))

    # define a function to compute the average word vector for a sentence
    def sentence_to_avg_vector(sentence):
        words = sentence.split()
        vectors = [word_to_vec[word] for word in words if word in word_to_vec]
        if len(vectors) > 0:
            return np.mean(vectors, axis=0)
        else:
            return np.zeros(100)

    # compute the average word vector for each sentence
    features = np.array([sentence_to_avg_vector(sentence) for sentence in text_data])
    
    return features


# In[ ]:
# TF-IDF weighted Word2Vec vectors Function
import gensim
from gensim.models import Word2Vec
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from fuzzywuzzy import fuzz
import re

def get_word2vec_features(text_data):
    # split the text data into sentences
    sentences = [sentence.split() for sentence in text_data]

    # train a Word2Vec model on the sentences
    #model = Word2Vec(sentences, min_count=1, vector_size=100, workers=4)
    model = Word2Vec(sentences,window=7, min_count=1, sg=1, alpha=0.5) # Best hyperparameters for xgboost (recall)

    # get the Word2Vec vectors for the words in the vocabulary
    vectors = model.wv.vectors

    # get the vocabulary of the Word2Vec model
    vocab = model.wv.key_to_index.keys()

    # create a TF-IDF vectorizer
    tfidf = TfidfVectorizer()
    tfidf.fit(text_data)

    # transform the text data into a TF-IDF matrix
    tfidf_matrix = tfidf.transform(text_data)

    # compute the TF-IDF weighted Word2Vec vectors
    weighted_vectors = []
    for i, word in enumerate(vocab):
        tfidf_score = tfidf.idf_[tfidf.vocabulary_[word]] if word in tfidf.vocabulary_ else 1
        weighted_vector = vectors[i] * tfidf_score
        weighted_vectors.append(weighted_vector)

    # create a dictionary mapping words to vectors
    word_to_vec = dict(zip(vocab, weighted_vectors))

    # define a function to compute the average word vector for a sentence
    def sentence_to_avg_vector(sentence):
        words = sentence.split()
        vectors = [word_to_vec[word] for word in words if word in word_to_vec]
        if len(vectors) > 0:
            return np.mean(vectors, axis=0)
        else:
            return np.zeros(100)

    # compute the average word vector for each sentence
    features = np.array([sentence_to_avg_vector(sentence) for sentence in text_data])
    
    return features

def word2vec_dummy(df, column, words_list, threshold=90):
    
    # Get Word2Vec features for the text column
    features = get_word2vec_features(df[column])
    # Create a new column for each word in the list
    
    for word in words_list:
        # Compute the average Word2Vec vector for the word
        word_vec = np.mean([word_to_vec[word] for word_to_vec in features if word in word_to_vec], axis=0)
        
        # Create a new column name for the word
        column_name = f"{column}_{word}"
        
        # Compute the similarity metric between the word vector and each row of the text column
        df[column_name] = df[column].apply(lambda x: fuzz.ratio(word, x) if fuzz.ratio(word, x) >= threshold else 0)
        
        # Multiply the similarity metric by the corresponding component of the Word2Vec vector
        df[column_name] = df[column_name] * word_vec
        
    return df
import math
def w2v(alertP1):
    #alertP1= pre_process(alertP1)
    
    # Split data into train and test
    AlertP1_sorted = alertP1[alertP1['clean_text']!=''].sort_values(by='DATA_RECEPCAO')

    # calculate the index for the split
    split_index = math.ceil(0.8 * len(AlertP1_sorted))

    # split the data frame into test and train sets
    train_set = AlertP1_sorted.iloc[:split_index]
    test_set = AlertP1_sorted.iloc[split_index:]


    #Converting text into list of sentences
    sentences = train_set['clean_text'].tolist()

    #W2V model building
    model = Word2Vec(sentences, window=3, min_count=5, workers=4,sg=1,alpha=0.01)  # Adjust parameters as needed
    
    #Featurization
    def get_sentence_vector(sentence):
        vectors = []
        for word in sentence:
            if word in model.wv:
                vectors.append(model.wv[word])#If the word in the text exists in the W2V vocabulary, it assigns the vector 
        if vectors:
            return np.mean(vectors, axis=0)#Takes the mean of the vectors for that referral
        else:
            return np.zeros(model.vector_size) #if it can't find 
        
    alertP1['word2vec_feature'] = alertP1['clean_text'].apply(lambda x: get_sentence_vector(x)) #assigning w2v to the correct columns.
    return(alertP1)


