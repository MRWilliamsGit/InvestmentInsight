#from bs4 import BeautifulSoup
#from sentence_transformers import SentenceTransformer, util
#import numpy as np
#import requests
#from transformers import pipeline
#import nltk
#from nltk.corpus import stopwords

import pandas as pd
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from callreddit import callreddit

#pre-process text
def gettext():
    #get text
    df = callreddit()

    #extract title and post body
    #(could eventually add more weight to titles?)
    titles = df['title']
    body = df['content']

    #combine in one text block
    #print(df.iloc[2])
    text = ''
    for this in body:
        text = text+this

    #print(text)
    return text

#get model and tokenizer once
def getmodel():
    print("Downloading Model...")
    model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")
    tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
    print("Download Complete")
    return model, tokenizer

def summarize():
    text = gettext()
    model, tokenizer = getmodel()

    input_ids = tokenizer.encode(text, return_tensors="pt", truncation=True, max_length=1024)
    output = model.generate(
        input_ids,
        max_length=200,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id,
    )
    
    output = tokenizer.decode(output[0])

    print(output)
    return output

summarize()