import pandas as pd
import numpy as np
import os
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import cross_val_score, train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
import matplotlib.pyplot as plt

def scale_to_n(speaker, n=6):
    '''scale the formant data for an individual speaker into n partitions'''

    # set F to number of formants in analysis
    F = 4

    start = speaker['Time_s'].min()
    end = speaker['Time_s'].max()

    # result will be the row in our feature matrix, X, for this speaker
    result = []

    timescale = np.linspace(start, end, n)

    for lvl in xrange(F):
        formant = 'F%d_Hz' % (lvl + 1)
        for time in timescale:
            if time == start:
                result.append(speaker[formant].iloc[0])
            elif time == end:
                result.append(speaker[formant].iloc[-1])
            else:
                before_f = speaker[speaker.Time_s < time][formant].iloc[-1]
                after_f = speaker[speaker.Time_s > time][formant].iloc[-1]
                before_t = speaker[speaker.Time_s < time]['Time_s'].iloc[-1]
                after_t = speaker[speaker.Time_s > time]['Time_s'].iloc[-1]
                new_f = (time - before_t) / (after_t - before_t) * (after_f - before_f) + before_f
                result.append(new_f)

    return np.array(result)

def plot(filename):
    data = pd.read_csv('data/%s' % filename)
    plt.plot(data['Time_s'], data['F1_Hz'], color='r')
    plt.plot(data['Time_s'], data['F2_Hz'], color='b')
    plt.plot(data['Time_s'], data['F3_Hz'], color='g')
    plt.plot(data['Time_s'], data['F4_Hz'], color='y')
    plt.title(filename)
    plt.show()

def norm_to_F1(X, n=6):
    result = np.zeros(X.shape)
    i = 0
    for row in X:
        avg_f1 = row[:n].mean()
        result[i] = row - avg_f1
        i += 1
    return result

def create_Xy(n=6):
    features = []
    labels = []
    for filename in os.listdir('data/u/'):
        if not os.path.isfile(filename):    
            data = pd.read_csv('data/u/' + filename)
            features.append(scale_to_n(data, n))
            labels.append(filename[0])
    X = np.array(features)
    return norm_to_F1(X, n), np.array(labels)

def normalize(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2)
    scaler = StandardScaler()
    scaler.fit(X_train)
    return scaler.transform(X_train), scaler.transform(X_test), y_train, y_test

def svm_score(X, y):
    scores = []
    for i in xrange(5):
        X_train, X_test, y_train, y_test = normalize(X, y)
        svm = SVC()
        svm.fit(X_train, y_train)
        scores.append(svm.score(X_test, y_test))
    return scores

# def svm_score(X, y):
#     svm = SVC()
#     scaler = StandardScaler()
#     X = scaler.fit_transform(X)
#     return cross_val_score(svm, X, y, scoring='accuracy', cv=5)

def logist_score(X, y):
    logist = LogisticRegression()
    return cross_val_score(logist, X, y, scoring='accuracy', cv=5)

def rf_score(X, y):
    rf = RandomForestClassifier()
    return cross_val_score(rf, X, y, scoring='accuracy', cv=5)

def grad_boost_score(X, y):
    boo = GradientBoostingClassifier()
    return cross_val_score(boo, X, y, scoring='accuracy', cv=5)

def gauss(X, y):
    gauss = GaussianNB()
    return cross_val_score(gauss, X, y, scoring='accuracy', cv=5)

def diff_mat(X, n=6):
    result = np.zeros(X.shape)
    i = 0
    for row in X:
        new_row = []
        for val in row[:n]:
            new_row.append(val)
        for val in xrange(X.shape[1] - n):
            new_row.append(row[val+n] - row[val])
        result[i] = np.array(new_row)
        i += 1
    return result

def avg_mat(X, n=6):
    num_f = X.shape[1]/n
    result = np.zeros((X.shape[0], num_f))
    i = 0
    for row in X:
        row_avgs = []
        for f in xrange(num_f):
            avg = row[f*n : f*n + n].mean()
            row_avgs.append(avg)
        result[i] = np.array(row_avgs)
        i += 1
    return result

if __name__ == '__main__':
    n = 5   
    X, y = create_Xy(n)
    X_diff = diff_mat(X, n)
    print 'svm accuracy:', np.mean(svm_score(X_diff, y))
    print 'logist accuracy:', np.mean(logist_score(X_diff, y))
    print 'rf accuracy:', np.mean(rf_score(X_diff, y))
    print 'grad boost accuracy:', np.mean(grad_boost_score(X_diff, y))
    print 'gaussian NB accuracy:', np.mean(gauss(X_diff, y))
    

