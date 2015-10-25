# HackingEDU
# SmartCards
### Inspiration
Khan Academy! What other ways can we take difficult to learn concepts and help people learn them without getting overwhelmed.
### What it does
SmartCards takes a topic entered by a user (e.g. teacher, student, parent) and searches relevant API's like WolframAlpha to build a comprehensive and enriching flashcard set. It then loads those flashcards into CourseHero for you to study and make sure you ace that upcoming exam!

### How we built it
A collaborative team focused on taking advantage of all the data available and curating it into smaller learnable chunks that can be digested by people of any age to continue to learn.

### Challenges we ran into
The proper scoping of a flashcard set can be very difficult without asking for a lot of input from the user up front. However, with input from the user SmartCards can intelligently learn what topics you are interested in studying.

### Accomplishments that we are proud of
Creating an generic framework to auto-create sets of flashcards based on very limited effort by the user, but with great value in learning concepts.

### What's next for SmartCards
Continuing to build out the knowledge base to more accurately scope sets and retrieve information from existing and available knowledge bases.

### Installation
1. Extract the zip
2. Make sure you have installed **flask**
3. Install the CORS plugin in case it's not going to be hosted **pip install -U flask-cors**
4. Start server by running **python get_flashcards.py**
5. Once it starts, hit **index.html** and have fun generating flash cards in the smartest way ever