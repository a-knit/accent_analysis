import numpy as np


def scale_to_n(times, formant, n=6):
    '''scale the formant data for an individual word into n partitions'''

    start = times[0]
    end = times[-1]

    result = []

    timescale = np.linspace(start, end, n)

    for t in timescale:
        if t == start:
            result.append(formant[0])
        elif t == end:
            result.append(formant[-1])
        else:
            i2 = np.argmax(np.array(times)>t)
            i1 = i2 - 1

            before_f = formant[i1]
            after_f = formant[i2]
            before_t = times[i1]
            after_t = times[i2]

            new_f = (t - before_t) / (after_t - before_t) * (after_f - before_f) + before_f
            result.append(new_f)

    return np.array(result)