#https://github.com/roshan-adusumilli/nlp_10-ks/blob/master/NLP_on_Financial_Statements.ipynb

#from data_tools import make_sent_cloud, lemmatize_words_words
import nltk
import numpy as np
import pandas as pd
import pickle
import pprint
import string
import matplotlib.pyplot as plt
import os
import re

from tqdm import tqdm
from collections import Counter
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from collections import defaultdict, Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import jaccard_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#Sentiment Analysis Class
class Sentiment():
    def __init__(self):
        #Loughran McDonald Sentiment Word Lists to do sentiment analysis on Reddit posts
        #Of the 7 available sentiments, only 3 are used: negative, postive, and uncertainty
        sentiment_words = ['negative', 'positive', 'uncertainty']

        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        
    # params: df of post info returned from API
    # returns: list of lematized words
    def data_prep(self, posts_df):
        #add titles and post bodies together
        textblock = ''
        for i in range(len(posts_df)):
            textblock = textblock + " " + posts_df['title'][i+1] + ' ' + posts_df['content'][i+1]

        #remove links, etc.
        textblock = re.sub(r'http\S+', '', textblock)
        textblock = re.sub("&amp;#x200B;", '', textblock)
        gone = '[]//\\()'
        for g in gone:
            textblock = textblock.replace(g, '')
        textblock = textblock.replace("\n", ' ')

        #lowercase
        textblock = textblock.lower()

        #lemmatize
        words = textblock.split()
        lemmatized_words = [WordNetLemmatizer().lemmatize(word, 'v') for word in words]

        #remove stopwords
        all_stopwords = stopwords.words('english')
        lemmatized_words = [word for word in lemmatized_words if not word in all_stopwords]

        return lemmatized_words

    def Derrick_get_sent(self, lemmatized_words):

        sentiment_list = []
        # CB additions
        sentiment_df = pd.read_csv('data\LM-SA-2020.csv')

        sentiment_dict = dict(list(zip(sentiment_df.word, sentiment_df.sentiment)))
    
        for word in sentiment_dict.keys():
            if word in lemmatized_words:
                sentiment_list.append(sentiment_dict[word])
        
        # CB comment out
        # with open('data\LM-SA-2020.txt', 'r') as file:
        #     for line in file:
        #         print(line)
        #         #clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
        #         word, emotion = line.split(' ')

        #         if word in lemmatized_words:
        #             sentiment_list.append(emotion)

        print(sentiment_list)
        w = Counter(sentiment_list)
        print(w)

        score = SentimentIntensityAnalyzer().polarity_scores(self)
        if score['neg'] > score['pos']:
            print("Negative Sentiment")
        elif score['neg'] < score['pos']:
            print("Positive Sentiment")
        else:
            print("Uncertainty Sentiment")
        
        #sentiment_df = pd.read_csv('data\LM-SA-2020.csv')
        #sentiment_df.columns = [column.lower() for column in sentiment_df.columns] # Lowercase the columns for ease of use

        # Remove unused information
        #sentiment_df = sentiment_df[sentiments + ['word']]
        #sentiment_df[sentiments] = sentiment_df[sentiments].astype(bool)
        #sentiment_df = sentiment_df[(sentiment_df[sentiments]).any(1)]

        # Apply the same preprocessing to these words as the 10-k words
        #sentiment_df['word'] = lemmatize_words(sentiment_df['word'].str.lower())
        #sentiment_df = sentiment_df.drop_duplicates('word')

        return 

    # params:
    # returns:
    # Generate a bag of words that counts the number of sentiment words in each Reddit post
    # NOT YET TESTED
    def get_bag_of_words(sentiment_df, posts):

        vec = CountVectorizer(vocabulary=sentiment_df)
        vectors = vec.fit_transform(posts)
        words_list = vec.get_feature_names()
        bag_of_words = np.zeros([len(posts), len(words_list)])
        
        for i in range(len(posts)):
            bag_of_words[i] = vectors[i].toarray()[0]

        return bag_of_words.astype(int)

    #TF-IDF 
    #Using the sentiment word lists to generate sentiment TF-IDF from Reddit posts
    #NOT YET TESTED
    def get_tfidf(sentiment_words, posts):
        vec = TfidfVectorizer(vocabulary=sentiment_words)
        tfidf = vec.fit_transform(docs)
        
        return tfidf.toarray()

    #Jaccard Similarity
    #From Bag of Words calculate jaccard similarity 
    # NOT YET TESTED
    def get_jaccard_similarity(bag_of_words_matrix):
        jaccard_similarities = []
        bag_of_words_matrix = np.array(bag_of_words_matrix, dtype=bool)
        
        for i in range(len(bag_of_words_matrix)-1):
                u = bag_of_words_matrix[i]
                v = bag_of_words_matrix[i+1]
                jaccard_similarities.append(jaccard_score(u,v))    
        
        return jaccard_similarities


    #Cosine Similarity
    #Use TF-IDF values to calculate the cosine similarity 
    # NOT YET TESTED
    def get_cosine_similarity(tfidf_matrix):
        cosine_similarities = []    
        
        for i in range(len(tfidf_matrix)-1):
            cosine_similarities.append(cosine_similarity(tfidf_matrix[i].reshape(1, -1),tfidf_matrix[i+1].reshape(1, -1))[0,0])
        
        return cosine_similarities

    # params:
    # returns:
    # this should be the main function that runs everything necessary
    def get_sentiment(self, posts_df):
 
        lemlist = self.data_prep(posts_df)
        sentiment_df = self.get_sent_words()
        bag = self.get_bag_of_words(sentiment_df, lemlist)

        #Sentiment Analysis & Plot
        fig, ax1 = plt.subplots()
        ax1.bar(w.keys(), w.values())
        fig.autofmt_xdate()
        plt.savefig('graph.png')
        plt.show()

        #return ans

