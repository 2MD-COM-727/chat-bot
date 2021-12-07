"""Trains the ChatBot model with given json.

Requires the follwing packages: json, pickle, random, numpy, nltk, and tensorflow.
"""

# pylint: disable=no-name-in-module

import json
import pickle
from random import shuffle
import numpy as np
from nltk import word_tokenize, download
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

download("punkt")
download("wordnet")

IGNORE = ["!", "?", ".", ","]


class Model:
    """Saves trained model and words list.

    1) Load queries from data file.
    2) Process words in each query and store those with their respective category.
    3) Convert processed words and categories into numerical arrays.
    4) Train the neural network model.
    """

    def __init__(self):
        self.all_words = set()
        self.processed_data = []
        self.training = []
        self.model = None

        self.load_process_data()

    def load_process_data(self):
        """Loads and processes the data."""

        with open("chat_bot/data/data.json", encoding="utf-8") as data_file:
            self.category_data = json.loads(data_file.read())["categories"]
        lem = WordNetLemmatizer()

        for i, category in enumerate(self.category_data):
            for question in category["questions"]:

                # Splits up the question into words
                # Converts words into stems and ignores punctuation.
                words = [
                    lem.lemmatize(word)
                    for word in word_tokenize(question)
                    if word not in IGNORE
                ]

                # Stores processed words along with its category number.
                self.processed_data.append([words, i])

                # Updates the master word list.
                self.all_words.update(words)

        # Fixes the order of the master word list and saves it to a file.
        self.all_words = list(self.all_words)
        with open("chat_bot/data/words.pkl", "wb") as words_file:
            pickle.dump(self.all_words, words_file)

        # Converts input to numerical arrays for the neural network.
        for item in self.processed_data:
            query_words, cat_num = item

            # For query words, use bag-of-words model (en.wikipedia.org/wiki/Bag-of-words_model).
            # Use 1 to indicate a word is present in the query and 0 if not (assume word only
            # appears once in each query).
            bag = [1 if word in query_words else 0 for word in self.all_words]

            # For categories/labels, use array of 0s with correct category indicated by a 1.
            output_row = [0] * len(self.category_data)
            output_row[cat_num] = 1

            # Stores bag-of-words array alongside output array.
            self.training.append([bag, output_row])

        # Shuffles the training data and splits it into input (x) and output (y).
        shuffle(self.training)
        self.training = np.array(self.training)
        self.train_x = list(self.training[:, 0])
        self.train_y = list(self.training[:, 1])

    def build_model(self):
        """Builds the neural network model and prints a summary."""

        # Neural network (NN) with dropouts to avoid overfitting.
        model = Sequential()
        model.add(Dense(128, input_shape=(len(self.train_x[0]),), activation="relu"))
        model.add(Dropout(0.2))
        model.add(Dense(64, activation="relu"))
        model.add(Dropout(0.2))

        # Output layer has a vector shape and the same number of nodes as with labels.
        model.add(Dense(len(self.train_y[0]), activation="softmax"))

        self.model = model
        print(model.summary())

    def train_model(self):
        """Trains the neural network with given data and hyperparameters."""

        self.build_model()

        # Sets the hyperparameters for the NN (optimizer).
        sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)

        # Compiles NN with loss and metrics calculations.
        self.model.compile(
            loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"]
        )

        # Trains and saves the model
        trained_model = self.model.fit(
            np.array(self.train_x),
            np.array(self.train_y),
            epochs=30,
            batch_size=5,
            verbose=1,
        )
        self.model.save("chat_bot/data/trained_model.h5", trained_model)
