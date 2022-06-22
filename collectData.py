from fileinput import close
import os
import pandas as pd
import csv

class csvFile:
    def __init__(self, sex=None, age= None, avg=None, max=None, min=None, bmi=None):
        self.sex = sex 
        self.age = age
        self.bmi = bmi ##0: underweight (<18.5), 1:normal(18.5-25), 2:overweight(25<) 
        self.avg = avg
        self.max = max
        self.min = min

    def append_to_file(self, f):
        writer = csv.writer(f)
        data = [self.sex, self.age, self.bmi, self.avg[0], self.max[0], self.min[0],self.avg[1], self.max[1], self.min[1],self.avg[2], self.max[2], self.min[2],self.avg[3], self.max[3], self.min[3]]
        writer.writerow(data)

def write_header(f):
        writer = csv.writer(f)
        header = ['sex','age','bmi','avg4','max4','min4','avg3','max3','min3','avg2','max2','min2','avg1','max1','min1']
        writer.writerow(header)

high = 0

if high == 1:
    file_format = 'high'
else:
    file_format = 'low'
##create file if it exist clear it
f_sad = open('data/model_data/sadness_' + file_format + '.csv', 'w')
f_disgust = open('data/model_data/disgust_' + file_format + '.csv', 'w')
f_anger = open('data/model_data/anger_' + file_format + '.csv', 'w')
f_anti = open('data/model_data/anticipation_' + file_format + '.csv', 'w')
f_joy = open('data/model_data/joy_' + file_format + '.csv', 'w')
f_trust = open('data/model_data/trust_' + file_format + '.csv', 'w')
f_fear = open('data/model_data/fear_' + file_format + '.csv', 'w')
f_surprise = open('data/model_data/surprise_' + file_format + '.csv', 'w')

write_header(f_sad)
write_header(f_disgust)
write_header(f_anger)
write_header(f_anti)
write_header(f_joy)
write_header(f_trust)
write_header(f_fear)
write_header(f_surprise)

df = pd.read_csv("data/users_edited.csv", header=None, delimiter=";")
df.columns = ['id', 'sex', 'age', 'height', 'weight', 'path']

for i in df.index:
    df_u = pd.read_csv(df['path'][i], header=None)
    df_u.columns = ['id','dev_emotion','user_emotion','path']
    for j in df_u.index:
        if df_u['user_emotion'][j] != 'NR':
            path = df_u['path'][j].split('/')
            if path[2] != '.DS_Store':
                if high == 1:
                    filepath = 'data/device_data/' + path[2] + '/std_dev/high/High_' + path[3]
                else:
                    filepath = 'data/device_data/' + path[2] + '/std_dev/low/Low_' + path[3]
                
                if os.path.isfile(filepath):
                    testFile = csvFile()
                    df_test = pd.read_csv(filepath, header=None)
                    df_test.columns = ['mean','min','max']
                    testFile.avg = df_test['mean'].to_list()
                    testFile.min = df_test['min'].to_list()
                    testFile.max = df_test['max'].to_list()
                    if df['sex'][i] == 'M':
                        testFile.sex = 0
                    else:
                        testFile.sex = 1
                    testFile.age = df['age'][i]

                    height = df['height'][i]
                    weight = df['weight'][i]
                    
                    if height == 0 or weight == 0:
                        bmi = 20
                    else:
                        bmi = weight / (height/100)**2
                    
                    if bmi < 18.5:
                        testFile.bmi = 0
                    elif bmi > 18.5 and bmi < 25:
                        testFile.bmi = 1
                    elif bmi > 25:
                        testFile.bmi = 2
                    
                    if df_u['user_emotion'][j] == 'S':
                        testFile.append_to_file(f_sad)
                        print("Data successfully written from the file: " + filepath + " to the file: " + 'data/model_data/sadness_' + file_format + '.csv')
                    elif df_u['user_emotion'][j] == 'D':
                        testFile.append_to_file(f_disgust)
                        print("Data successfully written from the file: " + filepath + " to the file: " + 'data/model_data/disgust_' + file_format + '.csv')
                    elif df_u['user_emotion'][j] == 'A':
                        testFile.append_to_file(f_anger)
                        print("Data successfully written from the file: " + filepath + " to the file: " + 'data/model_data/anger_' + file_format + '.csv')
                    elif df_u['user_emotion'][j] == 'AN':
                        testFile.append_to_file(f_anti)
                        print("Data successfully written from the file: " + filepath + " to the file: " + 'data/model_data/anticipation_' + file_format + '.csv')
                    elif df_u['user_emotion'][j] == 'J':
                        testFile.append_to_file(f_joy)
                        print("Data successfully written from the file: " + filepath + " to the file: " + 'data/model_data/joy_' + file_format + '.csv')
                    elif df_u['user_emotion'][j] == 'T':
                        testFile.append_to_file(f_trust)
                        print("Data successfully written from the file: " + filepath + " to the file: " + 'data/model_data/trust_' + file_format + '.csv')
                    elif df_u['user_emotion'][j] == 'F':
                        testFile.append_to_file(f_fear)
                        print("Data successfully written from the file: " + filepath + " to the file: " + 'data/model_data/fear_' + file_format + '.csv')
                    elif df_u['user_emotion'][j] == 'SU':
                        testFile.append_to_file(f_surprise)
                        print("Data successfully written from the file: " + filepath + " to the file: " + 'data/model_data/surprise_' + file_format + '.csv')

f_sad.close()
f_disgust.close()
f_anger.close()
f_anti.close()
f_joy.close()
f_trust.close()
f_fear.close()
f_surprise.close()