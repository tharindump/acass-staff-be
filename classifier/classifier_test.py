import _pickle
import requests
from classifier.profile_classifier import EnsembleClassifier
import config

if __name__ == '__main__':

    clf = EnsembleClassifier()

    while True:
        inp = input('>> ')
        if inp == "exit":
            break

        print('Sending request to %s....' % inp)
        test_page = requests.get(inp)

        pred = clf.predict_web_page(test_page.content)
        print("Result: ", ['non-profile', 'profile'][pred])
