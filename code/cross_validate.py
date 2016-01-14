import numpy as np
import pandas as pd
from sklearn.cross_validation import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
import scipy.stats as sts
from undersample import undersample, smote

def cross_val_speaker(model, X, y, cv=5, svm=False, samp_method=None):
    obs = X.shape[0]
    if y.shape[0] != obs:
        return 'Error: X and y must have the same number of observations'

    masks = create_folds(obs, cv)
    scores = []
    for mask in masks:
        X_train, X_test, y_train, y_test = train_test(X, y, mask, svm=svm)

        if samp_method=='smote':
            X_train, y_train = smote(X_train, y_train, .3, 'mandarin')
            # X_train, y_train = smote(X_train, y_train, .33, 'afroasiatic')
            # X_train, y_train = smote(X_train, y_train, .25, 'indo_iranian')
            # X_train, y_train = smote(X_train, y_train, .25, 'sino_tibetan')
        # if samp_method=='und' or samp_method=='smote':
        #     X_train, y_train = undersample(X_train, y_train, .75)
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        round_scores = calc_metrics(y_pred, y_test)
        scores.append(round_scores)
        print 'fold completed'

    return np.mean(scores, axis=0)
    # scores format: [accuracy, afro pr/re, euro pr/re, indo pr/re, sino pr/re]


def cross_val_word(model, X, y, sp, cv=5, svm=False, samp_method=None):
    obs = X.shape[0]
    if y.shape[0] != obs:
        return 'Error: X and y must have the same number of observations'

    speakers = set(sp.flatten())
    speakers = np.array(list(speakers))
    masks = create_folds(speakers.shape[0], cv)
    print 'folds created'
    scores = []
    for mask in masks:
        sp_train = speakers[mask]
        sp_test = speakers[~mask]
        data_mask = np.in1d(sp, list(set(sp_train.flatten())))

        X_train, X_test, y_train, y_test = train_test(X, y, data_mask, svm=svm)

        if samp_method=='smote':
            X_train, y_train = smote(X_train, y_train, .5, 'other')
            # X_train, y_train = smote(X_train, y_train, .4, 'afroasiatic')
            # X_train, y_train = smote(X_train, y_train, .29, 'indo_iranian')
            # X_train, y_train = smote(X_train, y_train, .223, 'sino_tibetan')
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        all_sp_test = sp[~data_mask]
        sp_pred, sp_actual = make_pred_by_speaker(all_sp_test, sp_test, y_pred, y_test)

        round_scores = calc_metrics(sp_pred, sp_actual)
        scores.append(round_scores)
        print 'fold completed'

    return np.mean(scores, axis=0)
    # scores format: [accuracy, afro pr/re, euro pr/re, indo pr/re, sino pr/re]


def create_folds(obs, cv):
    num_test = obs/cv
    remaining = set(np.arange(obs))
    folds_remaining = cv
    masks = []
    for i in xrange(cv-1):
        choices = np.random.choice(np.array(list(remaining)), num_test, replace=False)
        mask = np.ones(obs, dtype=bool)
        mask[choices] = False
        masks.append(mask)
        remaining = remaining.difference(choices)
        folds_remaining -= 1
        num_test = len(remaining)/folds_remaining
    mask = np.ones(obs, dtype=bool)
    mask[np.array(list(remaining))] = False
    masks.append(mask)
    return masks


def calc_metrics(pred, test):
    round_scores = []
    accuracy = np.sum(test==pred)/float(test.shape[0])
    round_scores.append(accuracy)
    # for family in ['afroasiatic', 'european', 'indo_iranian', 'sino_tibetan']:
    for family in ['european', 'other']:
        precision = np.sum((test==family)&(pred==family))/float(np.sum(pred==family))
        recall = np.sum((test==family)&(pred==family))/float(np.sum(test==family))
        f1 = 2 * precision * recall / (precision + recall)
        round_scores.append(f1)
    return round_scores


def train_test(X, y, mask, svm=False):
    X_train = X[mask]
    X_test = X[~mask]
    
    if svm:
        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)            

    y_train = y[mask]
    y_test = y[~mask]

    return X_train, X_test, y_train, y_test


def make_pred_by_speaker(all_sp_test, sp_test, y_pred, y_test):
    sp_pred = []
    sp_actual = []
    for speaker in list(set(sp_test.flatten())):
        test_mask = all_sp_test==speaker
        pred = max(set(y_pred[test_mask]), key=list(y_pred[test_mask]).count)
        sp_pred.append(pred)
        actual = max(set(y_test[test_mask]), key=list(y_pred[test_mask]).count)
        sp_actual.append(actual)
    sp_pred = np.array(sp_pred)
    sp_actual = np.array(sp_actual)
    return sp_pred, sp_actual
