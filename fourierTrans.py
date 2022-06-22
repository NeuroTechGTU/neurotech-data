import csv
import os
from pathlib import Path
import shutil
import statistics
import numpy as np
import pandas as pd
from scipy import pi
from scipy.fftpack import fft
import matplotlib.pyplot as plt

def plot_graph(path, file_name):
    csv_file = path + '/fourier/' + file_name
    col_list = ["S1", "S2", "S3", "S4"]
    results = pd.read_csv(csv_file, names=col_list)

    ##prepare time domain signal
    sample_rate = 2
    y = len(results)
    N = len(results) * sample_rate


    for j in range(0,4):
        for i in range(0, len(results)):
            results.iloc[i, j].replace('(', '')
            results.iloc[i, j].replace(')', '')
            results.iloc[i, j] = complex(results.iloc[i, 0])
        

    frequency = np.linspace (0.0, sample_rate/2, int (N/2))
    y1 = 2/N * np.abs (results['S1'] [0:np.int64 (N/2)])
    y2 = 2/N * np.abs (results['S2'] [0:np.int64 (N/2)])
    y3 = 2/N * np.abs (results['S3'] [0:np.int64 (N/2)])
    y4 = 2/N * np.abs (results['S4'] [0:np.int64 (N/2)])

    #plt.plot(frequency, y)
    #plt.title('Frequency domain Signal')
    #plt.xlabel('Frequency in Hz')
    #plt.ylabel('Amplitude')
    #plt.savefig(path + '/fourierTrans' + file_name + '.png')

    #create directory if it doesn't exist
    while not os.path.exists(path + '/f_dev'):
        os.makedirs(path + '/f_dev')

    # create file if it exist clear it
    f_dev = open(path + '/f_dev/' + file_name, 'w')
    ## remove directory
    
    header = ['mean', 'min', 'max']
    writer = csv.DictWriter(f_dev, fieldnames=header)
    #writer.writeheader()
    writer.writerow({'mean': statistics.mean(y1), 'min': min(y1), 'max': max(y1)})
    writer.writerow({'mean': statistics.mean(y2), 'min': min(y2), 'max': max(y2)})
    writer.writerow({'mean': statistics.mean(y3), 'min': min(y3), 'max': max(y3)})
    writer.writerow({'mean': statistics.mean(y4), 'min': min(y4), 'max': max(y4)})


    f_dev.close()

##read all folder names in the device_data folder
folder_names = os.listdir("data/device_data")
file_name_list = list()
##read all files in the folders in the folder_names
for folder_name in folder_names:
    if folder_name == ".DS_Store":
        continue
    file_names = os.listdir("data/device_data/"+folder_name)
    for file_name in file_names:
        if file_name != ".DS_Store" and file_name != "std_dev" and file_name != "fourier" and file_name != "f_dev":
            #read the csv file
            csv_file = open("data/device_data/"+folder_name+"/"+file_name,"r",encoding="utf-8")
            read_csv_file = csv_file.read()
            line_csv_file = read_csv_file.split("\n")
            # N :Number of sample points , -1 for the extra line read at the end
            N = len(line_csv_file)-1

            sensor1=list()
            sensor2=list()
            sensor3=list()
            sensor4=list()
            i=0
            j=0

            while(i<N):
                splited_csv_file = line_csv_file[i].split(",")
                sensor1.append(splited_csv_file[0])
                sensor2.append(splited_csv_file[1])
                sensor3.append(splited_csv_file[2])
                sensor4.append(splited_csv_file[3])
                i+=1

            #convert the string to float if string is not empty
            sensor1 = [float(i) for i in sensor1 if i != ""]
            sensor2 = [float(i) for i in sensor2 if i != ""]
            sensor3 = [float(i) for i in sensor3 if i != ""]
            sensor4 = [float(i) for i in sensor4 if i != ""]

            #Fast Fourier transform to each sensor data
            F1 = np.fft.fft(sensor1)
            F2 = np.fft.fft(sensor2)
            F3 = np.fft.fft(sensor3)
            F4 = np.fft.fft(sensor4)
            #save the values in csv
            # create a new folder
            if not os.path.exists("data/device_data/"+folder_name + '/fourier'):
                os.makedirs("data/device_data/"+folder_name + '/fourier')
            
            csv_file = open('data/device_data/' + folder_name + '/fourier/' + file_name, 'w', encoding="utf-8")
            
            for i in range(len(F1)):
                csv_file.write(str(F1[i])+","+str(F2[i])+","+str(F3[i])+","+str(F4[i])+"\n")
            csv_file.close()
            print("fourier transform done for data/device_data/" + folder_name + '/fourier/' + file_name)
            plot_graph("data/device_data/" + folder_name, file_name)