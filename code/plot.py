import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_nth_word(X, y, n, f_per_word):
    '''takes in X and y from the speaker model and plots the nth word with mean(F2) on the x axis and mean(F1) on the y axis'''

    X_list = [X[y=='afroasiatic'], X[y=='european'], X[y=='indo_iranian'], X[y=='sino_tibetan']]
    color_list = ['orange', 'lavender', 'fuchsia', 'olive']

    for i in xrange(4):
        X = X_list[i]
        color = color_list[i]
        F1 = []
        F2 = []

        for j in xrange(X.shape[0]):
            start_F1 = (n - 1) * f_per_word * 4
            start_F2 = start_F1 + f_per_word
            end_F2 = start_F2 + f_per_word
            F1.append(np.mean(X[j, start_F1:start_F2]))
            F2.append(np.mean(X[j, start_F2:end_F2]))

        plt.scatter(F2, F1, alpha=.5, color=color)

    # plt.title('%dth word' % n)
    # plt.show()

def plot_n_words(X, y, n, f_per_word):
    '''takes in X and y from the speaker model and plots the nth word with mean(F2) on the x axis and mean(F1) on the y axis'''

    X_list = [X[y=='afroasiatic'], X[y=='european'], X[y=='indo_iranian'], X[y=='sino_tibetan']]
    color_list = ['orange', 'lavender', 'fuchsia', 'olive']

    for i in xrange(4):
        X = X_list[i]
        color = color_list[i]
        F1 = []
        F2 = []

        for j in xrange(n):
            start_F1 = j * f_per_word * 4
            start_F2 = start_F1 + f_per_word
            end_F2 = start_F2 + f_per_word
            F1.append(np.mean(X[:, start_F1:start_F2]))
            F2.append(np.mean(X[:, start_F2:end_F2]))

        plt.scatter(F2, F1, alpha=.5, color=color)

    plt.title('First %d words' % n)
    plt.show()
