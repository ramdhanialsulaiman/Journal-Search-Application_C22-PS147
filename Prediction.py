import csv
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

model = tf.keras.models.model_load('my_model.h5')

vocab_size = 10000
embedding_dim = 64
max_length = 200
trunc_type = 'post'
padding_type = 'post'
oov_tok = '<OOV>'
TRAINING_SPLIT = .8

import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords
import re
STOPWORDS = set(stopwords.words('english'))

print(tf.__version__)


def cleaning_stopwords(title):
  title = title.lower()
  for word in STOPWORDS:
    token = ' ' + word + ' '
    Title = title.replace(token, ' ')
    title = title.replace(' ', ' ')
    title = re.sub(r'[^\w\s]', '', title)
  return title

def seq_pad_and_trunc(titles, padding, truncating, maxlen):
    tokenizer = Tokenizer(num_words=vocab_size, oov_token='<OOV>')
    tokenizer.fit_on_texts(titles)
    titles = tokenizer.texts_to_sequences(titles)
    pad_trunc_sequences = pad_sequences(titles, maxlen=maxlen, truncating=truncating,padding=padding)
    return pad_trunc_sequences

model = tf.keras.models.load_model('/content/my_model.h5')

def predict(title, padding_type, trunc_type, max_length):
  class_names = ['teknik','kesehatan','ekonomi','hukum']
  clean_words = cleaning_stopwords(title)
  try_seq = seq_pad_and_trunc(clean_words, padding_type, trunc_type, max_length)
  prediction = model.predict(try_seq)
  index = prediction[0].argmax()
  label = class_names[index]
  return label