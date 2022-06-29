from scripts.API_tools import access_API, API_request
from scripts.summary_tools import getmodel, summarize
from scripts.data_tools import makecloud, prep_data

def main():
    searchterm = "Puppies"
    
    headers = access_API()
    df = API_request(headers, searchterm)
    block = makecloud(df)
    #prep_data(block)

    model, t = getmodel()
    output = summarize(model, t, block)
    print(output)


if __name__ == "__main__":
    main()