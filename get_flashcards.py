
from flask import Flask

app = Flask(__name__)

@app.route("/")

def get_flashcards(category):
    import subprocess
    p = subprocess.Popen("python mine_wordnet.py " + category, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    
if __name__ == 'main':
    app.run()