#main file

from scripts.API_tools import access_API, API_request
from scripts.getsummary import getmodel, summarize

if __name__ == "__main__":
    
    headers = access_API()
    df, block = API_request(headers, "NVDA")
    model, t = getmodel()
    output = summarize(model, t, block)

    print(output)