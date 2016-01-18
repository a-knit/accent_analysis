import numpy as np
import pandas as pd
from sklearn.cross_validation import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
import scipy.stats as sts
from undersample import undersample, smote
import matplotlib.pyplot as plt

def cross_val(model, X, y, sp=np.array([]), cv=5, word_=False, svm=False, samp_method=None):
    '''cross validate the given model, feature matrix, and labels
    cv determines the number of folds for validation
    word_ toggles to the word by word analysis and requires a speaker array, sp of speaker ids
    svm toggles to an svm validation which includes scaling X
    samp_method gives the option to smote or undersample the data prior to fitting the model'''

    obs = X.shape[0]
    if y.shape[0] != obs:
        return 'Error: X and y must have the same number of observations'

    if word_:
        speakers = set(sp.flatten())
        speakers = np.array(list(speakers))
        masks = create_folds(speakers.shape[0], cv)
    else:
        masks = create_folds(obs, cv)

    scores = []
    i = 0
    for mask in masks:
        if word_:
            sp_train = speakers[mask]
            sp_test = speakers[~mask]
            mask = np.in1d(sp, list(set(sp_train.flatten())))

        X_train, X_test, y_train, y_test = train_test(X, y, mask, svm=svm)

        # optional smoting and undersampling
        if samp_method=='smote':
            X_train, y_train = smote(X_train, y_train, .5, 'other')
        elif samp_method=='und':
            X_train, y_train = undersample(X_train, y_train, .75)
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        if word_:
            all_sp_test = sp[~mask]
            sp_pred, sp_actual = make_pred_by_speaker(all_sp_test, sp_test, y_pred, y_test)
            round_scores = calc_metrics(sp_pred, sp_actual)
        else:
            round_scores = calc_metrics(y_pred, y_test)
        scores.append(round_scores)
        i += 1
        print '%d%% completed' % (i*100/float(cv))

    return np.mean(scores, axis=0)
    # scores format: [accuracy, euro F1, other F1]


def create_folds(obs, cv):
    '''create cv folds randomly from the total observations, returned as a list of boolean arrays'''

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
    '''take predictions and test labels and return a list starting with accuracy followed by the F1 scores for each class'''

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
    '''create training and test sets based on a given mask indicating the training rows
    scale as well if svm is True'''

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
    '''make predictions for each speaker given the predictions for all words, only used in the word_ model'''

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
