from collections import defaultdict
from bs4 import BeautifulSoup
import requests
import json



# Open config file to get key
with open('wolframalpha_api.config', 'r') as f:
    wolfram_key = f.readline().rstrip()
            
# Ask for topic to query
print 'Enter a topic to query on Wolfram Alpha:'
TOPIC = raw_input()

# Build URL using topic/key
url = 'http://api.wolframalpha.com/v2/query?input=' + TOPIC + "&format=image" +'&appid=' + wolfram_key 

# Scrape URL using requests and beautiful soup
r  = requests.get(url)
data = r.text
soup = BeautifulSoup(data)

print '\nURL: ',url,'\n'


pod_data = defaultdict(list)
for i,pod in enumerate(soup.findAll('pod')):
    pod_data[pod["id"]] = [ pod.findAll("img")[0].get("src")]
    for info in pod.findAll("info"):
         if info.get("text") != None and info.findAll("img"):
            pod_data[pod["id"]].append(info.get("text")) 
            pod_data[pod["id"]].append(info.findAll("img")[0].get("src"))


data_out = open(TOPIC, "w")
data_out.write(json.dumps(pod_data))
data_out.close()

data_in = open(TOPIC, "r")
for line in data_in.readlines():
    print json.loads(line).keys()
    print "\n"
    print json.loads(line).values()
