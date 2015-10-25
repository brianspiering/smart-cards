""" Various CourseHero API integrations

Doc: https://www.coursehero.com/api/intro.php
"""

from __future__ import (absolute_import, 
                        division,
                        print_function,
                        unicode_literals)
from pprint import pprint
import requests
import urllib
from urlparse import urljoin, urlunsplit

# Load api keys
with open('.config') as f:
    api_key = f.readline()
    exec(api_key)
    api_key = {'api_key': api_key}
    
    #secret_key = f.readline()
    #exec(secret_key)

def validate_api_call(r):
    "Check if api call gets a valid code, if not print the error message."
    if r.status_code == 200:
        print('API call success =)')
        data = r.json()['data']
    elif r.status_code == 400:
         pprint(eval(r.content.replace('false', 'False')))
    else:
        print('Check this status:' + r.status_code)

def get_related_card_sets(protocol, base, topic):
    
    endpoint = 'categories/'
    parameter  = 'starts_with'
    value = topic

    queries = {}
    queries.update(api_key)
    queries.update({parameter: value})
          
    url_query = urllib.urlencode(queries)

    url = urlunsplit((protocol, base, endpoint, url_query, ''))
    print(url)

    #  Query API
    r = requests.get(url)
    validate_api_call(r)
    data = r.json()['data']

    # Get best category id 
    for datum in data:
        if datum['category'].lower() == value: # TODO: Make fuzzy match using fuzzywuzzy package
            category_id = datum['id']

    # Get flashcard sets that share category id
    endpoint = 'categories/' + "/".join([str(category_id), 'sets']) + '/' # /api/flashcards/categories/1914/sets
    queries = {}
    queries.update(api_key)
    url_query = urllib.urlencode(queries)
    url = urlunsplit((protocol, base, endpoint, url_query, ''))
    print(url)

    r = requests.get(url)
    validate_api_call(r)
    data = r.json()['data']

    # url and total flashcards of user with largest set
    max_url   = "empty"
    max_cards = 0
    max_user = None
    for i in xrange(len(data)):
        if i == 0:
            max_url      = data[i]["url"]
            max_cards    = int(data[i]["total_flashcards"])
            max_user     = data[i] 
        else:
            if int(data[i]["total_flashcards"]) > max_cards:
                max_cards = int(data[i]["total_flashcards"])
                max_url   = data[i]["url"]
                max_user  = data[i]
    print("\n\nThe best cards for topc "+topic+": ")
    print(max_url)
    print(max_user)
    pprint(max_cards, width=1, indent=4)

# Fundmentals of the api call
protocol = 'https'
base = 'www.coursehero.com/api/flashcards'

# Get related flash card sets
# topic = 'pi'
# get_related_card_sets(protocol, base, topic)

# 