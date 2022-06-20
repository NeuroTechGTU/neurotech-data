from cgi import test
import numpy as np
from numpy import loadtxt
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.metrics import Precision, Recall
from sklearn.preprocessing import OneHotEncoder

# load the dataset
dataset = pd.read_csv('all_high.csv')
print(dataset.head())
#dataset = loadtxt('total.csv', delimiter=',')
row_count = dataset.shape[0]
train_count = int(row_count * 0.8)
test_count = row_count - train_count
OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
OH_encoder = OH_encoder.fit(dataset[['emotion']])
categorical = pd.DataFrame(OH_encoder.transform(dataset[['emotion']]))
dataset.drop('emotion', axis=1, inplace=True)
dataset = pd.concat([dataset, categorical], axis=1)
dataset = dataset.to_numpy()

np.random.shuffle(dataset)

X_test = dataset[:test_count, 0:15]
Y_test = dataset[:test_count, 15]

# split into input (X) and output (y) variables
X = dataset[test_count:,0:15]
y = dataset[test_count:,15:]
# define the keras model
model = Sequential()
model.add(Dense(15, input_dim=15 ))
model.add(Dense(50, activation='relu'))
model.add(Dense(8, activation='sigmoid'))
# compile the keras model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy', Precision(), Recall()])
# fit the keras model on the dataset
model.fit(X, y, epochs=350, batch_size=15)
# evaluate the keras model
_, accuracy, prec, recall = model.evaluate(X, y)
model.save_weights('model.h5')
print('Accuracy: %.2f' % (accuracy*100), 'Precision: %.2f' % (prec*100), 'Recall: %.2f' % (recall*100))
