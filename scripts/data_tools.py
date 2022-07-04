import string
import spacy
import re
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.cli.download import download

def makecloud(posts_df):
    
    #extract title and post body
    #(could eventually add more weight to titles?)
    titles = posts_df['title']
    body = posts_df['content']

    #combine in one text block
    textblock = ''
    for i in range(len(titles)):
        textblock = textblock+titles[i]
        textblock = textblock+body[i]

    # remove links
    textblock = re.sub('http[s]?://\S+', '', textblock)
    
    #return block
    return textblock

def maketitlecloud(posts_df):
    #extract title and post body
    #(could eventually add more weight to titles?)
    titles = posts_df['title']
    body = posts_df['content']

    #combine titles in one text block
    textblock = ''
    for this in titles:
        textblock = textblock+this
    
    #return block
    return textblock

def token_word(textblock):
    # feed text into spacy
    #download('en_core_web_sm')
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(textblock)
    # Get tokens
    tokens = [token for token in doc]
    # Extract the lemmas for each token
    tokens = [token.lemma_.lower().strip() for token in tokens]
    # remove stopwords and punctuation
    stopwords = set(STOP_WORDS)
    punctuations = string.punctuation
    tokens = [token for token in tokens if token.lower() not in stopwords and token not in punctuations]

    print(tokens)