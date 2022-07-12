from scripts.API_tools import access_API, API_request
from scripts.data_tools import makecloud, maketitlecloud
from scripts.summary_classes import ExFinSummarizer, GenFinSummarizer
import pandas as pd
import nltk
import numpy as np
import pandas as pd
import pickle
import pprint
import reddit_helper
import os

from tqdm import tqdm


def main():

    searchterm = "AAPL"

    headers = access_API()
    df = API_request(headers, searchterm)
    block = makecloud(df)
    #block = maketitlecloud(df)

    # generative summarization
    # returns 200 word summary
    gfs = GenFinSummarizer()
    output = gfs.summarize(block)
    sentiment = data_prep(self, output)

    # extractive summarization
    #top_n = the number of sentences to extract
    #efs = ExFinSummarizer()
    #output = efs.summarize(block, top_n=10)

    print(sentiment)


if __name__ == "__main__":
    main()
