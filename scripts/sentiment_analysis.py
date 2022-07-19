import re
import nltk
import pandas as pd
from collections import Counter
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# Sentiment Analysis Class
class Sentiment:
    # Init function
    def __init__(self):
        nltk.download("stopwords")
        nltk.download("wordnet")
        nltk.download("omw-1.4")

        return

    def data_prep(self, posts_df):
        # add titles and post bodies together
        textblock = ""
        for i in range(len(posts_df)):
            textblock = (
                textblock
                + " "
                + posts_df["title"][i + 1]
                + " "
                + posts_df["content"][i + 1]
            )

        # remove links, etc.
        textblock = re.sub(r"http\S+", "", textblock)
        textblock = re.sub("&amp;#x200B;", "", textblock)
        gone = "[]//\\()"
        for g in gone:
            textblock = textblock.replace(g, "")
        textblock = textblock.replace("\n", " ")

        # lowercase
        textblock = textblock.lower()

        # lemmatize
        words = textblock.split()
        lemmatized_words = [WordNetLemmatizer().lemmatize(word, "v") for word in words]

        # remove stopwords
        all_stopwords = stopwords.words("english")
        lemmatized_words = [
            word for word in lemmatized_words if not word in all_stopwords
        ]

        return lemmatized_words

    def get_sent(self, lemmatized_words):

        # Create sentiment list
        sentiment_list = []

        # Read sentiment csv into dataframe
        sentiment_df = pd.read_csv(
            "https://raw.githubusercontent.com/MRWilliamsGit/SocialMediaNLP/main/data/LM-SA-2020.csv"
        )

        # Create dictionary of words to sentiments
        sentiment_dict = dict(list(zip(sentiment_df.word, sentiment_df.sentiment)))

        # Loop through words and check if they are in lemmatized_words. then append to list
        for word in sentiment_dict.keys():
            if word in lemmatized_words:
                sentiment_list.append(sentiment_dict[word])

        # Get counts of sentiments we care about (Positive, Negative, Uncertainty)
        sentiment_counter = Counter(sentiment_list)

        # Convert sentiment_counter dict to df for bar graph output
        sentiment_counter_df = pd.DataFrame({"Frequency": sentiment_counter})

        # Return highest sentiment based on lemmatized words
        sentiment_max = max(sentiment_counter.items(), key=lambda pair: int(pair[1]))

        # Return the count of sentiments and the most frequent sentiment for lemmatized words
        return sentiment_counter_df, sentiment_max[0]  # , score