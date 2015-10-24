""" Call wolframalpha API

docs (pdf): http://products.wolframalpha.com/docs/WolframAlpha-API-Reference.pdf?_ga=1.107330246.599422832.1445658318

Works for:
- e: Not a great flashcard
- pi: Good stuff

Doesn't work for:
- Ln; returns plots

"""

from collections import defaultdict
import json
import requests
import shutil

from bs4 import BeautifulSoup


def clean_wolfram_data(raw_data):
    try:
        clean_data = round(float(raw_data[:10]), 4)

        return clean_data
    except ValueError:
        print('\n\n{} is not handled by the code'.format(raw_data))


def save_image(url, filename):
    "Save image to disk"
    r = requests.get(url, stream=True)

    if r.status_code == 200:
        with open(filename, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    else:
        print('Non-valid url')    
    
# Open config file to get key
with open('wolframalpha_api.config', 'r') as f:
    wolfram_key = f.readline().rstrip()
            
# Ask for topic to query
topic = raw_input('Enter a topic to query on Wolfram Alpha: ')
topic = topic.lower().strip()

# Build URL using topic/key
url = 'http://api.wolframalpha.com/v2/query?input=' + topic + "&format=image" +'&appid=' + wolfram_key 

# Scrape URL
r  = requests.get(url)
data = r.text
soup = BeautifulSoup(data)

# Get just the simple flashcard info
for i, pod in enumerate(soup.findAll('pod')):
    if i == 1:
        card_front = "What is the "+ pod.attrs['title'].lower() + ' of ' + topic + '?'
        text = pod.findAll("img")[0].get("alt") # Sometimes 
        # card_back = clean_wolfram_data(raw_data)
        image_url = pod.findAll("img")[0].get("src")
        image_filename = 'data/images/'+topic
        save_image(image_url, image_filename)
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
        "definition": None,
        "hint": "",
        "example": "",
        "term_image": image_filename,
        "hint_image": None}

# Save the data
flashcard_endpoint = "data/"+topic+".json"

with open(flashcard_endpoint, "w") as data_out:
    json.dump(flashcard, data_out)

print('Wolfram Alpha data stored for: '+topic)

# TODO: Write images also
# see wolframalpha_api.ipynb
