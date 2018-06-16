import os
from collections import Counter
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

from preprocessor import clean_page
import _pickle
import config


class EnsembleClassifier():

    def __init__(self):
        print("Initializing classifier.")
        self.name = "Ensemble Profile Classifier"

        # loading classifier model
        path = config.CLASSIFIER_MODEL_DIR

        with open(path + config.MNB_CLASSIFIER, 'rb') as f:
            self.mnb_classifier = _pickle.load(f)

        with open(path + config.SVM_CLASSIFIER, 'rb') as f:
            self.svm_classifier = _pickle.load(f)

        # loading TFIDF Vectorizer
        with open(path + config.TFIDF_VECTORIZER, 'rb') as f:
            self.vectorizer = _pickle.load(f)

        print('Classifier is ready.')

    def predict_web_page(self, page):
        formatted_page = clean_page(page)
        feature_tf = self.vectorizer.transform([formatted_page])

        svm_probability = self.svm_classifier.predict_proba(feature_tf.toarray())
        mnb_probability = self.mnb_classifier.predict_proba(feature_tf.toarray())

        print(svm_probability, mnb_probability)

        predicted_result = self.mnb_classifier.predict(feature_tf.toarray())
        result = np.asscalar(np.int32(predicted_result[0]))
        return result
