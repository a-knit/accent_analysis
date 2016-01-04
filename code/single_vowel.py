import pandas as pd
import numpy as np
import sklearn as skl

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