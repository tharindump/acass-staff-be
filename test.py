import requests
import score_calc
from threading import Thread
import preprocessor


def hello(line):
    print(line+" world")


def run_pages():
    page = requests.get('http://ucsc.cmb.ac.lk/profile/kph/')
    score_calc.calculate_relevance_score(page.text, "Human Computer Interaction")

    page1 = requests.get('http://ucsc.cmb.ac.lk/')
    score_calc.calculate_relevance_score(page1.text, "Human Computer Interaction")

    page2 = requests.get('http://ucsc.cmb.ac.lk/about/')
    score_calc.calculate_relevance_score(page2.text, "Human Computer Interaction")

    page3 = requests.get('http://ucsc.cmb.ac.lk/profile/spw/')
    score_calc.calculate_relevance_score(page3.text, "Human Computer Interaction")

import _pickle
from classifier.train_profile_classifier import count_words
if __name__ == "__main__":
    bag_of_words = count_words()
    with open('bag_of_words.mdl', 'wb') as f:
        _pickle.dump(bag_of_words, f)
