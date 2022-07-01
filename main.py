from scripts.API_tools import access_API, API_request
from scripts.data_tools import makecloud
from scripts.summary_classes import ExFinSummarizer, GenFinSummarizer


def main():

    searchterm = "AAPL"

    headers = access_API()
    df = API_request(headers, searchterm)
    block = makecloud(df)

    # generative summarization
    # gfs = GenFinSummarizer()
    # output = gfs.summarize(block)

    # extractive summarization
    efs = ExFinSummarizer()
    output = efs.summarize(block, top_n=5)

    print(output)


if __name__ == "__main__":
    main()
