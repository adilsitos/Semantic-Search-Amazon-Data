from copy import Error
from fastai.text.all import *
import pandas as pd
import requests
import json

def load_model():
    learn = load_learner('./10_with_encoder.pth')   
    return learn


def tokenize_text(df):
    tokenized_text = []
    dls = torch.load('./dataloader.pkl')

    for description in df['description']:
        tok_description = dls.tokenizer(description)
        num_description = dls.numericalize(tok_description)
        tokenized_text.append(num_description)

    return tokenized_text


def semantic_search(text, id):
    try:
        input = json.dumps({"search_string":text,"ID":id})
        endpoint = 'http://50a9efd4-bbc1-4e53-b376-f44aac367846.southcentralus.azurecontainer.io/score'
        headers = { 'Content-Type':'application/json'}

        resp = requests.post(endpoint, input, headers=headers)

        return resp.text
    except Error:
        print("Error:", Error)


def format_response(results):
    if(type(results) is str):
        data = json.loads(results)
        df = pd.read_json(data['response'])
        return df

    else:
        return f'Error: Results is not a str type'





