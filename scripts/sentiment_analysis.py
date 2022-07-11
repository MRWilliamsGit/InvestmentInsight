import sys
#!{sys.executable} -m pip install -r requirements.txt
from scripts.data_tools import make_sent_cloud
import nltk
import numpy as np
import pandas as pd
import pickle
import pprint
import reddit_helper
import os
import re

from tqdm import tqdm
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.corpus import stopwords


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



#Loughran McDonald Sentiment Word Lists to do sentiment analysis on Reddit posts
import os

#Of the 7 available sentiments, only 3 are used: negative, postive, and uncertainty
sentiments = ['negative', 'positive', 'uncertainty']

sentiment_df = pd.read_csv(os.path.join('..', '..', 'data', 'project_5_loughran_mcdonald', 'loughran_mcdonald_master_dic_2016.csv'))
sentiment_df.columns = [column.lower() for column in sentiment_df.columns] # Lowercase the columns for ease of use

# Remove unused information
sentiment_df = sentiment_df[sentiments + ['word']]
sentiment_df[sentiments] = sentiment_df[sentiments].astype(bool)
sentiment_df = sentiment_df[(sentiment_df[sentiments]).any(1)]

# Apply the same preprocessing to these words as the Reddit words
sentiment_df['word'] = lemmatize_words(sentiment_df['word'].str.lower())
sentiment_df = sentiment_df.drop_duplicates('word')


sentiment_df.head()

#Bag of Words
#Generate sentiment bag of words from Reddit threads

from collections import defaultdict, Counter
from sklearn.feature_extraction.text import CountVectorizer

#Generate a bag of words that counts the number of sentiment words in each Reddit post
def get_bag_of_words(sentiment_words, docs):
    vec = CountVectorizer(vocabulary=sentiment_words)
    vectors = vec.fit_transform(docs)
    words_list = vec.get_feature_names()
    bag_of_words = np.zeros([len(docs), len(words_list)])
    
    for i in range(len(docs)):
        bag_of_words[i] = vectors[i].toarray()[0]

    return bag_of_words.astype(int)


#Using get_bag_of_words function, generate a bag of words for all the Reddit threads

sentiment_bow_posts = {}

for ticker, posts in posts_by_ticker.items():
    lemma_docs = [' '.join(ten_k['file_lemma']) for post in posts]
    
    sentiment_bow_posts[ticker] = {
        sentiment: get_bag_of_words(sentiment_df[sentiment_df[sentiment]]['word'], lemma_docs)
        for sentiment in sentiments}


#Jaccard Similarity
#From Bag of Words calculate jaccard similarity and plot over time

from sklearn.metrics import jaccard_similarity_score

def get_jaccard_similarity(bag_of_words_matrix):
    jaccard_similarities = []
    bag_of_words_matrix = np.array(bag_of_words_matrix, dtype=bool)
    
    for i in range(len(bag_of_words_matrix)-1):
            u = bag_of_words_matrix[i]
            v = bag_of_words_matrix[i+1]
            jaccard_similarities.append(jaccard_similarity_score(u,v))    
    
    return jaccard_similarities

Using  get_jaccard_similarity function, plot similarities over time
# Get dates for the universe
file_dates = {
    ticker: [post['file_date'] for post in posts]
    for ticker, posts in posts_by_ticker.items()}  

jaccard_similarities = {
    ticker: {
        sentiment_name: get_jaccard_similarity(sentiment_values)
        for sentiment_name, sentiment_values in post_sentiments.items()}
    for ticker, post_sentiments in sentiment_bow_posts.items()}


reddit_helper.plot_similarities(
    [jaccard_similarities[example_ticker][sentiment] for sentiment in sentiments],
    file_dates[example_ticker][1:],
    'Jaccard Similarities for {} Sentiment'.format(example_ticker),
    sentiments)


#TF-IDF 
# Using the sentiment word lists to generate sentiment TF-IDF from Reddit posts
from sklearn.feature_extraction.text import TfidfVectorizer


def get_tfidf(sentiment_words, docs):
    vec = TfidfVectorizer(vocabulary=sentiment_words)
    tfidf = vec.fit_transform(docs)
    
    return tfidf.toarray()

#Generate TF-IDF for all Reddit posts
sentiment_tfidf_posts = {}

for ticker, posts in posts_by_ticker.items():
    lemma_docs = [' '.join(ten_k['file_lemma']) for post in posts]
    
    sentiment_tfidf_posts[ticker] = {
        sentiment: get_tfidf(sentiment_df[sentiment_df[sentiment]]['word'], lemma_docs)
        for sentiment in sentiments}

    
reddit_helper.print_post_data([sentiment_tfidf_posts[example_ticker]], sentiments)

