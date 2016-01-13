import numpy as np
import scipy.stats as sts

def go(wps, p, ts):
    '''wps = words per speaker, p = prob of labeling correct, ts = size of test set'''

    classes = ['a', 'b', 'c', 'd']
    test_set = []
    for i in xrange(ts*wps):
        for c in classes:
            test_set.append(c)
            if len(test_set)==ts*wps:
                break
        if len(test_set)==ts*wps:
            break

    results = []
    for i in xrange(ts):
        selections = []
        for j in xrange(wps):
            rand = np.random.random()
            if rand < p:
                selections.append('y')
            else:
                selections.append(np.random.choice(['n1', 'n2', 'n3']))
        mode = max(set(selections), key=selections.count)
        if mode=='y':
            results.append(1)
        else:
            results.append(0)

    accuracy = np.sum(results)/float(len(results))
    print 'accuracy:', accuracy

if __name__ == '__main__':
    go(12, 0.323, 5000)