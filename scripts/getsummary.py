#from bs4 import BeautifulSoup
#from sentence_transformers import SentenceTransformer, util
#import numpy as np
#import requests
#from transformers import pipeline
#import nltk
#from nltk.corpus import stopwords

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from callreddit import callreddit

#pre-process text
def gettext():
    #get text
    df = callreddit()

    #extract title and post body
    titles = df['title']
    body = df['content']

    return text

#get model and tokenizer once
def getmodel():
    print("Downloading Model...")
    model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")
    tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
    print("Download Complete")
    return model, tokenizer

def summarize():


    return summary