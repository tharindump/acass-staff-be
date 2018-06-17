from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
import _pickle

from preprocessor import clean_page
from config import *
from classifier.utils import create_vector

if __name__ == '__main__':
    # get cleaned web page text with corresponding labels
    X_features, y_labels = create_vector()

    # split the result into test and train
    X_train, X_test, y_train, y_test = train_test_split(X_features, y_labels, test_size=0.3)

    # create TFIDF vectorizer
    vectorizer = TfidfVectorizer(min_df=1, stop_words="english", max_features=5000)

    # fitting the vectorizer with training data (training page text) and transforming using tfidf calculation
    X_train_tf = vectorizer.fit_transform(X_train)

    # creating linear svm
    svm_classifier = SVC(kernel='linear', C=2 ** 1, probability=True)
    # the X_train_df is a metrix, and converting it to a ndarray
    svm_classifier.fit(X_train_tf.toarray(), y_train)

    # transforming test feature set using tfidf
    X_test_tf = vectorizer.transform(X_test)
    predictions = svm_classifier.predict(X_test_tf.toarray())

    print(accuracy_score(y_test, predictions), "\n")

    # creating Multinomial Naive Bayes classifier
    mnb_classifier = MultinomialNB()
    mnb_classifier.fit(X_train_tf.toarray(), y_train)

    mnb_predictions = mnb_classifier.predict(X_test_tf.toarray())
    print(accuracy_score(y_test, mnb_predictions))

    # saving classifiers
    with open(CLASSIFIER_MODEL_DIR + MNB_CLASSIFIER, 'wb') as f:
        _pickle.dump(mnb_classifier, f)
        print("Saved the classifier")

    with open(CLASSIFIER_MODEL_DIR + SVM_CLASSIFIER, 'wb') as f:
        _pickle.dump(svm_classifier, f)
        print("Saved the classifier")

    with open(CLASSIFIER_MODEL_DIR + TFIDF_VECTORIZER, 'wb') as f:
        _pickle.dump(vectorizer, f)
        print("Saved the classifier")

    X, y = create_vector()
