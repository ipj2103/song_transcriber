from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import find_peaks



##########################################################################

# Musical Notes

##########################################################################

class MusicNotes:
    
    
    def __init__(self,octives=6,scale=1.,only={'C','Cs','D','Ds','E','F','G','Gs','A','As','B'},plot_styling=False):
        self.scale = scale
        self.octives = octives
        self.only = only
        self.plot_styling = plot_styling
        
        self.fundamental_freqs = self.fundamental_note_freqs()
        self.octive_freqs = self.octive_note_freqs()
        
        
    
    def fundamental_note_freqs(self):
        '''hard coded, but potentially scaled fundamental frequencies of all the notes'''
        return {'C0':16.35*self.scale, 'Cs0':17.32*self.scale,
            'D0':18.35*self.scale,'Ds0':19.45*self.scale,'E0':20.6*self.scale,
            'F0':21.83*self.scale,'Fs0':23.12*self.scale,'G0':24.5*self.scale,
            'Gs0':25.96*self.scale,'A0':27.5*self.scale,'As0':29.14*self.scale,
            'B0':30.87*self.scale}
    
    
    
    def octive_note_freqs(self):
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
        
        self.octive_freqs = {}#fundamental_freqs.copy()
        
        for o in range(-1,self.octives+1):
            # can avoid a for loop by making a a copy of the fundamental freqs, changing the keys and vals, then adding it to fundamental_freqs?
            for f in self.fundamental_freqs:
                #print(f[:-1])
                if(self.plot_styling):
                    styles = {'C':('r','-'), 'Cs':('r','--'),
                              'D':('y','-'),'Ds':('r','--'),'E':('g','-'),
                              'F':('c','-'),'Fs':('c','--'),'G':('b','-'),
                              'Gs':('b','--'),'A':('m','-'),'As':('m','--'),
                              'B':('w','-')}
                    if f[:-1] in self.only: self.octive_freqs[f[:-1]+str(o+1)] = (self.fundamental_freqs[f] * 2 ** (o+1),styles[f[:-1]][0],styles[f[:-1]][1])
                else:
                    if f[:-1] in self.only: self.octive_freqs[f[:-1]+str(o+1)] = self.fundamental_freqs[f] * 2 ** (o+1)
    
        
        #print(self.octive_freqs)
        return self.octive_freqs
    
    
    def draw_freq_lines(self):#(octives=6,scale=1.,only={'C','Cs','D','Ds','E','F','G','Gs','A','As','B'}):
        '''
        draw pretty lines corresponding to the frequenies of some notes
        
        needs a plot to already be made
        
        Params are for note_octive_freqs and note_fundamental_freqs
        '''
        #(octives=octives,scale=scale,only=only,styling=True)
        if(self.plot_styling):
            for n in self.octive_freqs:
                if( n[:-1] in self.only ): plt.axvline(x=self.octive_freqs[n][0],label=n,color=self.octive_freqs[n][1],ls=self.octive_freqs[n][2])
        else:
            raise ValueError("Don't try to draw without the styling")



def c_major_scale(): return {'C','D','E','F','G','A','B'}


##########################################################################

# Sound File Data Processing

##########################################################################

