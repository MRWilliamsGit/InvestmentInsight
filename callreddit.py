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

#### 2. Get hot & new posts in r/wallstreetbets and r/superstonk and put into dataframe (can add additional subreddits)
def API_request(headers):
   
    # Initialize lists of subreddits
    subreddit_list = ['wallstreetbets', 'superstonk']

    # Initialize category list of posts (where they appear in subreddit)
    category_list = ['hot', 'new']

    # Initialize dataframe for posts
    posts_df = pd.DataFrame()

    # Loop through lists and add everything to df
    for subreddit in subreddit_list:
        for category in category_list:
            # Get request for all subreddits and categories in list. Limited to 3 posts (can change - this doesn't seem to be working exactly as planned bc it's returning 5 for the hot category)
            res = requests.get('https://oauth.reddit.com/r/{0}/{1}'.format(subreddit,category), headers = headers, params={'limit':'3'})

            # Access each post in the response and put in dataframe
            for post in res.json()['data']['children']:
                posts_df = posts_df.append({
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
                }, ignore_index=True)

    # Remove duplicate posts (if any) based on full_name (unique ID of post)
    posts_df = posts_df[~posts_df.full_name.duplicated()]

    #print(posts_df)
    return posts_df

def callreddit():
    headers = access_API()
    df = API_request(headers)
    return df

###Appears to be extra at this time

    ############################### Different Request Examples ####################################################

    #### 1. Standard requests code for future use returned in json format (commenting out)
        # requests.get('https://oauth.reddit.com/api/v1/me', headers = headers).json())

    #### 3. Get comments associated with posts

    # Intialize comments df
    #comments_df = pd.DataFrame()

    #res = requests.get('https://oauth.reddit.com/r/wallstreetbets/comments/vjx0ta/', headers = headers)#, params={'limit':'3'})
    #print(res.json())

    ##### 4. Using the subreddit-comments-dl GitHub repository
    # I create a virual enviornment, cloned this repository, and installed the requirements .txt inside the virual environment

    # Used this code to download posts and comments from Wallstreetbets
    #  (NLP) C:\Users\Colin Bryan\Documents\Duke\AIPI 540\SocialMediaNLP\subreddit-comments-dl>python src/subreddit_downloader.py wallstreetbets --batch-size=512 --laps=1 --reddit-id wHoj946HPNygT64EIPRTug --reddit-secret 8W37ufOt9rFx_KTjtJkpnudr8Pbgrg --reddit-username AIPI540NLP

    # Used this code to build the dataset
    #(NLP) C:\Users\Colin Bryan\Documents\Duke\AIPI 540\SocialMediaNLP\subreddit-comments-dl>python src/dataset_builder.py