from pymongo import MongoClient
from pulse_analysis import get_intervals, partition
import os
import pandas as pd
import numpy as np

def get_info(filename):
    '''extract information stored in filename'''

    info = filename.split('_')
    gender = info[0]
    country = info[1]
    language = info[2].strip('0123456789')
    return (gender, country, language)

def get_formants(file_, partitions):
    '''get the formant data for a particular speaker based off time partitions'''

    data = pd.read_csv(file_, sep='   ')
    data = data.replace(to_replace='--undefined--', value=np.nan)
    data = data.dropna(axis=0)
    data = data.astype(float)

    f_partitions = []
    i = 0
    for interval in partitions.iterrows():
        int_post = {}
        start = interval[1]['start']
        end = interval[1]['end']
        int_post['start'] = start
        int_post['end'] = end
        int_post['int_length'] = end - start
        subsection = data[(data.Time_s > start) & (data.Time_s < end)]
        int_post['time'] = list(subsection['Time_s'])
        int_post['F1'] = list(subsection['F1_Hz'])
        int_post['F2'] = list(subsection['F2_Hz'])
        int_post['F3'] = list(subsection['F3_Hz'])
        int_post['F4'] = list(subsection['F4_Hz'])
        int_post['index'] = i
        f_partitions.append(int_post)
        i += 1
    return f_partitions

def prepare_post(filename, directory, i):
    '''prepare the mongoDB post for a particular speaker'''

    info = get_info(filename)
    gender = info[0]
    country = info[1]
    language = info[2]
    family = directory.split('/')[-1]

    intervals = get_intervals(family, filename)
    partitions = partition(intervals)

    formant_file = directory + '/' + filename + '_formant.txt'
    formants = get_formants(formant_file, partitions)

    post = {'file': filename, 'family': family, 'language': language, 'country': country, 'word_formants': formants, 'gender': gender, 'index': i}
    return post


if __name__ == '__main__':
    client = MongoClient()
    db = client['project']
    collection = db['word_data']

    families = ['afroasiatic', 'european', 'indo_iranian', 'sino_tibetan']
    i = 0
    for fam in families:
        directory = './data/raw_praat/' + fam
        for fn in os.listdir(directory):
            parts = fn.split('_')
            if parts[-1] == 'formant.txt':
                filename = parts[0] + '_' + parts[1] + '_' + parts[2]
                post = prepare_post(filename, directory, i)
                collection.insert_one(post)
                i += 1
        print fam, ' completed'
    print i, ' posts added' # 1546 posts added
