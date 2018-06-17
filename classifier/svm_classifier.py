from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
import _pickle

from preprocessor import clean_page
import config
from classifier.utils import create_vector


def weighted_mean_prediction(svm_pred, mnb_pred, svm_acc, mnb_acc):
    mean_prob = (svm_pred * svm_acc + mnb_pred * mnb_acc) / (svm_acc + mnb_acc)
    if mean_prob > 0.60:
        return 1
    else:
        return 0

def evaluate_model(target_true, target_predicted):
    print(classification_report(target_true, target_predicted))
    print("The accuracy score is {:.2%}".format(accuracy_score(target_true, target_predicted)))


if __name__ == "__main__":
    path = config.CLASSIFIER_MODEL_DIR
    with open(path + config.MNB_CLASSIFIER, 'rb') as f:
        mnb_classifier = _pickle.load(f)

    with open(path + config.SVM_CLASSIFIER, 'rb') as f:
        svm_classifier = _pickle.load(f)

    # loading TFIDF Vectorizer
    with open(path + config.TFIDF_VECTORIZER, 'rb') as f:
        vectorizer = _pickle.load(f)

    X, y = create_vector()

    X_test_tf = vectorizer.transform(X)
    psvm = svm_classifier.predict(X_test_tf.toarray())
    pmnb = mnb_classifier.predict(X_test_tf.toarray())
    print("SVM:", accuracy_score(y, psvm))
    print("MNB:", accuracy_score(y, pmnb))

    ensemble_predictions = []
    arr = X_test_tf.toarray()
    for i in range(0, arr.shape[0]):
        feature = arr[i, :]
        s = svm_classifier.predict_proba([feature])[0,1]
        m = mnb_classifier.predict_proba([feature])[0,1]
        r = weighted_mean_prediction(svm_pred=s, mnb_pred=m, svm_acc=0.81, mnb_acc=0.65)
        ensemble_predictions.append(r)

    evaluate_model(y, ensemble_predictions)
    print(accuracy_score(y, ensemble_predictions))
