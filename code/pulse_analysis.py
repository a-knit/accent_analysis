import pandas as pd
import numpy as np

def get_intervals(family, filename):
    '''extract the interval amounts between each pulse in the pulse data'''

    file_ = 'data/raw_praat/' + family + '/' + filename + '_pulse.txt'
    df = pd.read_csv(file_)
    df['interval'] = -df['Time_s'].diff(-1)
    return df

def partition(df):
    '''partition the audio file into words based on where there are large distances
    between pulses'''

    nint = df['interval'].quantile(.9)
    result = pd.DataFrame()
    result['start'] = df['Time_s'].shift(-1)[df.interval > (nint*1.5)]
    result['start'] = result['start'].shift(1)
    result['start'].iloc[0] = df['Time_s'].iat[0]
    result['end'] = df['Time_s'][df.interval > (nint*1.5)]
    result = result[result.start != result.end]
    return result

if __name__ == '__main__':
    pass
    # df1 = get_intervals('afroasiatic', 'm_iraq_arabic12')
    # df2 = get_intervals('european', 'f_brazil_portuguese37')
    # df3 = get_intervals('indo_iranian', 'f_iran_farsi16')
    # df4 = get_intervals('sino_tibetan', 'f_china_cantonese14')
    # df1 = partition(df1)
    # df2 = partition(df2)
    # df3 = partition(df3)
    # df4 = partition(df4)