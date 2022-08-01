import re

# params: df of post info returned from API
# returns: text block of body text: used for ExFinSummarizer
def makecloud(posts_df):
    #add titles and post bodies together
    textblock = ''
    for i in range(len(posts_df)):
        textblock = textblock + " " + posts_df['title'][i+1] + ' ' + posts_df['content'][i+1]

    #remove links, etc.
    textblock = re.sub(r'http\S+', '', textblock)
    textblock = re.sub("&amp;#x200B;", '', textblock)
    gone = '[]$\\//()'
    for g in gone:
        textblock = textblock.replace(g, '')
    textblock = textblock.replace("\n", ' ')
    
    #return block
    return textblock

# params: df of post info returned from API
# returns: list of text blocks of titles and text, used for GenFinSummarizer
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
        gone = '[]//$\\()'
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
