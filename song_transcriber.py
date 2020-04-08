from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt



##########################################################################

# Musical Note Utilities

##########################################################################

def note_fundamental_freqs(scale=1.):
    '''hard coded, but potentially scaled fundamental frequencies of all the notes'''
    return {'C0':16.35*scale, 'Cs0':17.32*scale,
            'D0':18.35*scale,'Ds0':19.45*scale,'E0':20.6*scale,
            'F0':21.83*scale,'Fs0':23.12*scale,'G0':24.5*scale,
            'Gs0':25.96*scale,'A0':27.5*scale,'As0':29.14*scale,
            'B0':30.87*scale}



def note_octive_freqs(octives=6,scale=1., only = {'C','Cs','D','Ds','E','F','G','Gs','A','As','B'} , styling=False):
    '''
    use the fundamental frequencies for the notes to find the higher octives of the notes
    
    Params:
        octives : int (optional)
            the number of octives for each note to draw a line for in the plot
            
        scale : float (optional)
            a scaling of the fundamental frequencies for each note 
            
        only : set (optional)
            a set of the notes that you want to draw
            for instance can be the notes of a particular scale 
            
        styling : bool (optional)
            a hacky way to get matplotlib info associated with each note for pretty plots
    
    '''
    fundamental_freqs = note_fundamental_freqs(scale=scale)
    
    octive_freqs = {}#fundamental_freqs.copy()
    
    for o in range(-1,octives+1):
        # can avoid a for loop by making a a copy of the fundamental freqs, changing the keys and vals, then adding it to fundamental_freqs?
        for f in fundamental_freqs:
            #print(f[:-1])
            if(styling):
                styles = {'C':('r','-'), 'Cs':('r','--'),
                          'D':('y','-'),'Ds':('r','--'),'E':('g','-'),
                          'F':('c','-'),'Fs':('c','--'),'G':('b','-'),
                          'Gs':('b','--'),'A':('m','-'),'As':('m','--'),
                          'B':('w','-')}
                if f[:-1] in only: octive_freqs[f[:-1]+str(o+1)] = (fundamental_freqs[f] * 2 ** (o+1),styles[f[:-1]][0],styles[f[:-1]][1])
            else:
                if f[:-1] in only: octive_freqs[f[:-1]+str(o+1)] = fundamental_freqs[f] * 2 ** (o+1)

    
    return octive_freqs



def draw_note_freq_lines(octives=6,scale=1.,only={'C','Cs','D','Ds','E','F','G','Gs','A','As','B'}):
    '''
    draw pretty lines corresponding to the frequenies of some notes
    
    needs a plot to already be made
    
    Params are for note_octive_freqs and note_fundamental_freqs
    '''
    
    
    notes = note_octive_freqs(octives=octives,scale=scale,only=only,styling=True)
    for n in notes:
        if( n[:-1] in only ): plt.axvline(x=notes[n][0],label=n,color=notes[n][1],ls=notes[n][2])


def c_major_scale(): return {'C','D','E','F','G','A','B'}



##########################################################################

# Sound File Processing

##########################################################################



def fourier_transform_wav(wav,f_res=5):
    '''
    fourier transforms a .wav final and bins the fourier transforms to make an amplitude vs frequency vs time array for the 
    
    sound in the .wav file
    
    Params:
        wav : string
            the file name including .wav e.g. 'foo.wav'
        
        f_res : int
            f_res = 1/time_res
            used to break up the sample rate of the entire .wav file into smaller bins
    
    Returns:
        final : numpy array
            amplitude vs frequency vs time array
    
    '''
    fs, data = wavfile.read(wav)
    #f_res = 5
    tot_ind = (len(data)//(fs//f_res))

    final = np.empty((0,fs//(f_res*2)))
    
    for i in range(tot_ind):
        #print(i,tot_ind)
        begin = i*(fs//f_res)
        end = (i+1)*(fs//f_res) 

        row = np.fft.fft(data[begin:end])
        freqs = np.fft.fftfreq(len(row))*f_res*2*len(row)
        row = row[:len(row)//2]
        freqs = freqs[:len(freqs)//2]
        
        final = np.concatenate((final,np.array([(row * np.conj(row)).real])),axis=0)

    return final


if __name__ == "__main__":
    

    #all_freqs()
    freq_v_time = fourier_transform_wav("foo.wav")
    
    plt.imshow(final,interpolation = 'spline36',aspect = 'auto',extent = (0,freqs[-1],len(data)//fs,0))
    plt.xscale('log')
    draw_note_freq_lines(octives=9,only=c_major_scale())
    plt.show()
    
