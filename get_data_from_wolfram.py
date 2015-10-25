""" Call wolframalpha API

docs (pdf): http://products.wolframalpha.com/docs/WolframAlpha-API-Reference.pdf?_ga=1.107330246.599422832.1445658318

Doesn't work for:
- one: returns itself

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

def make_card_front(title, topic):
    "Reformat a title string into front of a flashcard."
    
    # Create a translation dictionary
    phrase = {'plot': {'subject': 'Please draw a plot of', 
                        'punctation': '.'},
             'plots': {'subject': 'Please draw a plot of', 
                        'punctation': '.'},
             'illustration': {'subject': 'Please draw a plot of', 
                        'punctation': '.'},
              'visual form':{'subject': 'What is the mathmatical symbol for', 
                            'punctation': '?'},
             'decimal approximation': {'subject': 'Name as many decimals as possible for', 
                            'punctation': '.'},
             'basic definition': {'subject': 'What is the definition of', 
                            'punctation': '?'},              
             'definition': {'subject': 'What is the definition of', 
                            'punctation': '?'},
             'definitions': {'subject': 'What are definitions of', 
                            'punctation': '?'},
            'equation': {'subject': 'What is the equation for', 
                            'punctation': '?'},
              'conversions to other units': {'subject': 'Name equivalent terms for', 
                            'punctation': '.'},
              'number name': {'subject': 'Name equivalent terms for', 
                            'punctation': '.'}, 
                'statement': {'subject': 'What is the', 
                            'punctation': '?'}, 
            'alternate names': {'subject': 'What are alternate names for', 
                            'punctation': '?'},  
                'limit':  {'subject': 'What is unique about a ', 
                            'punctation': '?'}       
             }
    
    title = title.lower().strip() # Munge data
    
    card_front = phrase[title]['subject']+' '+topic+phrase[title]['punctation']
    return card_front

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

# Make an image flashcard
for i, pod in enumerate(soup.findAll('pod')):
    if i == 1:
        try:
            card_front = make_card_front(pod.attrs['title'], topic)

            # raw_data = pod.findAll("img")[0].get("alt") # Sometimes 
            # card_back = clean_wolfram_data(raw_data) # The text is not good nor consistent
            image_url = pod.findAll("img")[0].get("src")
            image_filename = 'data/images/'+topic
            save_image(image_url, image_filename)
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

            break
        except NameError:
            print("Couldn't find your term. Please try another one.")
