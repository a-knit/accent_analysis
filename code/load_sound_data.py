from scipy.io.wavfile import read
import numpy as np

def load_sound(filename):
    return read(filename)



if __name__ == '__main__':
    filename = 'files/ebira/ebira1.wav'
    # filename2 = 'files/ebira/ebira1_2.wav'
    data = load_sound(filename)[1]
    # data2 = load_sound(filename2)
    np.savetxt('proposal_data_mat.csv', data, delimiter=',')