from math import log
from classifier.utils import load_web_pages
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from preprocessor import clean_page
from nltk import word_tokenize
from nltk.corpus import stopwords
import requests


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


if __name__ == "__main__":
    X_features, y_labels = create_vector()
    X_train, X_test, y_train, y_test = train_test_split(X_features, y_labels, test_size=0.3)
    vectorizer = TfidfVectorizer(min_df=1, stop_words="english", max_features=5000)

    X_train_tf = vectorizer.fit_transform(X_train)

    svm_classifier = SVC(kernel='linear', C=2 ** 1, probability=True)
    svm_classifier.fit(X_train_tf.toarray(), y_train)

    X_test_tf = vectorizer.transform(X_test)
    predictions = svm_classifier.predict(X_test_tf.toarray())

    print(accuracy_score(y_test, predictions), "\n")

    mnb_classifier = MultinomialNB()
    mnb_classifier.fit(X_train_tf.toarray(), y_train)

    mnb_predictions = mnb_classifier.predict(X_test_tf.toarray())
    print(accuracy_score(y_test, mnb_predictions))

    while True:
        inp = input('>> ')
        if inp == "exit":
            break

        test_page = requests.get(inp)

        formatted_page = clean_page(test_page.content)
        feature_tf = vectorizer.transform([formatted_page])

        pred = svm_classifier.predict(feature_tf.toarray())
        mnb_pred = mnb_classifier.predict_proba(feature_tf.toarray())

        print(svm_classifier.predict_proba(feature_tf.toarray()), "|", mnb_pred)
        print("Result: ", ['non-profile', 'profile'][pred[0]])
