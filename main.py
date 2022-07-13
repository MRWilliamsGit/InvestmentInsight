from scripts.API_tools import API_request
from scripts.data_tools import make_cloud_chunks
from scripts.summary_classes import GenFinSummarizer
from scripts.sentiment_analysis import Sentiment
import streamlit as st


def main():

    st.title("Stock Support")
    searchterm = st.text_input("Enter a stock name. Ex: AAPL, NVDA, AMZN", " ")

    if searchterm != " ":
        # get reddit posts
        df = API_request(searchterm)
        st.write("Number of news posts found: ", len(df))

        if len(df) < 1:
            st.error(
                "No Reddit news posts were found for this searchterm. Please try a different stock."
            )
        else:
            with st.spinner("Generating Summary"):
                # generative summarization
                # length = the length of summary to return for each text chunk
                text_list = make_cloud_chunks(df)
                gfs = GenFinSummarizer()
                output = gfs.summarize(text_list, length=400)
            st.write(output)

            # sentiment analysis
            sent = Sentiment()
            lemwords = sent.data_prep(df)
            sent.Derrick_get_sent(lemwords)

if __name__ == "__main__":
    main()
