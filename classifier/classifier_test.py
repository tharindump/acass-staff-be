import os
from collections import Counter
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from preprocessor import clean_page
from nltk import word_tokenize
from nltk.corpus import stopwords
import _pickle
from classifier.profile_classifier import count_words
import requests

if __name__ == '__main__':
    #loading classifie model
    with open('profile-classifier.mdl', 'rb') as f:
        classifier = _pickle.load(f)

    bow = count_words()

    while True:
        inp = input('>> ')
        if inp == "exit":
            break

        print('Sending request to %s....'%inp)
        test_page = requests.get(inp)
        print('Page received...')
        formatted_page = clean_page(test_page.content)
        words_list = word_tokenize(formatted_page)

        features = []
        for word in bow:
            features.append(words_list.count(word[0]))

        print('Predicting result...')
        predicted_result = classifier.predict([features])
        print(predicted_result)


