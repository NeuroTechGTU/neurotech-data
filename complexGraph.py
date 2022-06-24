# import library
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import pi
from scipy.fftpack import fft
  
# create data of complex numbers
# read csv file
col_list = ["S1", "S2", "S3", "S4"]
csv_file = "data/device_data/u_28/fourier/v_4.csv"
results = pd.read_csv(csv_file, names=col_list)

##prepare time domain signal
sample_rate = 2
y = len(results)
N = len(results) * sample_rate
time = np.linspace(0, len(results), N)

# frequency componenets
freq1 = 60
magnitude1 = 25
freq2 = 270
magnitude2 = 2

waveform1 = magnitude1 * np.sin (2 * pi * freq1 * time)
waveform2 = magnitude2 * np.sin (2 * pi * freq2 * time)

#noise component
# create np array from pandas dataframe
#noise = np.array(results['S1'], dtype=float)
#noise.shape = (len(noise), 1)
#time_data = waveform1 + waveform2 + noise


#plt.plot (time [0:y], time_data [0:y])
#plt.title ('Time Domain Signal')
#plt.xlabel ('Time')
#plt.ylabel ('Amplitude')
#plt.show ()

for i in range(0, len(results)):
    results.iloc[i, 0].replace('(', '')
    results.iloc[i, 0].replace(')', '')
    results.iloc[i, 0] = complex(results.iloc[i, 0])

frequency = np.linspace (0.0, sample_rate/2, int (N/2))
freq_data = results['S1']
y = 2/N * np.abs (freq_data [0:np.int64 (N/2)])


plt.plot(frequency, y)
plt.title('Frequency domain Signal')
plt.xlabel('Frequency in Hz')
plt.ylabel('Amplitude')
plt.show()