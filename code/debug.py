import pandas as pd
import numpy as np
from pymongo import MongoClient




if __name__ == '__main__':
    i = 3

    client = MongoClient()
    db = client['project']
    collection = db['word_data']

    entry = collection.find_one({'index': i})
    print 'file:', entry['file']
    for word in entry['word_formants']:
        print 'len:', len(word['F1']), 'index:', word['index'], 'int:', word['int_length'], 'start', word['start'], 'end', word['end']
