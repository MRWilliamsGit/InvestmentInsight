# Making Cents Out of Nonsense: <br> Applying NLP to Reddit for an Investment Edge
 ![image](https://user-images.githubusercontent.com/78511177/176003905-7eed8447-4bd7-43d5-98d0-ed475fe48a73.png)

#### AIPI 540 Deep Learning Applications
#### Project by: Colin Bryan, Maria Williams, and Derrick Adam
#### Project Structure: Natural Language Processing Module
#### Category: Social Media & News
#### Steamlit Application: [Link](https://mrwilliamsgit-socialmedianlp-main-yx3u2h.streamlitapp.com/)

Motivation
----------
"The non-consensus idea is the only way to achieve extraordinary results in *anything*." - Doug Clinton
<br>
<br>
Main St. vs. Wall St. - Pushing Back Against the Establishment 
<br>
![main](https://user-images.githubusercontent.com/78511177/178585851-20285751-0a5d-4ada-9ffb-9a4dddf7cbd8.png)
<br> 
<br> In January 2021, GameStop, an American video game retailer, experienced a short squeeze initiated by Reddit's subreddit r/wallstreetbets. Reddit is a social news website that started the retail vs. establishment movement in investments. Since then, Reddit and subreddits like r/wallstreetbets has transformed into a platform for sharing investment recommendations and discussion. 
<br>
* As the number of market participants increase so will the demand for alternative data sources to generate alpha (above market returns)
* Unconventional data can provide insights that other market participants haven't considered
* Investors who use the same resources can only achieve the ordinary. Only the non-consensus investor can yield the *extraordinary* 
<img width="602" alt="Gamestop " src="https://user-images.githubusercontent.com/78511177/178586080-3208a474-91a1-4cd6-8b06-0865e3b5de75.png">
(Source: Marketwatch)

Problem Statement
-----------------
* The objective of the project is to convert informal text from subreddits like, r/wallstreetbets, into formalized, bite-sized bits from which everyday, retail investors can make informed, actionable trades. 
* Generally, retail investors, don't have the time, the requisite psychological framework to deal with the vicissitudes of markets, and the financial background to parse through troves of information to make thoughtful investment decisions. The interactive Streamlit platform abstracts all of this away and provides value to the end user in the following ways:

    1) Users input a stock ticker and the model will compile relevant news threads regarding that stock to curate a generative summary

    2) Sentiment analysis will label the news aggregation as postive, negative, or uncertain

    3) Given that non-consensus investing yields superior returns, the platform will generate a buy reommendation when the sentiment is negative, a sell signal when the sentiment is negative, and do nothing when the sentiment is uncertain

Getting Started
---------------
1. To run locally: Clone the repository, create a virtual environment, and install the requirements needed to run the application
```
pip install -r requirements.txt
```
2. Download the nltk modules required to run the application by following these steps:
```
python 
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('vader_lexicon')
```
3. Start the Streamlit app
```
streamlit run main.py
```

Data Sourcing, Processing, & Modeling
-------------------------------------
* Data is sourced from the Reddit API when a user enters a stock's ticker on the Streamlit User Interface in the following steps:

     1) API queries Reddit for the search term
    
     2) Retrieves the 100 most recent posts related to the search term and returns posts categorized as "Company           News" or "News" as a dataframe
     
     3) If "News" posts aren't found, the user is prompted to enter a new search term. If "News" posts are found,         the following steps happen under the hood:
     
           * The Reddit posts are put through a data pipeline extracting phrases from the title and content of                  the posts. This process is called "chunking" 
           
           * From analyzing all of the returned posts by passing the text chunks through a generative summary                  model that summary is rendered onto the User Interface 
           
           * Sentiment analysis is conducted by lemmatizing the Reddit posts and returning a list of lemmatized                words from the posts. This list is then compared to the Loughran-McDonald Sentiment Word List, a                  popular finance word-to-sentiment mapping repository, to understand the frequency of sentiment-                    carrying words that occur in each Reddit post that is processed
           
           * A count of the frequency of sentiment-carrying words in the Reddit posts for the queried stock                    ticker is conducted and used to make a recommendation on buying, selling, or waiting on the stock. A              graph of sentiment-carrying word frequency is also displayed through the User Interface

Adavantages of Deep Learning vs. Non-Deep in Finance
---------------
NLP is better at creating structure out of unstructured data and recognizing finance jargon

NLP enriches decision-making in the following ways:

     1) Automation: Replace manual process or turning unstructured data into a more usabble form i.e. automating             capture of earnings calls
    
     2) Data Enrichment: Add context to captured, unstructered data to make it more searchable and actionable i.e.           searching for a particular topic in an earnings call
     
     3) Search and Discovery: Create a competitive advantage from a variety of sources
     
     (Source: MIT Sloan School of Management)



Model Evaluation & Results
----------------------------

* The tool works best for popular stocks on Reddit
* For stocks with less trading volume, "News" posts often do not exist or the ticker is mistaken for a different topic on Reddit
* For best results, search for more popular assets, like blue-chip stocks

Results Based on Sentiment Analysis:

Suggested Buy Signal


<img width="434" alt="Screen Shot 2022-07-19 at 6 14 19 PM" src="https://user-images.githubusercontent.com/78511177/179857576-74286598-141e-42b3-8d66-b09eeb82ded7.png">

<br>

Suggested Sell Signal


<img width="432" alt="Screen Shot 2022-07-19 at 6 16 44 PM" src="https://user-images.githubusercontent.com/78511177/179857811-b1fa053f-c93e-4ed6-a252-1ba75c7fe814.png">

Streamlit Demonstration on Coinbase (Ticker: COIN)
<br>
<br>
Ticker Search:

https://user-images.githubusercontent.com/78511177/180041852-69e2c8a4-5031-49f7-97a6-21f5d6bc673e.mp4

Summary Generation:



https://user-images.githubusercontent.com/78511177/180041893-c5568833-a517-4893-b632-5d11305b42e0.mp4







Future Work
------------
* Improve the query passed to the Reddit API to ensure only stock-related posts are returned
* Generate more posts for both popular and less popular tickers
* Apply weights to the posts based on the subreddit where the post is found (e.g., r/wallstreetbets, r/stocks, r/superstonk, r/personalfinance, r/investing, etc.)
* Expand support for alternative asset classes, like cryptocurrencies and commodities
* Enable cross-platform support for phone and tablet
* Allow for scale: multiple users across devices should simultaneously be able to generate results


Conclusion
----------
"Be fearful when others are greedy. Be greedy when others are fearful." - Warren Buffett
* Being non-concensus in the way one invests is the only way to generate superior returns 
* Using non-traditional data sources, like Reddit, have come into vogue and came help all types of investors glean insights they would not otherwise have readily available
* By coupling technology and discipline, retail investors can level the playing field and even beat financial institutions at their own game

Additional Resources
--------------------
* NLP in the Stock Market - Project by Roshan Adusumilli: [here](https://towardsdatascience.com/nlp-in-the-stock-market-8760d062eb92#:~:text=Machine%20learning%20models%20implemented%20in,forms%20to%20forecast%20stock%20movements.)

* Loughran McDonald-SA-2020 Sentiment Word List: [here](https://researchdata.up.ac.za/articles/dataset/Loughran_McDonald-SA-2020_Sentiment_Word_List/14401178)

* Famed Investor Howard Marks' Memo on Non-Consensus Investing: [here](https://www.oaktreecapital.com/docs/default-source/memos/1993-02-15-the-value-of-predictions-or-where-39-d-all-this-rain-come-from.pdf?sfvrsn=6fbc0f65_2)


Citation
--------
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
