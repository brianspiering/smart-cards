""" Call wolframalpha API
Works for:
- pi

Doesn't work for:
- Ln; returns plots
- e
"""

from collections import defaultdict
from bs4 import BeautifulSoup
import requests
import json

def clean_wolfram_data(raw_data):
    try:
        clean_data = round(float(raw_data[:10]), 4)

        return clean_data
    except ValueError:
        print('\n\n{} is not handled by the code'.format(raw_data))
    
# Open config file to get key
with open('wolframalpha_api.config', 'r') as f:
    wolfram_key = f.readline().rstrip()
            
# Ask for topic to query
print 'Enter a topic to query on Wolfram Alpha:'
topic = raw_input()

# Build URL using topic/key
url = 'http://api.wolframalpha.com/v2/query?input=' + topic + "&format=image" +'&appid=' + wolfram_key 

# Scrape URL using requests and beautiful soup
r  = requests.get(url)
data = r.text
soup = BeautifulSoup(data)

# Get just the simple flashcard info
for i, pod in enumerate(soup.findAll('pod')):
    if i == 1:
        card_front = "What is the "+ pod.attrs['title'].lower() + ' of ' + topic + '?'
        raw_data = pod.findAll("img")[0].get("alt")
        card_back = clean_wolfram_data(raw_data)
        break

# Example of flashcard 
# data = {"fcid": 1,
#         "order": 0,
#         "term": "pi",
#         "definition": "3.1416",
#         "hint": "",
#         "example": "",
#         "term_image": None,
#         "hint_image": None}

flashcard = {"fcid": 1,
        "order": 0,
        "term": card_front,
        "definition": card_back,
        "hint": "",
        "example": "",
        "term_image": None,
        "hint_image": None}

# Save the data
file_endpoint = "data/"+topic+".txt"

with open(file_endpoint, "w") as data_out:
    json.dump(flashcard, data_out)


# TODO: Write images also
# see wolframalpha_api.ipynb
