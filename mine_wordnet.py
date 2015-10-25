from nltk.corpus import wordnet as wn
from itertools import product,chain
from collections import defaultdict
import operator,json,csv,sys,subprocess,os.path

def get_definitions(word):
    '''
    Takes a word as input and returns all definitions in the form of a
    dictionary with the synset as keys and definition text as values.
    '''
    definitions = defaultdict()
    for i,j in enumerate(wn.synsets(word)):
        definitions[j] = j.definition()
    return definitions

def get_ontology(seed_syn,word,write_file=False):
    '''
    Takes word as input and returns two dictionaries. One with the list
    of hypernym synsets and one with a list of hyponym synsets.
    '''
    hypernyms = defaultdict()
    hyponyms = defaultdict()
    for i,j in enumerate(wn.synsets(word)):
        hypernyms[j] = ",".join(list(chain(*[l.lemma_names() for l in j.hypernyms()])))
        hyponyms[j] = ",".join(list(chain(*[l.lemma_names() for l in j.hyponyms()])))

    if not hyponyms.values():
        return [],[]
    
    hypo_words = [hyponyms.values()[i].split(',') for i in range(len(hyponyms.values())) if hyponyms.values()[i]][0]
    hypo_syns = [get_definitions(hypo_words[i].replace(' ','_')).keys()[0] for i in xrange(len(hypo_words))]
    relevant_hypo_synsets = calc_seed_similarity(seed_syn,hypo_syns)
    
    # Write to file as feeder system to wolfram alpha api code
    if write_file:
        file_endpoint = "data/"+word+"_hyponyms.csv"
        hypo_out = [str(relevant_hypo_synsets[i][0].lemma_names()[0]).replace('_',' ')
                    for i in range(len(relevant_hypo_synsets))]        
                
        with open(file_endpoint, "w") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerow(hypo_out) 
    
    return hypernyms, relevant_hypo_synsets

def calc_seed_similarity(seed_syn,topic_syns,threshold=.2):
    '''
    Using Wu-Palmer Similiarity compare a seed synset to a list of
    topic synsets. If the similarity score is above the threshold
    it is considered relevant and returned.
    '''
    similarity_scores = defaultdict()
    for i in range(len(topic_syns)):
        score = seed_syn.wup_similarity(topic_syns[i]) # Wu-Palmer Similarity
        if score > threshold:
            similarity_scores[topic_syns[i]] = score
    return sorted(similarity_scores.items(), key=operator.itemgetter(1), reverse=True) 

def create_flashcard(i,card_front,card_back):
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
    file_endpoint = "data/"+card_front+"_text"+str(i)+".json"
    with open(file_endpoint, "w") as data_out:
        json.dump(flashcard, data_out)

#### TODO: Not yet converted to real function
# def get_synonyms(word):
#     print "THESAURUS"
#     print 50 * '*'
#     for i,j in enumerate(wn.synsets(topic)):
#         print "Meaning",i, "NLTK ID:", j.name()
#         print "Definition:",j.definition()
#         print "Synonyms:",  ", ".join(j.lemma_names())
#         print

def main(argv):
    # Start by providing seed word to filter out unrelated topics/words
    SEED = 'math'
    seed_syn = get_definitions(SEED).keys()[0]
    # print 'SEED: ',SEED
    # print seed_syn

    topic = argv
    topic_syns = get_definitions(topic)
    print 'TOPIC: ',topic
    # print 'SYNSETS: ',topic_syns

    relevant_synsets = calc_seed_similarity(seed_syn,topic_syns.keys())
    # print 'REL SYNSETS: ',relevant_synsets
    for i in range(len(relevant_synsets)):
        create_flashcard(i,topic,topic_syns[relevant_synsets[i][0]])

    _,_ = get_ontology(seed_syn,topic,write_file=True) # hypernyms, hyponyms

if __name__ == "__main__":
    _,topic = sys.argv
    main(topic)
    
    print topic
    p = subprocess.Popen("python get_data_from_wolfram.py " + topic, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    #print output