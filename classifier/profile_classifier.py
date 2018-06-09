import os
from collections import Counter
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from preprocessor import clean_page
from nltk import word_tokenize
from nltk.corpus import stopwords
import _pickle


def load_web_pages():
    profile_dir = './training_data/profiles/'
    non_profile_dir = './training_data/non-profiles/'
    profiles = os.listdir(profile_dir)
    non_profiles = os.listdir(non_profile_dir)

    web_pages_list = [non_profile_dir + non_profile_page for non_profile_page in non_profiles]
    web_pages_list = web_pages_list + [profile_dir + profile_page for profile_page in profiles]

    return web_pages_list


def count_words():
    web_pages_list = load_web_pages()
    stop_words_set = set(stopwords.words('english'))
    words_list = []

    for web_page in web_pages_list:
        try:
            with open(web_page, 'r', encoding='utf8') as f:
                # clean page with pre-processor
                formatted_page = clean_page(f.read())
                f.close()

            # tokenize words with nltk tokenizer
            unfiltered_words = word_tokenize(formatted_page)

            # remove stop words, and non-alphabetic words from the bag of words
            for word in unfiltered_words:
                word = word.lower()
                if word.isalpha() and not word in stop_words_set:
                    words_list.append(word)
        except Exception as e:
            print(e)

    bag_of_words = Counter(words_list)
    print('Words =', len(words_list), '| BoW =', len(bag_of_words))
    print(bag_of_words.most_common())

    return bag_of_words.most_common(5000)


def create_dataset(bag_of_words):
    web_pages_list = load_web_pages()
    features_set = []
    labels = []

    # iterate the training dataset
    for web_page in web_pages_list:
        try:
            with open(web_page, 'r', encoding='utf8') as f:
                # clean the web page
                formatted_page = clean_page(f.read())
                f.close()

            # tokenize the page text
            words_list = word_tokenize(formatted_page)
            word_occurrence = []

            # calculate word occurrence in the page with bag of words
            for word_entry in bag_of_words:
                word_occurrence.append(words_list.count(word_entry[0]))

            # append the calculated word occurrence to features list
            features_set.append(word_occurrence)
            if 'non-profiles' in web_page:
                labels.append(0)  # 0 for non profile pages
            elif 'profiles' in web_page:
                labels.append(1)  # 1 for profile pages

        except Exception as e:
            print(e)

    return features_set, labels


if __name__ == '__main__':
    bow = count_words()
    feature_set, labels = create_dataset(bow)

    # splitting data
    x_train, x_test, y_train, y_test = train_test_split(feature_set, labels, test_size=0.2)
    classifier = MultinomialNB()
    # training classifier
    classifier.fit(x_train, y_train)

    # calculate predictions
    predictions = classifier.predict(x_test)
    # test accuracy
    print("Accuracy = ", accuracy_score(y_test, predictions))

    # saving classifier
    with open('profile-classifier.mdl', 'wb') as f:
        _pickle.dump(classifier, f)
        print("Saved the classifier")
