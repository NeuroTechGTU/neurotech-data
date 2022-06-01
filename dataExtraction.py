from asyncore import write
import csv
from fileinput import filename
import statistics
import string
from matplotlib.cbook import ls_mapper
import statistic
import pandas as pd
import os
import numpy as np
from pathlib import Path
from re import search

def extractdata(folder_name, csv_name):
    columns = ["Sensor4","Sensor3","Sensor2","Sensor1","Size"]
    exact_folder_path = folder_name+csv_name
    print(exact_folder_path)
    file = pd.read_csv(exact_folder_path, names=columns)

    counter = 0
    
    while counter < 4: 
        x = []
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
                    writer.writerow(arr)
                    f_low.close()
                flag = 1
            if(flag == 1):
                flag = 0
                break
                
        flag = 0
        for arr in standart_x:    
            final = "High_"
            path = folder_name+std_dev+"/high/"
            if not Path(path).is_dir():
                os.mkdir(folder_name+std_dev+"/high") 
            if(x[len(x) - 1] == statistics.stdev(arr) and num_lines <= 2):
                with open(path+ final+csv_name, "a",newline='') as f_high:
                    writer = csv.writer(f_high)
                    writer.writerow(arr)
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
