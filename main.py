from scripts.API_tools import access_API, API_request
from scripts.data_tools import makecloud, maketitlecloud, make_cloud_chunks
from scripts.summary_classes import ExFinSummarizer, GenFinSummarizer
import pandas as pd
import streamlit as st


def main():

    st.title("Stock Support")

    which = st.radio("",("Generative Summary","Extractive Summary"),)
    st.write("<style>div.row-widget.stRadio > div{flex-direction:row;}</style>",unsafe_allow_html=True,)

    searchterm = st.text_input("Enter a stock name. Ex: AAPL, NVDA, AMZN", ' ')

    if searchterm != ' ':
        #get reddit posts
        #searchterm = "SSNLF"
        df = API_request(searchterm)
        #print(len(df))
        st.write("Number of news posts found: ", len(df))

        if which == "Generative Summary":
            # generative summarization
            # length = the length of summary to return for each text chunk
            text_list = make_cloud_chunks(df)
            gfs = GenFinSummarizer()
            output = gfs.summarize(text_list, length=400)
            #print(output)
            st.write(output)
        else:
            # extractive summarization
            # top_n = the number of sentences to extract
            block = makecloud(df)
            efs = ExFinSummarizer()
            output = efs.summarize(block, top_n=5)
            #print(output)
            st.write(output)

if __name__ == "__main__":
    main()
