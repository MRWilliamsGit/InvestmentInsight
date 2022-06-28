#main file

from scripts.API_tools import access_API, API_request

def callreddit():
    
    if headers == None:
        headers = access_API()

    df = API_request(headers, "scrapbooking")
    print(df)