from scripts.API_tools import API_request
from scripts.data_tools import make_cloud_chunks
from scripts.summary_classes import GenFinSummarizer
from scripts.sentiment_analysis import Sentiment
import streamlit as st


def main():

    st.title("Reddit Stock Research Tool")
    searchterm = st.text_input("Enter a stock ticker. Ex: AAPL, MSFT, TSLA")

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
            st.header("Summary")
            st.write(output)

            ## sentiment analysis
            sent = Sentiment()
            lemwords = sent.data_prep(df)
            sentiment_counter, max_sentiment = sent.get_sent(lemwords)

            # Show analysis in UI
            st.header("Analysis")
            if max_sentiment == 'Negative':
                st.success("The sentiment is overly bearish, BUY the stock")
            elif max_sentiment == 'Positive':
                st.error("The sentiment is overly bullish, SELL the stock")
            else:
                st.warning("The sentiment is uncertain. Do nothing. Wait for the right catch.")

            # Show graph in UI
            st.header("Sentiment Graph")
            st.write("Sentiment analysis of key words")
            # CB 7.13 - Change to graph
            st.bar_chart(data=sentiment_counter, width=0, height=0, use_container_width=True)
            #st.write(sentiment_counter)


if __name__ == "__main__":
    main()
