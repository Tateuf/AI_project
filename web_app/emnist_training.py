import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import cv2
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras.models import Sequential, load_model
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras import layers
from keras.layers import *
from keras.utils import np_utils
from tqdm import tqdm

#for dirname, _, filenames in os.walk('kaggle/input'):
#    for filename in filenames:
#        print(os.path.join(dirname, filename))
        
train_df = pd.read_csv('kaggle/input/emnist/emnist-balanced-train.csv', header=None)
test_df = pd.read_csv('kaggle/input/emnist/emnist-balanced-test.csv', header=None)
#print(train_df.head())

label_map = pd.read_csv("kaggle/input/emnist/emnist-balanced-mapping.txt", 
                        delimiter = ' ', 
                        index_col=0, 
                        header=None, 
                        squeeze=True)
#print(label_map.head())

#Initialising an empty dictionary
label_dictionary = {}

i = 0
#Running a loop for ASCII equivalent to character conversion
for index, label in enumerate(label_map):
    #if i>=10:
        label_dictionary[index-10] = chr(label)
    #i += 1
#print(label_dictionary)

#train_df_new = train_df[train_df[0].isin(np.arange(10, 47))] #onlyletter
#train_df_new.loc[train_df_new[0] >= 10 , 0] = train_df_new[0] - 10

#test_df_new = test_df[test_df[0].isin(np.arange(10, 47))] #onlyletter
#test_df_new.loc[test_df_new[0] >= 10 , 0] = test_df_new[0] - 10

#print(train_df_new)
train_df.reset_index(inplace=True)
test_df.reset_index(inplace=True)
#print(train_df_new)

x_train = train_df.loc[:, 1:]
y_train = train_df.loc[:, 0]

x_test = test_df.loc[:, 1:]
y_test = test_df.loc[:, 0]
#print(x_train.shape, y_train.shape)

def flip_and_rotate(image):
    W = 28
    H = 28
    image = image.reshape(W, H)
    image = np.fliplr(image)
    image = np.rot90(image)
    return image

x_train = np.apply_along_axis(flip_and_rotate, 1, x_train.values)
x_test = np.apply_along_axis(flip_and_rotate, 1, x_test.values)
#print(x_train.shape)

x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') /255
#print(x_train[0])

number_of_classes = y_train.nunique()
#print(number_of_classes)

y_train = np_utils.to_categorical(y_train, number_of_classes)
y_test = np_utils.to_categorical(y_test, number_of_classes)
#print(y_train.shape)

x_train = x_train.reshape(-1, 28, 28, 1)
x_test = x_test.reshape(-1, 28, 28, 1)

x_train, x_val, y_train, y_val = train_test_split(x_train, 
                                                  y_train, 
                                                  test_size= 0.1, 
                                                  random_state=88)

model = Sequential()

model.add(layers.Conv2D(filters=32, kernel_size=(5,5), padding='same', activation='relu', input_shape=(28, 28, 1)))
model.add(layers.MaxPool2D(strides=2))
model.add(layers.Conv2D(filters=48, kernel_size=(5,5), padding='valid', activation='relu'))
model.add(layers.MaxPool2D(strides=2))
model.add(layers.Flatten())
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dense(84, activation='relu'))
model.add(layers.Dense(number_of_classes, activation='softmax'))

model.summary()

optimizer_name = 'adam'

model.compile(loss='categorical_crossentropy', optimizer=optimizer_name, metrics=['accuracy'])

early_stopping = EarlyStopping(monitor='val_loss', patience=5, verbose=1, mode='min')
mcp_save = ModelCheckpoint('emnist_model.h5', save_best_only=True, monitor='val_loss', verbose=1, mode='auto')

history = model.fit(x_train,
                    y_train, 
                    epochs=30, 
                    batch_size=32, 
                    verbose=1, 
                    validation_split=0.1,
                    callbacks=[early_stopping, mcp_save])

model = load_model('emnist_model.h5')
model.summary()