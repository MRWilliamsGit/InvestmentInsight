# InvestmentInsight
Individual lay investors often don't have the time or expertise to properly research stock options and make informed buying decisions. They easily fall into the trap of following the general consensus, when the best returns are always obtained through doing the opposite of the crowd.

To speed up the research process and dampen the effect of general sentiment, this project uses Natural Language Processing to summarize Reddit posts and identify sentiments related to specific stock tickers. It then reminds investors to behave opposite  the market, to "buy when others are selling and sell when others are buying."

## Data
Data is sourced from Reddit using the Reddit API. 

100 posts related to a user-selected stock ticker are collected and then filtered to those tagged as "Company News" or "News". The posts are cleaned and pre-processed by removing links and special characters. For sentiment analysis, the posts are further processed by removing stop-words and lemmatizing.

## Sentiment Analysis
Sentiment analysis is conducted using the Loughran-McDonald Sentiment Word List, a popular finance word-to-sentiment mapping repository. The frequency of sentiment-carrying words in the Reddit posts are simply tallied, and the sentiment with the most related words is returned as the general sentiment. 

## Summarization
Summarization is performed by a pre-trained [DistilBART model](https://huggingface.co/sshleifer/distilbart-cnn-12-6). BART uses bi-directional encoding like BERT, but causal decoding like GPT​, and generally outperforms BERT in summarization tasks.

## Explainability
A graph of sentiment-carrying word frequency is also displayed through the User Interface, so that investors can note how strong the sentiment is.

Note: this project makes use of the terms "bullish" and "bearish":
* 🐂 Bullish: Postive sentiment in which investors believe a stock or the broader market will appreciate in value
* 🐻 Bearish: Negative sentiment in which investors believe a stock or the broader market will depreciate in   value

## Public Deployment
Please enjoy interacting with this tool through its public app:
https://mrwilliamsgit-socialmedianlp-main-yx3u2h.streamlitapp.com/

## Local Deployment
1. First obtain Reddit API developer access.
2. Clone this repository to your local environment and add an additional folder named '.streamlit' (note the period).
3. In this folder, add a .toml file named 'secrets.toml' with these necessary details. Note: grant_type will remain the literal word 'password'.
```
CLIENT_ID = 'abcdef'
SECRET_KEY = 'abcdef'
grant_type = 'password'
username = 'abcdef'
password = 'abcdef'
```
4. Now that you have the crednentials you need, install the dependancies to your local environment.
```
pip install -r requirements.txt
```
5. To run the app locally, use the command line terminal.
```
streamlit run main.py
```

### Citation
[1] R. Adusumilli, [NLP in the Stock Market](/https://github.com/roshan-adusumilli/nlp_10-ks)

```
@InProceedings{NLP_on_Financial_Statements,
  author    = {Roshan Adusumilli},
  title     = {NLP in the Stock Market},
  year      = {2020},
  publisher = {GitHub},
  journal   = {GitHub repository},
  url       = {https://github.com/roshan-adusumilli/nlp_10-ks}
}
```
