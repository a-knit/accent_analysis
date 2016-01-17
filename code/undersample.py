import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier



def undersample(X, y, target, sp=np.array([])):
    """
    INPUT:
    X, y - your data
    target - the intended percentage of positive
             class observations in the output
    OUTPUT:
    X_undersampled, y_undersampled - undersampled data
    `undersample` randomly discards negative observations from
    X, y to achieve the target proportion
    """
  
    num_pos = np.sum([y!='european'])

    if target < num_pos/float(len(y)):
        return X, y

    # determine how many negative (majority) observations to retain
    positive_count = num_pos
    negative_count = len(y) - positive_count
    keep_count = positive_count*(1-target)/target
    keep_count = int(round(keep_count))
    
    # randomly discard negative (majority) class observations
    keep_array = np.array([True]*keep_count + [False]*(negative_count-keep_count))
    np.random.shuffle(keep_array)
    X_positive, y_positive = X[y!='european'], y[y!='european']
    X_negative = X[y=='european']
    X_negative_undersampled = X_negative[keep_array]
    y_negative = y[y=='european']
    y_negative_undersampled = y_negative[keep_array]
    X_undersampled = np.vstack((X_negative_undersampled, X_positive))
    y_undersampled = np.concatenate((y_negative_undersampled, y_positive))


    if sp != np.array([]):
        sp_positive = sp[y!='european']
        sp_negative = sp[y=='european']
        sp_negative_undersampled = sp_negative[keep_array]
        sp_undersampled = np.concatenate((sp_negative_undersampled, sp_positive))

        return X_undersampled, y_undersampled, sp_undersampled
    else:
        return X_undersampled, y_undersampled


def smote(X, y, target, family, k=None, sp=np.array([])):
    """
    INPUT:
    X, y - your data
    target - the percentage of positive class 
             observations in the output
    k - k in k nearest neighbors
    OUTPUT:
    X_oversampled, y_oversampled - oversampled data
    `smote` generates new observations from the positive (minority) class:
    For details, see: https://www.jair.org/media/953/live-953-2037-jair.pdf
    """
    if target <= np.sum([y==family])/float(len(y)):
        return X, y
    if k is None:
        k = len(X)**.5

    # fit kNN model
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X[y==family], y[y==family])
    neighbors = knn.kneighbors()[0]
    positive_observations = X[y==family]

    # determine how many new positive observations to generate
    positive_count = np.sum([y==family])
    negative_count = len(y) - positive_count
    target_positive_count = target*negative_count / (1. - target)
    target_positive_count = int(round(target_positive_count))
    number_of_new_observations = target_positive_count - positive_count

    # generate synthetic observations
    synthetic_observations = np.empty((0, X.shape[1]))
    while len(synthetic_observations) < number_of_new_observations:
        obs_index = np.random.randint(len(positive_observations))
        observation = positive_observations[obs_index]
        neighbor_index = np.random.choice(neighbors[obs_index])
        neighbor = X[neighbor_index]
        obs_weights = np.random.random(len(neighbor))
        neighbor_weights = 1 - obs_weights
        new_observation = obs_weights*observation + neighbor_weights*neighbor
        synthetic_observations = np.vstack((synthetic_observations, new_observation))

    X_smoted = np.vstack((X, synthetic_observations))
    y_smoted = np.concatenate((y, [family]*len(synthetic_observations)))

    return X_smoted, y_smoted
