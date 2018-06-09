import requests
import score_calc
from threading import Thread


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
    page = requests.get('https://www.mrt.ac.lk/web/taxonomy/term/275/feed')
    preprocessor.calculate_relevance_score(page.text, "Human Computer Interaction")