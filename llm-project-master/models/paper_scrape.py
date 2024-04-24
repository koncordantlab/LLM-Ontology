
from models.converter import create_graph_and_write

from models.chatgpt import get_chatgpt_response

import requests

import json


def get_key():
    with open("config.json") as config_file:
        config = json.load(config_file)

    API_KEY = config.get("SCHOLAR_API_KEY")
    return API_KEY

def get_flavonoid_abstracts(num_abstracts=3, keywords=None):
    api_key = get_key()

    headers = {

            'x-api-key': api_key,

        }

    if keywords is None:
        keywords = 'Flavonoids in Cancer and Apoptosis'


    print(keywords)

    limit = num_abstracts

    fields = "paperId,url,title,authors,abstract"

    params = {

            'query': keywords,

            'limit': limit,

            'fields': fields

        }

    response = requests.get(f'https://api.semanticscholar.org/graph/v1/paper/search?query={keywords}&limit={limit}&fields={fields}',

                            headers=headers, params=params)

    data = response.json()

    abstracts = []
    for paper in data['data']:
        abstracts.append(paper['abstract'])
        print(paper['abstract'])
        print("\n")

    return abstracts



