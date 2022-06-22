import numpy as np
import matplotlib.pyplot as plt


#first read the datas from data\device_data\u_N , N is the number of the experiment order

csv_file = open("data/device_data/u_1/v_0.csv","r",encoding="utf-8")
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

#Fast Fourier transform
F = np.fft.fft(sensor1)
print(F)

    







