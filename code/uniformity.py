import numpy as np


def scale_to_n(times, formant, n=6):
    '''scale the formant data for an individual word into n partitions, all times are in seconds'''

    start = times[0]
    end = times[-1]

    result = []

    # determine the times we calculate formant values for
    timescale = np.linspace(start, end, n)

    for t in timescale:
        if t == start:
            result.append(formant[0])
        elif t == end:
            result.append(formant[-1])
        else:
            i2 = np.argmax(np.array(times)>t)
            i1 = i2 - 1

            # find the closest time and formant values before and after the chosen time
            before_f = formant[i1]
            after_f = formant[i2]
            before_t = times[i1]
            after_t = times[i2]

            # calculate an estimated formant value at the chosen time by placing it the line between the previous and next formant values we have data for
            new_f = (t - before_t) / (after_t - before_t) * (after_f - before_f) + before_f
            result.append(new_f)

    return np.array(result)