from copy import Error
import pandas as pd
import requests
import json


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


def analytics_service(df, user_input, feedback):
    try:
        input = json.dumps({
            "users_response": feedback,
            "searched_query": user_input,
            "first": df.iloc[0]['title'],
            "first_score": df.iloc[0]['scores'],
            "second": df.iloc[1]['title'],
            "second_score": df.iloc[0]['scores'],
            "third": df.iloc[2]['title'],
            "third_score": df.iloc[0]['scores']
        })
        headers = { 'Content-Type':'application/json'}
        url = 'https://semanticsearchamazon.herokuapp.com'
        endpoint =  url + '/api/recommendations/'
        requests.post(endpoint, input, headers=headers)
        return 
    except Error:
        return






