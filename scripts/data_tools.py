import string
import spacy
import re
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.cli.download import download

# params: df of post info returned from API
# returns: text block of body text
def makecloud(posts_df):
    #add titles and post bodies together
    textblock = ''
    for i in range(len(posts_df)):
        textblock = textblock + " " + posts_df['title'][i+1] + ' ' + posts_df['content'][i+1]

    #remove links, etc.
    textblock = re.sub(r'http\S+', '', textblock)
    textblock = re.sub("&amp;#x200B;", '', textblock)
    gone = '[]()'
    for g in gone:
        textblock = textblock.replace(g, '')
    textblock = textblock.replace("\n", ' ')
    
    #return block
    return textblock

# params: df of post info returned from API
# returns: text block of title text
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

# params: df of post info returned from API
# returns: list of text blocks of titles and text
def make_cloud_chunks(posts_df):

    chunk_size = 1000
    textblock = []

    #go post by post and add together in chunks that are less than 1024 words
    for i in range(len(posts_df)):
        #combine post and title
        post = posts_df['title'][i+1] + ' ' + posts_df['content'][i+1]
        #remove links, etc.
        post = re.sub(r'http\S+', '', post)
        post = re.sub("&amp;#x200B;", '', post)
        gone = '[]()'
        for g in gone:
            post = post.replace(g, '')
        post = post.replace("\n", ' ')
        #if it's too long, chunk it
        if len(post.split(" "))>chunk_size:
            wds = post.split(" ")
            nchunks = int(len(wds)/chunk_size) + (len(wds) % chunk_size > 0)
            lchunks = int(len(wds)/nchunks) + (len(wds) % nchunks > 0)
            chunked = [wds[i:i+lchunks] for i in range(0,len(wds),lchunks)]
            for c in range(len(chunked)):
                chunked[c]= ' '.join(chunked[c])
        else:
            chunked = [post]

        #add the chunk(s) to textblock
        for c in chunked:
            if len(textblock)==0:
                textblock.append(c)
            else:
                chunkq = textblock[len(textblock)-1] + " " + c
                if len(chunkq.split()) < chunk_size:
                    textblock[len(textblock)-1] = chunkq
                else:
                    textblock.append(c)

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