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
from sklearn.model_selection import train_test_split, StratifiedKFold


download("punkt")
download("wordnet")

IGNORE = ["!", "?", ".", ","]


class Model:
    """Saves trained model and words list.

    1) Load queries from data file.
    2) Process words in each query and store those with their respective category.
    3) Convert processed words and categories into numerical arrays.
    4) Train the neural network model using the arrays.

    Also has two methods for evaluating the trained model.
    """

    def __init__(self):
        self.all_words = set()
        self.processed_data = []
        self.training_data = []
        self.model = None
        self.category_data = None
        self.X = None
        self.y = None

    def load_process_data(self):
        """Loads and processes the data."""

        with open("data/query_data.json", encoding="utf-8") as data_file:
            self.category_data = json.loads(data_file.read())["categories"]
        lem = WordNetLemmatizer()

        for i, category in enumerate(self.category_data[:-1]):
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
        with open("data/words.pkl", "wb") as words_file:
            pickle.dump(self.all_words, words_file)

        # Converts input to numerical arrays for the neural network.
        for item in self.processed_data:
            query_words, cat_num = item

            # For query words, use bag-of-words model (en.wikipedia.org/wiki/Bag-of-words_model).
            # Use 1 to indicate a word is present in the query and 0 if not (assume word only
            # appears once in each query).
            bag = [1 if word in query_words else 0 for word in self.all_words]

            # For categories/labels, use array of 0s with correct category indicated by a 1.
            output_row = [0] * (len(self.category_data) - 1)
            output_row[cat_num] = 1

            # Stores bag-of-words array alongside output array.
            self.training_data.append([bag, output_row])

        # Shuffles the training data and splits it into input (X) and labels (y).
        shuffle(self.training_data)
        self.training_data = np.array(self.training_data, dtype=object)
        self.X = np.array(list(self.training_data[:, 0]))
        self.y = np.array(list(self.training_data[:, 1]))

    def build_model(self, verbose=True):
        """Builds the neural network model, prints a
        summary if verbose is True, and returns the model.
        """

        # Only loads and processes the data if it hasn't been done
        # yet (makes repeated calls to this method more efficient).
        if isinstance(self.training_data, list):
            self.load_process_data()

        # Neural network (NN) with dropouts to avoid overfitting.
        model = Sequential()
        model.add(Dense(128, input_shape=(self.X.shape[1],), activation="relu"))
        model.add(Dropout(0.2))
        model.add(Dense(64, activation="relu"))
        model.add(Dropout(0.2))

        # Output layer has the same number of nodes as labels.
        model.add(Dense(self.y.shape[1], activation="softmax"))

        # Sets the hyperparameters for the NN (optimizer).
        sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)

        # Compiles NN with loss and metrics calculations.
        model.compile(
            loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"]
        )

        self.model = model

        if verbose:
            print(model.summary())

        return model

    def train_model(self, epochs=20):
        """Trains the neural network with given data and
        hyperparameters and saves the trained model to file.
        """

        self.build_model()

        # Trains the model with our input arrays and label arrays.
        trained_model = self.model.fit(
            self.X,
            self.y,
            epochs=epochs,
            batch_size=5,
            verbose=1,
        )

        # Saves the model to a file for use in bot.py.
        self.model.save("data/trained_model.h5", trained_model)

    def evaluate_ttsplit(self, num_epochs):
        """Gets the loss and accuracy for the model, depending on the number of epochs
        specified, using a simple split of the data into training and testing parts.

        Args:
            num_epochs (int): The number of epochs to train the model for before testing.

        Returns:
            Values for loss and accuracy (tuple of 2 floats).
        """

        model = self.build_model(verbose=False)

        X_train, X_test, y_train, y_test = train_test_split(
            self.X,
            self.y,
            test_size=0.25,
            stratify=self.y
        )
        model.fit(X_train, y_train, epochs=num_epochs, batch_size=5, verbose=0)

        return model.evaluate(X_test, y_test, verbose=0)

    def evaluate_kfold(self, num_epochs):
        """Gets the loss and accuracy for the model, depending on the number of epochs
        specified, using a more advanced testing method called stratified k-fold (better
        for smaller data sets).

        Args:
            num_epochs (int): The number of epochs to train the model for before testing.

        Returns:
            Values for loss and accuracy (tuple of 2 floats).
        """

        skf = StratifiedKFold(n_splits=8, shuffle=True, random_state=1)

        model = self.build_model(verbose=False)

        loss_scores = []
        accuracy_scores = []
        for train, test in skf.split(self.X, self.y.argmax(1)):
            model.fit(
                self.X[train],
                self.y[train],
                epochs=num_epochs,
                batch_size=5,
                verbose=0
            )
            loss, acc = model.evaluate(self.X[test], self.y[test], verbose=0)
            loss_scores.append(loss)
            accuracy_scores.append(acc)

        return np.mean(loss_scores), np.mean(accuracy_scores)
