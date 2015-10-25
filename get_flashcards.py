
from flask import Flask

app = Flask(__name__)

@app.route("/<category>")
def get_flashcards(category):
    import subprocess
    p = subprocess.Popen("python mine_wordnet.py " + category.split('=')[1], stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    return output
    
if __name__ == '__main__':
    app.run()