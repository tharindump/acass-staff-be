import _pickle
import requests
from classifier.profile_classifier import NaiveBayesClassifier
import config

if __name__ == '__main__':

    clf_path = config.CLASSIFIER_MODEL_DIR+config.CLASSIFIER_MODEL_NAME
    nbclf = NaiveBayesClassifier(clf_path)

    while True:
        inp = input('>> ')
        if inp == "exit":
            break

        print('Sending request to %s....'%inp)
        test_page = requests.get(inp)

        pred = nbclf.predict_web_page(test_page.content)
        print("Result: ", ['non-profile', 'profile'][pred])



