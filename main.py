from scripts.API_tools import access_API, API_request
from scripts.data_tools import makecloud, maketitlecloud, make_cloud_chunks
from scripts.summary_classes import ExFinSummarizer, GenFinSummarizer
import pandas as pd


def main():

    #get reddit posts
    searchterm = "SSNLF"
    df = API_request(searchterm)
    print(len(df))

    # generative summarization
    # length = the length of summary to return for each text chunk
    text_list = make_cloud_chunks(df)
    gfs = GenFinSummarizer()
    output = gfs.summarize(text_list, length=400)
    print(output)

    # extractive summarization
    # top_n = the number of sentences to extract
    block = makecloud(df)
    efs = ExFinSummarizer()
    output = efs.summarize(block, top_n=5)
    print(output)


if __name__ == "__main__":
    main()
