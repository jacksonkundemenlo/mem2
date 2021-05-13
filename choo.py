import pandas as pd
import csv
import sys
import string
import numpy
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
import random

def clean_caption(caption):
# add leading zeros if too short
# remove excess bars
# remove punctuation
    # if len(caption)<90:
    #     caption = (90-len(caption)) * 'ඞ' + caption
    caption = str(caption)
    caption = caption.translate(str.maketrans('', '', string.punctuation.replace(';', '')))
    # if '||' in caption:
    #     caption = caption.replace('||', ' ')
    # if caption[-1] == '|':
    #     caption = caption[:-1]
    # if '|' in caption:
    #     caption = caption.replace('|', ' | ')
    caption = caption.lower()
    for char in caption:
        if char not in 'qwertyuiopasdfghjkl;zxcvbnm1234567890 ':
            caption = '0'
    return caption

# datadf = pd.read_csv('train_gena_24_4000.csv')
# datadf['clean_caption'] = datadf['1'].apply(clean_caption)

datadf = pd.read_csv('cap.csv')
datadf['caption'] = datadf['caption'].apply(clean_caption)
datadf = datadf[datadf['caption'] != '0']
# print(string.punctuation)

# print(datadf)


def train_caption(meme_name, meme_ID, epochs, datadf=datadf, continue_model=None):
    # read in and clean csv for use
    datadf = datadf[datadf['type'] == meme_ID]
    data = ' '.join(datadf['caption'])
    data = data.split()

    # create mapping of unique words to integers
    chars = sorted(list(set(data)))
    char_to_int = dict((c, i) for i, c in enumerate(chars))

    # creat mapping of unique words to integers
    words = sorted(list(set(data)))
    char_to_int = dict((c, i) for i, c in enumerate(words))
    char_to_int[' '] = len(char_to_int) # add spaces to dict

    n_words = len(data)
    n_vocab = len(words)
    print ("Total Words: ", n_words)
    print ("Total Vocab: ", n_vocab)


    # prepare the dataset of input to output pairs encoded as integers
    seq_length = 12
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
    filepath = meme_name + "/weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
    # /Users/jacksonkunde/Desktop/Senior_CS/mem2/surprised_pika/weights-improvement-610-0.2669--1layerclean.hdf5 
    checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min', period = 10)
    callbacks_list = [checkpoint]

    # continue earlier training
    if continue_model != None:
        model = load_model(continue_model)

    model.fit(X, y, epochs=epochs, batch_size=128, callbacks=callbacks_list)

def generate_caption(meme_name, meme_ID, meme_weights_file, datadf=datadf, length_gen=12):

    # read in and clean csv for use
    datadf = datadf[datadf['0'] == meme_ID]
    data = ' '.join(datadf['clean_caption'])
    data = data.split()

    # create mapping of unique words to integers
    chars = sorted(list(set(data)))
    char_to_int = dict((c, i) for i, c in enumerate(chars))

    # creat mapping of unique words to integers
    words = sorted(list(set(data)))
    char_to_int = dict((c, i) for i, c in enumerate(words))
    char_to_int[' '] = len(char_to_int) # add spaces to dict

    # load the network weights
    model = load_model(meme_weights_file)

    # reverse dict to decode
    int_to_char = dict((i, c) for i, c in enumerate(words))

    # pick random meme from dataset to generate new meme
    start = random.randint(0,len(datadf))
    input_s = datadf['clean_caption'].iloc[start]

    # input_s = "students acting crazy | teacher pay attention | that kid named attention"
    # input_seed = input_s.split()

    start = random.randint(0,len(datadf))
    input_s = datadf['clean_caption'].iloc[start]
    input_seed = input_s.split()


    while len(input_seed) < length_gen:
        start = random.randint(0,len(datadf))
        input_s = datadf['clean_caption'].iloc[start]
        input_seed = input_s.split()

    input_list = []
    input_list.append([char_to_int[input_s] for input_s in input_seed])

    pattern = input_list[0]

    print ("Seed:")
    print(input_s)

    print('\nNew meme alert:')

    n_vocab = len(words)

    # generate characters
    for i in range(len(pattern)):
        x = numpy.reshape(pattern, (1, len(pattern), 1))
        x = x / float(n_vocab)
        prediction = model.predict(x, verbose=0)
        index = numpy.argmax(prediction)
        result = int_to_char[index]
        # seq_in = [int_to_char[value] for value in pattern]
        sys.stdout.write(result + ' ')
        pattern.append(index)
        pattern = pattern[1:len(pattern)]
    print ("\nDone.")

train_caption("Surprised-Pikachu", "Surprised-Pikachu", 200)

# not over fit
# generate_caption("surprised_pika", 155067746, "surprised_pika/weights-improvement-90-1.8385.hdf5")
# generate_caption("surprised_pika", 155067746, "surprised_pika/weights-improvement-100-1.6474.hdf5")
