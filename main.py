# Import functions, classes, and the streamlit library
from scripts.API_tools import API_request
from scripts.data_tools import make_cloud_chunks
from scripts.summary_classes import GenFinSummarizer
from scripts.sentiment_analysis import Sentiment
import streamlit as st

# Define main function
def main():

    # Streamlit title 
    st.title("Reddit Stock Research Tool")
    # Create search functionality
    searchterm = st.text_input("Enter a stock ticker. Ex: AAPL, MSFT, TSLA")

    # Execute search if it's not blank
    if searchterm != " ":
        # Use API_request function to get reddit news posts related to the search term
        df = API_request(searchterm)
        # Display number of news posts
        st.write("Number of news posts found: ", len(df))

        # If no news posts are found, tell the user to try a different stock ticker
        if len(df) < 1:
            st.error(
                "No Reddit news posts were found for this searchterm. Please try a different stock."
            )
        # If posts are found, generate summary and perform sentiment analysis
        else:
            with st.spinner("Generating Summary"):
                # Put reddit posts through text pipeline
                text_list = make_cloud_chunks(df)
                # Generate auto summary
                gfs = GenFinSummarizer()
                # Create output to display on UI
                output = gfs.summarize(text_list, length=400)
            # Display auto summary
            st.header("Summary")
            st.write(output)

            ## Perform Sentiment Analysis
            sent = Sentiment()
            # Lemmatize words
            lemwords = sent.data_prep(df)
            # Return the sentiment counter and most frequent sentiment from get_sent function 
            sentiment_counter_df, max_sentiment = sent.get_sent(lemwords)

            # Show analysis in UI
            st.header("Analysis")
            # If most frequent sentiment is negative, recommend to buy
            if max_sentiment == 'Negative':
                st.success("The sentiment is overly bearish, BUY the stock")
            # If most frequent sentiment is positive, recommend to sell
            elif max_sentiment == 'Positive':
                st.error("The sentiment is overly bullish, SELL the stock")
            # If most frequent sentiment is not positive or negative, don't make a recommendation
            else:
                st.warning("The sentiment is uncertain. Do nothing. Wait for the right catch.")

            # Show graph in UI of different sentiments
            st.header("Sentiment Graph")
            st.write("Sentiment analysis of key words by frequency of occurence")
            st.bar_chart(data=sentiment_counter_df, width=0, height=0, use_container_width=True)

# Execute main function
if __name__ == "__main__":
    main()
