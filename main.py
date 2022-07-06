from scripts.API_tools import access_API, API_request
from scripts.data_tools import makecloud, maketitlecloud
from scripts.summary_classes import ExFinSummarizer, GenFinSummarizer
import pandas as pd


def main():

    searchterm = "AAPL"

    headers = access_API()
    df = API_request(headers, searchterm)
    block = makecloud(df)
    #block = maketitlecloud(df)

    # generative summarization
    #returns 200 word summary
    gfs = GenFinSummarizer()
    output = gfs.summarize(block)

    # extractive summarization
    #top_n = the number of sentences to extract
    #efs = ExFinSummarizer()
    #output = efs.summarize(block, top_n=10)

    print(output)


if __name__ == "__main__":
    main()
