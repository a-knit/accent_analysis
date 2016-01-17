import pandas as pd
import numpy as np
from pymongo import MongoClient
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import cross_val_score, train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from uniformity import scale_to_n
from cross_validate import cross_val
from plot import plot_nth_word, plot_n_words

def prep_data(coll, word_=False, scaling=False):
    '''prepare words for model'''

    X = []
    y = []
    sp = [] # index of which speaker each data point comes from
    f_per_word = 16
    num_words = 12

    for i in xrange(1546):
        entry = collection.find_one({'index': i})

        family = entry['family']
        lang = entry['language']
        if family=='european':
            if lang != 'english':
                continue
        elif family=='sino_tibetan' or family=='afroasiatic':
            family = 'other'
        else family=='indo_iranian':
            continue

        word_data = entry['word_formants']

        x = np.array([])

        for word in word_data:

            # remove sounds that are too short, these are likely not actual words
            int_length = word['int_length']
            if int_length < .08:
                continue

            F1 = scale_to_n(word['time'], word['F1'], f_per_word)
            F2 = scale_to_n(word['time'], word['F2'], f_per_word)
            F3 = scale_to_n(word['time'], word['F3'], f_per_word)
            F4 = scale_to_n(word['time'], word['F4'], f_per_word)
            F = np.concatenate((F1, F2, F3, F4))

            if x.shape[0]==0:
                x = F
            else:
                x = np.concatenate((x, F))

            if not word_:
                if x.shape[0]==num_words*(f_per_word*4):
                    break

        # optional scaling of features to the mean and deviation of each formant of each speaker
        if scaling:
            x = scale_by_formant(x, f_per_word)

        # this is a alternate feature setup where we make a prediction of the accent for each word as opposed to each speaker
        if word_:
            words_for_this_sp = x.shape[0] / (f_per_word*4)
            for word_i in xrange(words_for_this_sp):
                start = word_i * f_per_word * 4
                end = start + f_per_word * 4
                F = x[start:end]
                X.append(F)
                y.append(family)
                sp.append(i)
        
        # this code will run in the standard model:
        else:
            if x.shape[0]==num_words*(f_per_word*4):
                X.append(x)
                y.append(family)            

    X = np.array(X)
    y = np.array(y)
    sp = np.array(sp)

    return X, y, sp

def ran_forest(X, y, sp, word_=False, samp_method=None):
    rf = RandomForestClassifier()
    return cross_val(rf, X, y, sp, word_=word_, samp_method=samp_method)

def SVM(X, y, sp, word_=False, samp_method=None):
    svm = SVC(class_weight='balanced')
    return cross_val(svm, X, y, sp, word_=word_, svm=True, samp_method=samp_method)

def KNN(X, y, sp, word_=False):
    knn = KNeighborsClassifier(n_neighbors=5)
    return cross_val(knn, X, y, sp, word_=word_, samp_method=samp_method)

def GB(X, y, sp, word_=False, samp_method=None):
    gb = GradientBoostingClassifier()
    return cross_val(gb, X, y, sp, word_=word_, samp_method=samp_method)

def scale_by_formant(x, f_per_word):
    '''scale data for each formant for a single speaker, x is a 1d array of all the formant data for a particular speaker'''

    F = [[],[],[],[]]
    result = np.zeros(x.shape)
    for i, val in enumerate(list(x)):
        f = divmod(i%(f_per_word*4), f_per_word)[0]
        F[f].append(val)
    F = np.array(F)
    means = np.mean(F, axis=1)
    stds = np.std(F, axis=1)
    for i, val in enumerate(list(x)):
        f = divmod(i%(f_per_word*4), f_per_word)[0]
        result[i] = (val - means[f]) / stds[f]
    return result 

if __name__ == '__main__':
    client = MongoClient()
    db = client['project']
    collection = db['word_data']

    sp = []
    X, y, sp = prep_data(collection, word_=False, scaling=False)
    print 'words prepped'
    # rf = ran_forest(X, y, sp, samp_method='smote')
    # print 'random forest complete'
    # svm = SVM(X, y, sp, samp_method='smote')
    # print 'svm complete'
    # gb = GB(X, y , sp, samp_method='smote')
    # print 'gradient boost complete'
    # print 'rf by word scores:', rf
    # print 'svm by word scores:', svm
    # print 'gb by word scores:', gb

    # rf = ran_forest(X, y, sp, word=False, samp_method='smote')
    # print 'random forest complete'
    # svm = SVM(X, y, sp, word=False, samp_method=None)
    # print 'svm complete'
    # gb = GB(X, y , sp, word=False, samp_method=None)
    # print 'rf by speaker scores:', rf
    # print 'svm by speaker scores:', svm
    # print 'gb by speaker scores:', gb

    # for i in xrange(2):
    #     plot_nth_word(X, y, (i+1), 16)

    for i in xrange(6):
        plot_n_words(X, y, (i+1), 16)
