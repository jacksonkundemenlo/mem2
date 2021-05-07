# code based off of https://machinelearningmastery.com/text-generation-lstm-recurrent-neural-networks-python-keras/

import string

def clean_caption(caption):
# add leading zeros if too short
# remove excess bars
# remove punctuation
    # if len(caption)<90:
    #     caption = (90-len(caption)) * 'ඞ' + caption
    caption = caption.translate(str.maketrans('', '', string.punctuation.replace('|', '')))
    if '||' in caption:
        caption = caption.replace('||', ' ')
    if caption[-1] == '|':
        caption = caption[:-1]
    if '|' in caption:
        caption = caption.replace('|', ' | ')
    caption = caption.lower()
    return caption

import pandas as pd
import csv
import sys

import numpy
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils

# data = ' '.join(pd.read_csv('train_gena_24_4000.csv')['1'][:1600])
# data = data.lower()

datadf = pd.read_csv('train_gena_24_4000.csv')
datadf['lenth_caption'] = datadf['1'].apply(len)
datadf['clean_caption'] = datadf['1'].apply(clean_caption)

datadf = datadf[datadf['0'] == 155067746]
# datadf = datadf[datadf['0'] == 222403160]
data = ' '.join(datadf['clean_caption'])
data = data.split()
# print(data)

# pd.set_option('display.max_colwidth', -1)
# print(datadf)
# print(datadf.describe())


# create mapping of unique chars to integers
# chars = sorted(list(set(data)))
# char_to_int = dict((c, i) for i, c in enumerate(chars))

# creat mapping of unique words to integers
words = sorted(list(set(data)))
char_to_int = dict((c, i) for i, c in enumerate(words))

char_to_int[' '] = len(char_to_int)
# print(char_to_int)



# print(char_to_int)
# print(chars)

n_words = len(data)
n_vocab = len(words)
print ("Total Words: ", n_words)
print ("Total Vocab: ", n_vocab)

# n_chars = len(data)
# n_vocab = len(chars)
# print ("Total Characters: ", n_chars)
# print ("Total Vocab: ", n_vocab)
# print(char_to_int)


# prepare the dataset of input to output pairs encoded as integers
seq_length = 20
dataX = []
dataY = []
for i in range(0, n_words - seq_length, 1):
    seq_in = data[i:i + seq_length]
    seq_out = data[i + seq_length]
    dataX.append([char_to_int[word] for word in seq_in])
    dataY.append(char_to_int[seq_out])
n_patterns = len(dataX)
# print ("Total Patterns: ", n_patterns)

# reshape X to be [samples, time steps, features]
X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
# normalize
X = X / float(n_vocab)
# one hot encode the output variable
y = np_utils.to_categorical(dataY)



# define the LSTM model
model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(256))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

# define the checkpoint
filepath= "weights-improvement-{epoch:02d}-{loss:.4f}--1layerclean.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min', period = 10)
callbacks_list = [checkpoint]

# continue earlier training
# model = load_model("weights-improvement-250-0.9334--1layerclean.hdf5")


# model.fit(X, y, epochs=1000, batch_size=128, callbacks=callbacks_list)



# load the network weights
filename = "weights-improvement-260-0.4991--1layerclean.hdf5"
model.load_weights(filename)
model.compile(loss='categorical_crossentropy', optimizer='adam')

# reverse dict to decode
int_to_char = dict((i, c) for i, c in enumerate(words))

# pick a random seed

# print("input: ")
# start = input()
# start = start.lower()
# pattern = []
# pattern.append([char_to_int[word] for word in start])
# pick a random seed

start = numpy.random.randint(0, len(dataX)-1)
pattern = dataX[start]
print ("Seed:")
print (''.join([int_to_char[value] for value in pattern]))
print('\nNew meme alert:')
# generate characters
for i in range(25):
	x = numpy.reshape(pattern, (1, len(pattern), 1))
	x = x / float(n_vocab)
	prediction = model.predict(x, verbose=0)
	index = numpy.argmax(prediction)
	result = int_to_char[index]
	seq_in = [int_to_char[value] for value in pattern]
	sys.stdout.write(result + ' ')
	pattern.append(index)
	pattern = pattern[1:len(pattern)]
print ("\nDone.")