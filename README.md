# Making Cents Out of Nonsense -
# Applying NLP to Reddit for an Investment Edge
 ![image](https://user-images.githubusercontent.com/78511177/176003905-7eed8447-4bd7-43d5-98d0-ed475fe48a73.png)

AIPI 540 Deep Learning Applications
<br> Natural Language Processing Module
<br> Project by: Colin Bryan, Maria Williams, and Derrick Adam

[Streamlit Platform](https://mrwilliamsgit-socialmedianlp-main-yx3u2h.streamlitapp.com/)

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
* Investors who use the same resources can only achieve the ordinary. Only the non-concensus investor can yield the *extraordinary* 
<img width="602" alt="Gamestop " src="https://user-images.githubusercontent.com/78511177/178586080-3208a474-91a1-4cd6-8b06-0865e3b5de75.png">
(Source: Marketwatch)

Problem Statement
-----------------
* The objective of the project is to convert informal text from subreddits like, r/wallstreetbets, into formalized, bite-sized bits from which everyday, retail investors can make informed, actionable trades. 
* Generally, retail investors, don't have the time or financial acumen to parse through troves of information to make thoughtful investment decisions. The interactive Streamlit platform abstracts all of this away and provides value to the end user in the following ways:

    1) Users input a stock ticker and the model will compile relevant news threads regarding that stock to curate a generative summary

    2) Sentiment analysis will label the news aggregation as postive, negative, or neutral

    3) Given that non-concensus investing yields superior returns, the platform will generate a buy reommendation when the sentiment is negative, a sell signal when the sentiment is negative, and do nothing when the sentiment is uncertain

Getting Started
---------------
1. Clone the repository, create a virtual environment, and install the requirements needed to run the application
```
pip install -r requirements.txt
```
2. Download the nltk modules required to run the application
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
Project Structure: NLP Pipeline
-----------------

Data Sourcing & Processing
--------------------------

Modeling Details
----------------

Non-DL Discussion
---------------

Model Evaluation & Results
----------------------------

Future Work
------------

Conclusion
----------
"Be fearful when others are greedy. Be greedy when others are fearful." - Warren Buffett
* Being non-concensus in the way one invests is the only way to generate superior returns 
* Using non-traditional data sources, like Reddit, have come into vogue and came help all types of investors glean insights they would not otherwise have readily available
* With technology and the right mindset, retail investors can level the playing field and even beat financial institutions at their own game

Additional Resources
--------------------
* NLP in the Stock Market - Project by Roshan Adusumilli: [here](https://towardsdatascience.com/nlp-in-the-stock-market-8760d062eb92#:~:text=Machine%20learning%20models%20implemented%20in,forms%20to%20forecast%20stock%20movements.)

Notebooks
---------

License
-------

Citation
--------
@misc{NLP_on_Financial_Statements,
  author = {Roshan Adusumilli},
  title = {NLP in the Stock Market},
  year = {2020},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/roshan-adusumilli/nlp_10-ks}}
}
