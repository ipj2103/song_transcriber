from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt

if __name__ == "__main__":
    fs, data = wavfile.read("foo.wav")
    f_res = 5
    tot_ind = (len(data)//(fs//f_res))

    final = np.empty((0,fs//(f_res*2)))
    
    for i in range(tot_ind):
        print(i,tot_ind)
        begin = i*(fs//f_res)
        end = (i+1)*(fs//f_res) 

        row = np.fft.fft(data[begin:end])
        freqs = np.fft.fftfreq(len(row))*f_res*2*len(row)
        row = row[:len(row)//2]
        freqs = freqs[:len(freqs)//2]
        
        final = np.concatenate((final,np.array([(row * np.conj(row)).real])),axis=0)

    plt.imshow(final,interpolation = 'spline36',aspect = 'auto',extent = (0,freqs[-1],len(data)//fs,0))
    plt.show()
    
