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

if __name__ == "__main__":
    from sklearn.datasets import fetch_20newsgroups
    from sklearn.feature_extraction.text import CountVectorizer

    categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']
    twenty_train = fetch_20newsgroups(subset='train',
                                      categories=categories, shuffle=True, random_state=42)

    count_vect = CountVectorizer()
    X_train = count_vect.fit_transform(twenty_train)
    print(len(twenty_train))
    print(X_train)