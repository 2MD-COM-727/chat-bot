"""Trains the ChatBot model with given json.

Requires the follwing packages: json, pickle, random, numpy, nltk, and tensorflow.
"""

import json
import pickle
from random import shuffle
import numpy as np
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD


IGNORE = ["!", "?", ".", ","]


def train_model():
    """Saves trained model and word list to files for use in chatbot.py.

    Process: 1) Load queries from data file.
             2) Process words in each query and store those with their respective category.
             3) Convert processed words and categories into numerical arrays.
             4) Use arrays to train neural network model.
    """

    with open("./data/data.json", encoding="utf-8") as data_file:
        category_data = json.loads(data_file.read())["categories"]
    lem = WordNetLemmatizer()

    all_words = set()
    processed_data = []
    for i, category in enumerate(category_data):
        for question in category["questions"]:

            # Splits up the question into words, converts words into stems and ignores punctuation.
            words = [
                lem.lemmatize(word)
                for word in word_tokenize(question)
                if word not in IGNORE
            ]

            # Stores processed words along with its category number.
            processed_data.append([words, i])

            # Updates the master word list.
            all_words.update(words)

    # Fixes the order of the master word list and saves it to a file.
    all_words = list(all_words)
    with open("./data/words.pkl", "wb", encoding="utf-8") as words_file:
        pickle.dump(all_words, words_file)

    # Converts input to numerical arrays for the neural network.
    training = []
    for item in processed_data:
        query_words, cat_num = item

        # For query words, use bag-of-words model (en.wikipedia.org/wiki/Bag-of-words_model).
        # Use 1 to indicate a word is present in the query and 0 if not (assume word only
        # appears once in each query).
        bag = [1 if word in query_words else 0 for word in all_words]

        # For categories/labels, use array of 0s with correct category indicated by a 1.
        output_row = [0] * len(category_data)
        output_row[cat_num] = 1

        # Stores bag-of-words array alongside output array.
        training.append([bag, output_row])

    # Shuffles the training data and splits it into input (x) and output (y).
    shuffle(training)
    training = np.array(training)
    train_x = list(training[:, 0])
    train_y = list(training[:, 1])

    # Neural network (NN) with dropouts to avoid overfitting.
    model = Sequential()
    model.add(Dense(128, input_shape=(len(train_x[0]),), activation="relu"))
    model.add(Dropout(0.2))
    model.add(Dense(64, activation="relu"))
    model.add(Dropout(0.2))

    # Output layer has a vector shape and the same number of nodes as with labels.
    model.add(Dense(len(train_y[0]), activation="softmax"))

    # Sets the hyperparameters for the NN (optimizer).
    sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)

    # Compiles NN with loss and metrics calculations.
    model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

    # Trains and saves the model
    trained_model = model.fit(
        np.array(train_x), np.array(train_y), epochs=30, batch_size=5, verbose=1
    )
    model.save("./data/chatbot_model.h5", trained_model)