#Cosine Similarity
#Use TF-IDF values to calculate the cosine similarity and plot over time

from sklearn.metrics.pairwise import cosine_similarity


def get_cosine_similarity(tfidf_matrix):
    cosine_similarities = []    
    
    for i in range(len(tfidf_matrix)-1):
        cosine_similarities.append(cosine_similarity(tfidf_matrix[i].reshape(1, -1),tfidf_matrix[i+1].reshape(1, -1))[0,0])
    
    return cosine_similarities

#Plot Cosine similariites over time
cosine_similarities = {
    ticker: {
        sentiment_name: get_cosine_similarity(sentiment_values)
        for sentiment_name, sentiment_values in post_sentiments.items()}
    for ticker, post_sentiments in sentiment_tfidf_posts.items()}


reddit_helper.plot_similarities(
    [cosine_similarities[example_ticker][sentiment] for sentiment in sentiments],
    file_dates[example_ticker][1:],
    'Cosine Similarities for {} Sentiment'.format(example_ticker),
    sentiments)


#Alpha Factors Against Cosine Similarities
#Get Daily Pricing, since Reddit posts are generated within seconds 
pricing = pd.read_csv( , parse_dates=['date'])
pricing = pricing.pivot(index='date', columns='ticker', values='adj_close')

pricing


#Dict to DataFrame
#The alphalens library uses dataframes need to convert  dictionary into df

cosine_similarities_df_dict = {'date': [], 'ticker': [], 'sentiment': [], 'value': []}


for ticker, post_sentiments in cosine_similarities.items():
    for sentiment_name, sentiment_values in post_sentiments.items():
        for sentiment_values, sentiment_value in enumerate(sentiment_values):
            cosine_similarities_df_dict['ticker'].append(ticker)
            cosine_similarities_df_dict['sentiment'].append(sentiment_name)
            cosine_similarities_df_dict['value'].append(sentiment_value)
            cosine_similarities_df_dict['date'].append(file_dates[ticker][1:][sentiment_values])

cosine_similarities_df = pd.DataFrame(cosine_similarities_df_dict)
cosine_similarities_df['date'] = pd.DatetimeIndex(cosine_similarities_df['date']).year
cosine_similarities_df['date'] = pd.to_datetime(cosine_similarities_df['date'], format='%Y')


cosine_similarities_df.head()


#Alphalens Format - Align indices 
import alphalens as al


factor_data = {}
skipped_sentiments = []

for sentiment in sentiments:
    cs_df = cosine_similarities_df[(cosine_similarities_df['sentiment'] == sentiment)]
    cs_df = cs_df.pivot(index='date', columns='ticker', values='value')
    
    try:
        data = al.utils.get_clean_factor_and_forward_returns(cs_df.stack(), pricing.loc[cs_df.index], quantiles=5, bins=None, periods=[1])
        factor_data[sentiment] = data
    except:
        skipped_sentiments.append(sentiment)

if skipped_sentiments:
    print('\nSkipped the following sentiments:\n{}'.format('\n'.join(skipped_sentiments)))
factor_data[sentiments[0]].head()

#Convert time to unix timestamp 

unixt_factor_data = {
    factor: data.set_index(pd.MultiIndex.from_tuples(
        [(x.timestamp(), y) for x, y in data.index.values],
        names=['date', 'asset']))
    for factor, data in factor_data.items()}

#Factor returns
#postive sentiment should be moving up and to the right
#negative sentiment should be moving down and to the right
#uncertainty sentiment shouldn't move much

ls_factor_returns = pd.DataFrame()

for factor_name, data in factor_data.items():
    ls_factor_returns[factor_name] = al.performance.factor_returns(data).iloc[:, 0]

(1 + ls_factor_returns).cumprod().plot()

# Basis Points Per Day per Quantile
qr_factor_returns = pd.DataFrame()

for factor_name, data in unixt_factor_data.items():
    qr_factor_returns[factor_name] = al.performance.mean_return_by_quantile(data)[0].iloc[:, 0]

(10000*qr_factor_returns).plot.bar(
    subplots=True,
    sharey=True,
    layout=(5,3),
    figsize=(14, 14),
    legend=False)

#Turnover Anlysis using Factor Rank Autocorrelation

ls_FRA = pd.DataFrame()

for factor, data in unixt_factor_data.items():
    ls_FRA[factor] = al.performance.factor_rank_autocorrelation(data)

ls_FRA.plot(title="Factor Rank Autocorrelation")

#Sharpe Ratio of the Alphas
daily_annualization_factor = np.sqrt(252)

(daily_annualization_factor * ls_factor_returns.mean() / ls_factor_returns.std()).round(2)


