import string
import spacy
import re
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.cli.download import download
import sys
# CB 7.12 - Is this needed? 
#!{sys.executable} -m pip install -r requirements.txt

import nltk
import numpy as np
import pandas as pd
import pickle
import pprint
import os

from tqdm import tqdm
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import defaultdict, Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import jaccard_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# params: df of post info returned from API
# returns: text block of body text
def makecloud(posts_df):
    #add titles and post bodies together
    textblock = ''
    for i in range(len(posts_df)):
        textblock = textblock + " " + posts_df['title'][i+1] + ' ' + posts_df['content'][i+1]

    #remove links, etc.
    textblock = re.sub(r'http\S+', '', textblock)
    textblock = re.sub("&amp;#x200B;", '', textblock)
    gone = '[]()'
    for g in gone:
        textblock = textblock.replace(g, '')
    textblock = textblock.replace("\n", ' ')
    
    #return block
    return textblock

# params: df of post info returned from API
# returns: text block of title text
def maketitlecloud(posts_df):
    #extract title and post body
    #(could eventually add more weight to titles?)
    titles = posts_df['title']
    body = posts_df['content']

    #combine titles in one text block
    textblock = ''
    for this in titles:
        textblock = textblock+this
    
    #return block
    return textblock

# params: df of post info returned from API
# returns: list of text blocks of titles and text
def make_cloud_chunks(posts_df):

    chunk_size = 1000
    textblock = []

    #go post by post and add together in chunks that are less than 1024 words
    for i in range(len(posts_df)):
        #combine post and title
        post = posts_df['title'][i+1] + ' ' + posts_df['content'][i+1]
        #remove links, etc.
        post = re.sub(r'http\S+', '', post)
        post = re.sub("&amp;#x200B;", '', post)
        gone = '[]//\\()'
        for g in gone:
            post = post.replace(g, '')
        post = post.replace("\n", ' ')
        #if it's too long, chunk it
        if len(post.split(" "))>chunk_size:
            wds = post.split(" ")
            nchunks = int(len(wds)/chunk_size) + (len(wds) % chunk_size > 0)
            lchunks = int(len(wds)/nchunks) + (len(wds) % nchunks > 0)
            chunked = [wds[i:i+lchunks] for i in range(0,len(wds),lchunks)]
            for c in range(len(chunked)):
                chunked[c]= ' '.join(chunked[c])
        else:
            chunked = [post]

        #add the chunk(s) to textblock
        for c in chunked:
            if len(textblock)==0:
                textblock.append(c)
            else:
                chunkq = textblock[len(textblock)-1] + " " + c
                if len(chunkq.split()) < chunk_size:
                    textblock[len(textblock)-1] = chunkq
                else:
                    textblock.append(c)

    return textblock

def token_word(textblock):
    # feed text into spacy
    #download('en_core_web_sm')
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(textblock)
    # Get tokens
    tokens = [token for token in doc]
    # Extract the lemmas for each token
    tokens = [token.lemma_.lower().strip() for token in tokens]
    # remove stopwords and punctuation
    stopwords = set(STOP_WORDS)
    punctuations = string.punctuation
    tokens = [token for token in tokens if token.lower() not in stopwords and token not in punctuations]

    print(tokens)

# params: df of post info returned from API
# returns: text block of body text
def make_sent_cloud(posts_df):
    #add titles and post bodies together
    textblock = ''
    for i in range(len(posts_df)):
        textblock = textblock + " " + posts_df['title'][i+1] + ' ' + posts_df['content'][i+1]

    #remove links, etc.
    textblock = re.sub(r'http\S+', '', textblock)
    textblock = re.sub("&amp;#x200B;", '', textblock)
    gone = '[]()'
    for g in gone:
        textblock = textblock.replace(g, '')
    textblock = textblock.replace("\n", ' ')
    
    return textblock


#Sentiment Analysis

#NLP Corpora:
#stopwords corpus for removing stopwords & wordnet for lemmatizing
def nlp_corpus():
    nltk.download('stopwords')
    nltk.download('wordnet')

    return

#Preprocess Summary 
def get_summary(textblock):
    textblock = textblock.lower
    textblock = textblock.lower

    return textblock

#Lemmatize Summary
def lemmatize_words_words(words):
    lemmatized_words = [WordNetLemmatizer().lemmatize(word, 'v') for word in words]

    return lemmatized_words

#Remove Stopwords
def remove_stopwords(summary):
    all_stopwords = stopwords.words('english')

    text_tokens = word_tokenize(summary)
    tokens_without_sw = [word for word in text_tokens if not word in all_stopwords]
    return tokens_without_sw

#Loughran McDonald Sentiment Word Lists to do sentiment analysis on Reddit posts
#Of the 7 available sentiments, only 3 are used: negative, postive, and uncertainty
def mcdonald():
    sentiment_words = ['negative', 'positive', 'uncertainty']

    return sentiment_words

#Bag of Words
#Generate sentiment bag of words from Reddit threads

#Generate a bag of words that counts the number of sentiment words in each Reddit post
def get_bag_of_words(sentiment_words, posts):
    vec = CountVectorizer(vocabulary=sentiment_words)
    vectors = vec.fit_transform(posts)
    words_list = vec.get_feature_names()
    bag_of_words = np.zeros([len(posts), len(words_list)])
    
    for i in range(len(posts)):
        bag_of_words[i] = vectors[i].toarray()[0]

    return bag_of_words.astype(int)

#TF-IDF 
# Using the sentiment word lists to generate sentiment TF-IDF from Reddit posts
def get_tfidf(sentiment_words, posts):
    vec = TfidfVectorizer(vocabulary=sentiment_words)
    tfidf = vec.fit_transform(docs)
    
    return tfidf.toarray()

#Cosine Similarity
#Use TF-IDF values to calculate the cosine similarity 
def get_cosine_similarity(posts_df):
    cosine_similarities = []    
    
    # 7/15 - Update 'insert header' with whatever header is in posts_df
    for i in range(len(posts_df)-1):
        cosine_similarities.append(df.loc[df.index[i], 'insert header'])
    
    count_vectorizer = CountVectorizer(stop_words='english')
    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(cosine_similarities)

    print(cosine_similarity(sparse_matrix, sparse_matrix))
    
    return 