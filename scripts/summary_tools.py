import pandas as pd
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# params: none, returns: model and tokenizer
def getmodel():
    print("Downloading Model...")
    model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-cnn-12-6")
    tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
    print("Download Complete")
    return model, tokenizer

# params: model, tokenizer, and text to summarize
# returns: text summary 
def summarize(model, tokenizer, text):

    print("Generating Summary...")
    input_ids = tokenizer.encode(text, return_tensors="pt", truncation=True, max_length=1024)
    output = model.generate(
        input_ids,
        max_length=200,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id,
    )
    
    output = tokenizer.decode(output[0])

    #print(output)
    return output