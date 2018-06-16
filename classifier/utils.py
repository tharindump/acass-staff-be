import os
from collections import Counter
from nltk import word_tokenize
from nltk.corpus import stopwords
import _pickle

from preprocessor import clean_page
from config import *


def load_web_pages():
    profile_dir = TRAINING_DATA_DIR + 'profiles/'
    non_profile_dir = TRAINING_DATA_DIR + 'non-profiles/'
    profiles = os.listdir(profile_dir)
    non_profiles = os.listdir(non_profile_dir)

    web_pages_list = [non_profile_dir + non_profile_page for non_profile_page in non_profiles]
    web_pages_list = web_pages_list + [profile_dir + profile_page for profile_page in profiles]

    return web_pages_list


# clean and extract text from web pages and returns the extracted
# text as a list and corresponding labels list with it
def create_vector():
    web_pages_list = load_web_pages()
    stop_words_set = set(stopwords.words('english'))
    features = []
    labels = []
    idx = 0
    for web_page in web_pages_list:
        try:
            idx += 1
            print(idx)
            with open(web_page, 'r', encoding='utf8') as f:
                # clean page with pre-processor
                formatted_page = clean_page(f.read())
                f.close()

            if 'non-profiles' in web_page:
                labels.append(0)  # 0 for non profile pages
            elif 'profiles' in web_page:
                labels.append(1)

            features.append(formatted_page)
        except Exception as e:
            print(e)

    return features, labels


def count_words():
    web_pages_list = load_web_pages()
    stop_words_set = set(stopwords.words('english'))
    words_list = []

    idx = 0

    for web_page in web_pages_list:
        try:
            idx += 1
            print(idx)
            with open(web_page, 'r', encoding='utf8') as f:
                # clean page with pre-processor
                formatted_page = clean_page(f.read())
                f.close()

            # tokenize words with nltk tokenizer
            unfiltered_words = word_tokenize(formatted_page)

            # remove stop words, and non-alphabetic words from the bag of words
            for word in unfiltered_words:
                word = word.lower()
                if word.isalpha() and word not in stop_words_set:
                    words_list.append(word)
        except Exception as e:
            print(e)

    bag_of_words = Counter(words_list)
    print('Words =', len(words_list), '| BoW =', len(bag_of_words))
    print(bag_of_words.most_common())

    # saving BoW
    with open('bag_of_words.mdl', 'wb') as f:
        _pickle.dump(bag_of_words, f)
        print("Saved the BoW")

    return bag_of_words.most_common(5000)


def create_dataset(bag_of_words):
    web_pages_list = load_web_pages()
    features_set = []
    labels = []

    # iterate the training dataset
    idx = 0
    for web_page in web_pages_list:
        try:
            idx += 1
            print(idx)
            with open(web_page, 'r', encoding='utf8') as f:
                # clean the web page
                formatted_page = clean_page(f.read())
                f.close()

            # tokenize the page text
            formatted_page_lower = formatted_page.lower()
            words_list = word_tokenize(formatted_page_lower)
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


def get_bow():
    bow_path = CLASSIFIER_MODEL_DIR + BAG_OF_WORDS_
    try:
        with open(bow_path, 'rb') as f:
            bow = _pickle.load(f)
            return bow.most_common(5000)
    except:
        return False