class AudioData:
    
    def __init__(self,audio_file_name,tempo=0):
        self.sample_rate, self.audio_data = wavfile.read(audio_file_name)#self.import_audio_file(audio_file_name)#
        self.tempo = tempo
        self.title = audio_file_name
        
        
    def import_audio_file(wav_file_name):
        '''
        hiding a check for the file being a .wav file 
        '''
        raise NotImplemented("still need to figure out if this actually works right")
        assert wav_file_name[-4:] == '.wav' # make sure that you give it a .wav file 
        return wavfile.read(wav_file_name)
    
    
    
    def fourier_time_space(self):
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
        f_res = 5  # do something with the tempo to find the necessary f_res; 1/self.tempo or something ?
        tot_ind = (len(self.audio_data)//(self.sample_rate//f_res))
        
        self.fourier_space = np.empty((0,self.sample_rate//(f_res*2)))
        
        for i in range(tot_ind):
            #print(i,tot_ind)
            begin = i*(self.sample_rate//f_res)
            end = (i+1)*(self.sample_rate//f_res) 
    
            row = np.fft.fft(self.audio_data[begin:end])
            self.freqs = np.fft.fftfreq(len(row))*f_res*2*len(row)
            row = row[:len(row)//2]
            self.freqs = self.freqs[:len(self.freqs)//2]
            
            self.fourier_space = np.concatenate((self.fourier_space,np.array([(row * np.conj(row)).real])),axis=0)
        
        return self.fourier_space      
    
    
    def find_notes_in_audio(self,threshold):
        '''
        an extremely simple way to try and tell if a note exists in the audio 
        
        if the max of that frequency slice is above some threshold the onte is in the song 
        
        probably not the best way to do that 
        '''
        
        #raise NotImplemented("")
        
        scaled_notes = MusicNotes(scale=1./self.freqs[1]).octive_freqs
        found_notes=[]
        for note in scaled_notes:
            note_freq = scaled_notes[note]
            #print(note_freq)
            frequecny_slice = self.fourier_space[:,int(note_freq)]
            if(max(frequecny_slice)>threshold):# not a good method likely 
                found_notes.append(note)
        return found_notes
        
        
    def is_note_in_song(self,note):
        raise NotImplemented("")
        #find_peaks(self.fourier_space[][])#scipy.signal
    
    
    
    def plot_frequency_timeline(self):
          freq_v_time = self.fourier_time_space()
          
          ax = plt.subplot(1,1,1)
          pplot = ax.imshow(freq_v_time,interpolation = 'spline36',aspect = 'auto',extent = (0,self.freqs[-1],len(self.audio_data)//self.sample_rate,0))
          
          all_notes = MusicNotes(plot_styling=True,only=c_major_scale(),scale=1./self.freqs[1])
          all_notes.draw_freq_lines()
          
          plt.xscale('log')
          plt.xlabel('Frequency (Hz/'+str(self.freqs[1])+')')
          plt.ylabel('Time (s)')
          plt.colorbar(pplot,label = 'Amplitude')
          plt.title(str(self.title[:-4])+' Frequency Breakdown ')
          plt.show()



if __name__ == "__main__":
    
    foo = AudioData('foo.wav')
    
    foo.plot_frequency_timeline()
    print(foo.find_notes_in_audio(5e13))
    
    
    
    #print(foo.sample_rate)
    #freq_v_time = foo.fourier_time_space()
    
    #all_freqs()
    #freq_v_time = fourier_transform_wav("foo.wav")
    
    #plt.imshow(freq_v_time,interpolation = 'spline36',aspect = 'auto',extent = (0,foo.freqs[-1],len(foo.audio_data)//foo.sample_rate,0))
    #plt.xscale('log')
    #draw_note_freq_lines(octives=9,only=c_major_scale())
    #plt.show()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

# old not objectified fucns
'''
def note_fundamental_freqs(scale=1.):
    return {'C0':16.35*scale, 'Cs0':17.32*scale,
            'D0':18.35*scale,'Ds0':19.45*scale,'E0':20.6*scale,
            'F0':21.83*scale,'Fs0':23.12*scale,'G0':24.5*scale,
            'Gs0':25.96*scale,'A0':27.5*scale,'As0':29.14*scale,
            'B0':30.87*scale}



def note_octive_freqs(octives=6,scale=1., only = {'C','Cs','D','Ds','E','F','G','Gs','A','As','B'} , styling=False):

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

    
    notes = note_octive_freqs(octives=octives,scale=scale,only=only,styling=True)
    for n in notes:
        if( n[:-1] in only ): plt.axvline(x=notes[n][0],label=n,color=notes[n][1],ls=notes[n][2])



'''


   
'''
def fourier_transform_wav(wav,f_res=5):

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
'''

