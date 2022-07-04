import requests
import pandas as pd
import json
import streamlit as st

#returns access key header
def access_API():

    CLIENT_ID = st.secrets['CLIENT_ID']
    SECRET_KEY = st.secrets['SECRET_KEY']
    #Set up authorization
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

    # Create dictionary to pass to reddit for login
    data = {
        "grant_type": "password",
        "username": st.secrets['username'],
        "password": st.secrets['password']
    }

    # Create description of API (Used MyAPI with a version number)
    headers = {'User-Agent': 'MyAPI/0.0.1'}

    # Send request for OAuth token from Reddit
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data =data, headers=headers)

    # Store access token
    TOKEN = res.json()['access_token']

    # Add token (formatted in string) to headers 
    headers['Authorization'] = f'bearer {TOKEN}'
    return headers

# requires header returned from access_API function
# search Reddit and collect posts with searchterm, return dataframe
def API_request(headers, searchterm):

    # Initialize dataframe for posts
    posts_df = pd.DataFrame()

    #print progress
    print("Collecting Data...")

    # Get request: defaults to 100 returns, can restrict datetime 
    payload = {'q': searchterm}
    res = requests.get('https://oauth.reddit.com/search', headers=headers, params=payload)
 
    #print(res.json())

    # Access each post in the response and put in dataframe
    for post in res.json()['data']['children']:
        posts_df = pd.concat([posts_df, pd.DataFrame({
            'subreddit': post['data']['subreddit'],
            'source_category': searchterm,
            'full_name': post['kind'] + '_' + post['data']['id'],
            'title': post['data']['title'],
            'content': post['data']['selftext'],
            'type': post['data']['link_flair_text'],
            'upvote_ratio': post['data']['upvote_ratio'],
            'ups': post['data']['ups'],
            'downs': post['data']['downs'],
            'score': post['data']['score'],
        }, index=[len(posts_df)+1])])

    return posts_df
