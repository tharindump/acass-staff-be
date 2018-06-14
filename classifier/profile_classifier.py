import os
from collections import Counter
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from preprocessor import clean_page
from nltk import word_tokenize
from nltk.corpus import stopwords
import _pickle
from classifier.train_profile_classifier import count_words, get_bow
import numpy as np


class MNBClassifier(object):

    def __init__(self, model):
        print("Initializing classifier.")
        self.name = "Multinomial Naive Bayes based Profile classifier"

        # loading classifier model
        with open(model, 'rb') as f:
            self.classifier = _pickle.load(f)

        # with open('D:/Workspace/Project_L4/acass-staff-be/bag_of_words.mdl', 'rb') as f:
        #     self.bag_of_words = _pickle.load(f)

        self.bag_of_words = get_bow()

        # self.bag_of_words = count_words()
        print('Classifier is ready.')

    def predict_web_page(self, page):
        formatted_page = clean_page(page)
        words_list = word_tokenize(formatted_page)

        features = []
        for word in self.bag_of_words:
            features.append(words_list.count(word[0]))

        predicted_result = self.classifier.predict([features])
        prob = self.classifier.predict_proba([features])

        # print(prob)
        result = np.asscalar(np.int32(predicted_result[0]))
        return result

    def score(self, page):
        return 22.33
