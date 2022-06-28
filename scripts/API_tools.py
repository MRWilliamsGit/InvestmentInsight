#Maria Williams
#6/28/22

import requests
import pandas as pd

def access_API():
    # Public Key
    CLIENT_ID = 'wHoj946HPNygT64EIPRTug'
    # Secret Key 
    SECRET_KEY = '8W37ufOt9rFx_KTjtJkpnudr8Pbgrg'
    #Set up authorization
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

    # Create dictionary to pass to reddit for login
    data = {
        'grant_type': 'password',
        'username': 'AIPI540NLP',
        'password': 'n$iQf782W*06'
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

    # Get request: defaults to 100 returns, can restrict datetime 
    res = requests.get('https://oauth.reddit.com/r/search?q='+searchterm, headers = headers)
    #res = requests.get('https://oauth.reddit.com/r/{0}/{1}'.format(subreddit,category), headers = headers, params={'limit':'3'})

    # Access each post in the response and put in dataframe
    for post in res.json()['data']['children']:
        posts_df = pd.concat([posts_df, pd.DataFrame({
            'subreddit': post['data']['subreddit'],
            'source_category': category,
            'full_name': post['kind'] + '_' + post['data']['id'],
            'title': post['data']['title'],
            'content': post['data']['selftext'],
            'type': post['data']['link_flair_text'],
            'upvote_ratio': post['data']['upvote_ratio'],
            'ups': post['data']['ups'],
            'downs': post['data']['downs'],
            'score': post['data']['score'],
        }, index=[len(posts_df)+1])])

    # Remove duplicate posts (if any) based on full_name (unique ID of post)
    posts_df = posts_df[~posts_df.full_name.duplicated()]

    #print(posts_df)
    return posts_df
