"""Trains chatbot based on data in json file.
"""

import json
import pickle
import numpy as np
from random import shuffle
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD


IGNORE = ["!", "?", ".", ","]
category_data = json.loads(open("../model-training/data.json").read())["categories"]
lem = WordNetLemmatizer()

all_words = set()
processed_data = []
for i, category in enumerate(category_data):
    for question in category["questions"]:
        # Split up question into words, convert words into stems and ignore punctuation
        words = [lem.lemmatize(word) for word in word_tokenize(question) if word not in IGNORE]
        # Store processed words alongside their category number
        processed_data.append([words, i])
        # Update master word list
        all_words.update(words)

# Fix order of master word list and save to file
all_words = list(all_words)
pickle.dump(all_words, open("../model-training/words.pkl", "wb"))

# Converting input to numerical arrays for neural network
training = []
for item in processed_data:
    query_words, cat_num = item
    # For query words, use bag-of-words model
    # Use 1 to indicate a word is present and a 0 if not
    bag = [1 if word in query_words else 0 for word in all_words]
    # For output category, use array of 0s with correct category indicated by a 1
    output_row = [0] * len(category_data)
    output_row[cat_num] = 1
    # Store bag-of-words array alongside output array
    training.append([bag, output_row])

# Shuffle training data and split it into input (x) and output (y)
shuffle(training)
training = np.array(training)
train_x = list(training[:, 0])  # (numpy notation)
train_y = list(training[:, 1])

# Build neural network by adding layers
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation="relu"))
model.add(Dropout(0.2))  # (dropout layers prevent overfitting)
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.2))
# For the output layer, we want the same number of nodes as categories
model.add(Dense(len(train_y[0]), activation="softmax"))

# Compile neural network with appropriate parameters
sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

# Train the model with our data and save it to a file
trained_model = model.fit(np.array(train_x), np.array(train_y), epochs=30, batch_size=5, verbose=1)
model.save("../model-training/chatbot_model.h5", trained_model)
