from cmath import log
import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
import winsound


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


# Setting standard filter requirements.
order = 6
fs = 10e6   
cutoff = 3.4e6 

b, a = butter_lowpass(cutoff, fs, order)

# Creating the data for filteration
path = 'Desktop/Laboratorio/Programacion-Automatizacion/Pyvisa/Output/Waveform/2022-03-24/b3_s3/b3_s3_'
num = np.linspace(0, 39, 50, dtype = int)

data =[]

for i in num:

    with open(path+str(i)+".txt") as file:
        for line in file: 
            line = line.strip() #or some other preprocessing
            data.append(float(line)) #storing everything in memory!

T = 0.6        # value taken in seconds
n = int(T * fs) # indicates total samples
t = np.linspace(0, T, n, endpoint=False)

# Filtering and plotting
y = butter_lowpass_filter(data, cutoff, fs, order)

#plt.subplot(2, 1, 2)
plt.plot(t, data, 'b-', label='data')
plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)
for i in range(3):
    winsound.Beep(650-i*100, 500-i*50)
plt.show()