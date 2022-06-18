from ast import Return
from time import sleep
from pynput import keyboard
import os
import serial
import time

break_video = False
def on_press(key):
    global break_program
    global break_video 
    global next_video

    if key == keyboard.Key.shift:
        print ('Video completed\n')
        break_video = True

    if key == keyboard.Key.tab:
        print ('Test completed.\n')
        return False



DELAY = 500
PIECE = 10 #How many pieces a video will be divided

class video:
    def __init__(self, id=None, emotion_dev=None, emotion_test=None, device_data=None):
        self.id = id 
        self.emotion_dev = emotion_dev
        self.emotion_test = emotion_test
        self.device_data = device_data
    
    def to_file(self, filepath):
        with open(filepath, 'a') as f:
            f.write(str(self.id) + ',' + str(self.emotion_dev) + ',' + str(self.emotion_test) + ',' + str(self.device_data) +'\n')
            f.close()


class user:
    def __init__(self, id, sex=None, age=None, height=None, weight=None, location=None, emotional=None, frequency=None, video_data=None):
        self.id = id
        self.sex = sex #M:male F:female
        self.age = age
        self.location = location
        self.height = height
        self.weight = weight
        self.emotional = emotional #Y: emotional N: not emotional
        self.frequency = frequency #0: never 1: every year 2: every 6 months 3: every month 4: every week 5: every 1-3 days
        self.video_data = video_data
        self.videos = []

    def to_file(self, filepath):
        with open(filepath, 'a') as f:
            f.write(str(self.id) + ',' + str(self.sex) + ',' + str(self.age) + ',' + str(self.height) + ',' + str(self.weight) + ',' + str(self.location) + ',' + str(self.emotional) + ',' + str(self.frequency) + ',' + str(self.video_data) + '\n')
            f.close()


fd = open('data/user_count', 'r')
id = int(fd.readline())
fd.close()

user_data = user(id)

while True:
    print('Male(M) or Female(F): ')
    inp = input()
    if inp=='M' or inp=='F':
        user_data.sex = inp
        break
    else:
        print('Wrong input')

while True:
    print('Age:')
    inp=input()
    user_data.age = inp
    break

while True:
    print('Height:')
    inp=input()
    user_data.height = inp
    break

while True:
    print('Weight:')
    inp=input()
    user_data.weight = inp
    break

while True:
    print('Location:')
    inp=input()
    user_data.location = inp
    break

while True:
    print('Are you emotional? Yes(Y) No(N)')
    inp=input()
    if inp=='Y' or inp=='N':
        user_data.emotional = inp
        break
    else:
        print('Wrong input')

while True:
    print('How often do you watch movies or series on a scale of 5?\n0: never 1: every year 2: every 6 months 3: every month 4: every week 5: every 1-3 days')
    inp=input()
    if inp=='0' or inp=='1' or inp=='2' or inp=='3' or inp=='4' or inp=='5' or inp=='6':
        user_data.frequency  = inp
        break
    else:
        print('Wrong input')

sleep(.5)
print('Press tab when all videos are watched and test is completed.\n')
file_name = user_data.id

count = 0
with keyboard.Listener(on_press=on_press) as listener:
    while True:
        try:
            ser = serial.Serial('COM7', 115200)
            print(ser.readline())
        except:
           pass
        print('Port ' + str(ser.isOpen()) + ' is active.\n')         # check which port was really used
        user_data.videos.append(video(count))
        user_data.videos[count].device_data = 'data/device_data/u_' + str(user_data.id) + '/v_' + str(count) + '.csv'
        isExist = os.path.exists('data/device_data/u_' + str(user_data.id))
        
        if not isExist:
            os.makedirs('data/device_data/u_' + str(user_data.id))
       
        device_fd = open(user_data.videos[count].device_data, 'w+')
        sleep(1)
        ser.flushInput()
        sleep(1)

        time = 0
        print('Press shift to pause when a video is watched.\n')
        while break_video == False:
            video_data = video(id)
            data_str = str(ser.readline())
            data_str = data_str.replace("b'", '')
            data_str = data_str.replace("\\r\\n'", '')
            data_str = data_str.split('\\')[0]
            data_list = data_str.split(' ')
            sensor_num = data_list[0]
            
            if(sensor_num == ''):
                continue
            sensor_num = int(sensor_num)
            
            if len(data_list) > 1:
                sensor_val = float(data_list[1])
            else:
                sensor_val = 0
            sensor_num_ind = sensor_num
            while(sensor_num_ind > 0):
                sensor_num_ind -= 1
                device_fd.write(str(sensor_val) + ',')
                
            for sensor_num_ind in range(4 - sensor_num - 1):
                device_fd.write(str(sensor_val) + ',')
                data_str = str(ser.readline())
                data_str = data_str.replace("b'", '')
                data_str = data_str.replace("\\r\\n'", '')
                data_str = data_str.split('\\')[0]
                data_list = data_str.split(' ')
                sensor_val = float(data_list[1])
            device_fd.write(str(sensor_val) + ',' + str(time) + '\n')
            time += 1
        device_fd.close()
        print('S: Sadness D: Disgust A: Anger AN: Anticipation J: Joy/Comedy T: Trust F: Fear SU: Surprise NR: Not Relevant')
        
        user_data.videos[count].emotion_dev = input('(Team member should answer) Which emotion is tested?\n')
        user_data.videos[count].emotion_test = input('(User should answer) Which emotion did you feel? If you feel none of them choose NR.\n')
        count+=1
        cont = input("Do you want to continue? Yes(Y) No(N)\n")
        if cont == 'N':
            print('Press TAB to complete the test.\n')
            break

        break_video = False
    
    listener.join()
    
    user_data.video_data  = 'data/user_tests/u_' + str(user_data.id)
    for video in user_data.videos:
        video.to_file(user_data.video_data)

    user_data.to_file('data/users.csv')
    fd2 = open('data/users.csv', 'w+')
    fd2.write('\n')
    fd2.close()
    
    fd = open('data/user_count', 'w')
    id = int(fd.write(str(id+1)))
    fd.close()
  
