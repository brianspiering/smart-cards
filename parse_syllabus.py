def parse_syllabus(syllabus_text):
    '''extract keywords from user syllabus '''
    import nltk
    from nltk.corpus import stopwords
    import pandas as pd
    import numpy as np
    
    def split_lexicon_keywords(lexicon):
        lst = []
        for keyword in lexicon:
            try:
                for token in keyword.split(" "):
                    if token not in stopwords.words():
                        lst.append(token)
            except: AttributeError
        return lst

    def to_lowercase(math_list):
        # lower case all math words 
        word_list = []
        for word in math_list:
            try:
                word_list.append(word.lower())
            except: AttributeError
        return word_list
    
    
    # get math lexicons
    df_cal = pd.read_csv("data/calculus_lexicon.csv", header=None)
    df_alg = pd.read_csv("data/algebra_lexicon.csv", header=None)
    df_trig = pd.read_csv("data/trigonometry_lexicon.csv", header=None)
    df_geo = pd.read_csv("data/geometry_lexicon.csv", header=None)
    
    cal = df_cal[df_cal.columns].values[0]
    alg = df_alg[df_alg.columns].values[0]
    trig = df_trig[df_trig.columns].values[0]
    geo = df_geo[df_geo.columns].values[0]
    
    # split lexicon terms to increase diversity of math terms
    cal  = split_lexicon_keywords(cal)
    alg  = split_lexicon_keywords(alg)
    trig = split_lexicon_keywords(trig)
    geo  = split_lexicon_keywords(geo)
    
    cal  = to_lowercase(cal)
    alg  = to_lowercase(alg)
    trig = to_lowercase(trig)
    geo  = to_lowercase(geo)
    
    # tokenize syllabus 
    syllabus_tokens = nltk.tokenize.regexp_tokenize(syllabus_text, r'[\w+]+')

    # filter out stop words for syllabus.txt, create unigrams and bigrams
    unigrams = [word for word in syllabus_tokens if word.lower() not in stopwords.words()]
    bigrams_tuples = [bigram for bigram in nltk.bigrams(unigrams)]
    
    # join bigrams tuples into bigram terms
    bigrams = [ " ".join(bigram)  for bigram in bigrams_tuples ]
    
    # extract keyowrds from syllabus
    bigram_keywords = [word for word in bigrams if word in cal or word in alg or word in trig or word in geo]
    unigram_keywords = [word for word in unigrams if word in cal or word in alg or word in trig or word in geo]
    
    # return a singl list of keywords
    return np.unique(unigram_keywords + bigram_keywords).tolist()


if __name__ == "__main__":
    with open('data/syllabus_2.txt', 'r') as f:
        syllabus_text = f.read()

    terms = parse_syllabus(syllabus_text)


