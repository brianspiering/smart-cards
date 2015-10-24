from nltk.corpus import wordnet as wn
from itertools import product,chain
from collections import defaultdict
import operator,json

def get_definitions(word):
    '''
    Takes a word as input and returns all definitions in the form of a
    dictionary with the synset as keys and definition text as values.
    '''
    definitions = defaultdict()
    for i,j in enumerate(wn.synsets(word)):
        definitions[j] = j.definition()      
    return definitions

def calc_seed_similarity(seed_syn,topic_syns,threshold=.2):
    '''
    Using Wu-Palmer Similiarity compare a seed synset to a list of
    topic synsets. If the similarity score is above the threshold
    it is considered relevant and returned.
    '''
    similarity_scores = defaultdict()
    maxscore = 0
    for i in range(len(topic_syns)):
        score = seed_syn.wup_similarity(topic_syns[i]) # Wu-Palmer Similarity
        if score > threshold:
            similarity_scores[topic_syns[i]] = score
    return sorted(similarity_scores.items(), key=operator.itemgetter(1), reverse=True) 

def create_flashcard(card_front,card_back,mode='w'):
    '''
    Create a flashcard with the front and back of the card as input
    arguments. By default a new data file will be written, but the mode
    can be set to 'a' or 'a+' to append to an existing file.
    '''
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

    if mode.startswith('a'):
        with open(file_endpoint, 'a+') as data_out:
            json.dump(',', data_out)
            json.dump(flashcard, data_out)
    else:
        with open(file_endpoint, 'w') as data_out:
            json.dump(flashcard, data_out)

#### TODO: Not yet converted to real functions
def get_synonyms(word):
    print "THESAURUS"
    print 50 * '*'
    for i,j in enumerate(wn.synsets(topic)):
        print "Meaning",i, "NLTK ID:", j.name()
        print "Definition:",j.definition()
        print "Synonyms:",  ", ".join(j.lemma_names())
        print

def get_ontology(word):
    print "ONTOLOGY"
    print 50 * '*'
    for i,j in enumerate(wn.synsets(topic)):
        print "Meaning",i, "NLTK ID:", j.name()
        print "Hypernyms:", ", ".join(list(chain(*[l.lemma_names() for l in j.hypernyms()])))
        print "Hyponyms:", ", ".join(list(chain(*[l.lemma_names() for l in j.hyponyms()])))
        print   


# Start by providing seed word to filter out unrelated topics/words
SEED = 'math'
seed_syn = get_definitions(SEED).keys()[0]
# print 'SEED: ',SEED
# print seed_syn

topic = 'pi'
topic_syns = get_definitions(topic)
# print 'TOPIC: ',topic
# print 'SYNSETS: ',topic_syns

relevant_synsets = calc_seed_similarity(seed_syn,topic_syns.keys())
for i in range(len(relevant_synsets)):
    create_flashcard(topic,topic_syns[relevant_synsets[i][0]],mode='a+')  