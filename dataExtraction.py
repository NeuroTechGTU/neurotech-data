from asyncore import write
import csv
from fileinput import filename
import statistics
import string
import pandas as pd
import os
import numpy as np
from pathlib import Path
from re import search


########################################

# bu kod user testlerinin sensor verilerindeki en yuksek ve en dusuk 
# standart sapma verilerini bulur takip ettigi dosya yolu = data/device_data/USER_NUMBER/.CSV
# butun dosyalari tarayip en yuksek standart sapma degerini data/device_data/USER_NUMBER/std_dev/high
# en dusuk standart sapma degerini ise data/device_data/USER_NUMBER/std_dev/low pathine kaydeder.
# bu degerler her sensor icin bir tane olarak csv olarak kaydedilir. Ornek olarak 
# "data/device_data/u_1/std_dev/high/High_v_0.csv" pathi icin csv dosyasindaki satirlarin
#  okunmasi su sekildedir

    # 1.satir  = 4.sensor verilerini (28mm)
    # 2.satir  = 3.sensor verilerini (23mm)     -------- mm cinsinden verilmis uzakliklar -----
    # 3.satir  = 2.sensor verilerini (10mm)     ---------- ledlere olan uzakliklardir ---------
    # 4.satir  = 1.sensor verilerini (5mm)

# verilen ornek dosya uzantisinda ("data/device_data/u_1/std_dev/high/High_v_0.csv")
# csv dosyasi high klasoru icinde oldugu icin bu csv dosyasindaki sensor verileri 
# kisiye ozel olarak ayni isimle yapilmis test icin (ornege gore v_0.csv test datasi) 
# en yuksek standart sapma degerini tutar


#########################################

def extractdata(folder_name, csv_name):
    columns = ["Sensor4","Sensor3","Sensor2","Sensor1","Size"]
    exact_folder_path = folder_name+csv_name
    print(exact_folder_path)
    file = pd.read_csv(exact_folder_path, names=columns)

    counter = 0
    
    while counter < 4: 
        x = []
        temp = []
        if(counter == 0):
             standart_x = np.array_split(file.Sensor4,10)
        elif(counter == 1):
            standart_x = np.array_split(file.Sensor3,10)
        elif(counter == 2):
           standart_x = np.array_split(file.Sensor2,10)
        elif(counter == 3):
            standart_x = np.array_split(file.Sensor1,10)
        counter += 1

        for arr in standart_x:
            x.append(statistics.stdev(arr))

        x.sort()
        i = 0
        flag = 0
        std_dev = "std_dev"

        path = folder_name+std_dev+'/'
        num_lines = 0

        if not Path(path).is_dir():
            os.mkdir(folder_name+std_dev) 

        for arr in standart_x:
            final = "Low_"
            if(x[0] == statistics.stdev(arr) and num_lines < 2):
                path = folder_name+std_dev+"/low/"
                if not Path(path).is_dir():
                    os.mkdir(folder_name+std_dev+"/low") 
                with open(path+final+csv_name, "a",newline='') as f_low:
                    writer = csv.writer(f_low)
                    temp.append(statistics.fmean(arr))
                    temp.append(min(arr))
                    temp.append(max(arr))
                    writer.writerow(temp)
                    f_low.close()
                flag = 1
            if(flag == 1):
                flag = 0
                break
        temp = []
        flag = 0
        for arr in standart_x:    
            final = "High_"
            path = folder_name+std_dev+"/high/"
            if not Path(path).is_dir():
                os.mkdir(folder_name+std_dev+"/high") 
            if(x[len(x) - 1] == statistics.stdev(arr) and num_lines <= 2):
                with open(path+ final+csv_name, "a",newline='') as f_high:
                    writer = csv.writer(f_high)
                    temp.append(statistics.fmean(arr))
                    temp.append(min(arr))
                    temp.append(max(arr))
                    print(temp)
                    writer.writerow(temp)
                    f_high.close()
                flag = 1
            if(flag == 1):
                flag = 0
                break

       
        
folder_path = "data/device_data/"
list_of_files = os.listdir(folder_path)

for file_name in list_of_files:
    exact_folder_name = folder_path+file_name+'/'
    list_of_csv = os.listdir(exact_folder_name)
    for csv_name in list_of_csv:
        exact_folder_name = ""
        exact_folder_name = folder_path+file_name+'/'
        if((not "u_2" == file_name) and search("csv",csv_name)):
            extractdata(exact_folder_name,csv_name)
