"Given a flat file of terms get make the flashcards"

import csv
import os

import get_data_from_wolfram


word = 'triangle' # topic is hardcoded

file_endpoint = "data/"+word+"_hyponyms.csv"

# Load file
with open(file_endpoint, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ')
    for hypos in spamreader:
            pass

# Call the other file
command_line_args = ' '.join(hypos).replace(' ', '_').replace(',', ' ')
os.system('python get_data_from_wolfram.py {}'.format(command_line_args)) # Doesn't seem to work