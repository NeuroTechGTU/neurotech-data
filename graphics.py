import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


columns = ["Sensor4","Sensor3","Sensor2","Sensor1","Size"]
file = pd.read_csv("data/device_data/u_25/v_2.csv", names=columns)

fig, ax = plt.subplots()
fig.set_size_inches(13, 8, forward=True)
# x = range(file.Sensor4.size)
x = np.arange(0, file.Sensor4.size, 1)
y = []

y = file.Sensor1;

ax.plot(x,y, label='29mm');
ax.plot(x,file.Sensor3,label='24mm')
ax.plot(x, file.Sensor2,label='10mm')
ax.plot(x, file.Sensor4,label='5mm')
ax.legend(loc='upper right',prop={'size': 6})

plt.savefig('data/figures/u_25/line/v2.png')