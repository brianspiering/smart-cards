
from nltk.corpus import wordnet as wn
from itertools import product,chain
from collections import defaultdict
import operator

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
    
    similarity_scores = defaultdict()
    maxscore = 0
    for i in range(len(topic_syns)):
        score = seed_syn.wup_similarity(topic_syns[i]) # Wu-Palmer Similarity
        if score > threshold:
            similarity_scores[topic_syns[i]] = score
    return sorted(similarity_scores.items(), key=operator.itemgetter(1), reverse=True) 

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