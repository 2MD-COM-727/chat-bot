"""Trains the chatbot model with given json and saves trained model and word list to file.
Also has two functions for model evaluation that use different methods.

Requires the follwing packages: json, pickle, random, numpy, nltk, tensorflow and sklearn.
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
from sklearn.model_selection import train_test_split, StratifiedKFold


# pylint: disable=too-many-locals
def prepare_data():
    """Loads queries from data file, processes words in each query
    and converts processed words and categories into numerical arrays.

    Returns:
        (list): Input arrays paired with their corresponding label array.
    """

    IGNORE = ["!", "?", ".", ","]

    with open("./data/data.json", encoding="utf-8") as data_file:
        category_data = json.load(data_file)["categories"]
    lem = WordNetLemmatizer()

    all_words = set()
    processed_data = []
    for i, category in enumerate(category_data[:-1]):
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
    with open("./data/words.pkl", "wb") as words_file:
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
        output_row = [0] * (len(category_data) - 1)
        output_row[cat_num] = 1

        # Stores bag-of-words array alongside output array.
        training.append([bag, output_row])

    return training


def build_model(X_size, y_size):
    """Sets type of model, adds layers, sets hyperparameters and compiles model.

    Args:
        X_size (int): The length of an input array.
        y_size (int): The length of an output array.

    Returns:
        (TensorFlow object): The compiled model ready for training.
    """

    # Neural network (NN) with dropouts to avoid overfitting.
    model = Sequential()
    model.add(Dense(128, input_shape=(X_size,), activation="relu"))
    model.add(Dropout(0.2))
    model.add(Dense(64, activation="relu"))
    model.add(Dropout(0.2))

    # Output layer has the same number of nodes as labels.
    model.add(Dense(y_size, activation="softmax"))

    # Sets the hyperparameters for the NN (optimizer).
    sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)

    # Compiles NN with loss and metrics calculations.
    model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

    return model


def train_and_save_model(training):
    """Arranges the training data for the model and uses it to train the model,
    then saves the trained model to a file for use by the chatbot module.

        Args:
            training (list): The training data returned by prepare_data().
    """

    # Shuffles the training data and splits it into input (x) and output (y).
    shuffle(training)
    training = np.array(training, dtype=object)
    X_train = list(training[:, 0])
    y_train = list(training[:, 1])

    model = build_model(len(X_train[0]), len(y_train[0]))

    # Trains and saves the model
    trained_model = model.fit(
        np.array(X_train), np.array(y_train), epochs=12, batch_size=5, verbose=1
    )
    model.save("./data/chatbot_model.h5", trained_model)


def evaluate_ttsplit(training, num_epochs):
    """Gets the loss and accuracy for the model, depending on the number of epochs
    specified, using a simple split of the data into training and testing parts.

    Args:
        training (list): The training data returned by prepare_data().
        num_epochs (int): The number of epochs to train the model for before testing.

    Returns:
        (tuple of 2 floats): Values for loss and accuracy.
    """

    training = np.array(training, dtype=object)
    X = np.array([np.array(x) for x in training[:, 0]])
    y = np.array([np.array(x) for x in training[:, 1]])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

    model = build_model(len(X[0]), len(y[0]))
    model.fit(X_train, y_train, epochs=num_epochs, batch_size=5, verbose=0)

    return model.evaluate(X_test, y_test, verbose=0)


def evaluate_kfold(training, num_epochs):
    """Gets the loss and accuracy for the model, depending on the number of epochs
    specified, using a more advanced testing method called stratified k-fold (better
    for smaller data sets).

    Args:
        training (list): The training data returned by prepare_data().
        num_epochs (int): The number of epochs to train the model for before testing.

    Returns:
        (tuple of 2 floats): Values for loss and accuracy.
    """

    training = np.array(training, dtype=object)
    X = np.array([np.array(x) for x in training[:, 0]])
    y = np.array([np.array(x) for x in training[:, 1]])

    skf = StratifiedKFold(n_splits=6, shuffle=True, random_state=1)

    model = build_model(len(X[0]), len(y[0]))

    loss_scores = []
    accuracy_scores = []
    for train, test in skf.split(X, y.argmax(1)):
        model.fit(X[train], y[train], epochs=num_epochs, batch_size=5, verbose=0)
        loss, acc = model.evaluate(X[test], y[test], verbose=0)
        loss_scores.append(loss)
        accuracy_scores.append(acc)

    return np.mean(loss_scores), np.mean(accuracy_scores)


# Testing new evaluation functions - remove before merge
prepared_data = prepare_data()

print("Evaluating model with train/test split method")
for i in range(1, 21):
    loss, acc = evaluate_ttsplit(prepared_data, i)
    print(f"{i}\tLoss: {loss:.2f}\tAccuracy: {acc:.1%}")

print("\nEvaluating model with K-fold method")
for i in range(1, 21):
    loss, acc = evaluate_kfold(prepared_data, i)
    print(f"{i}\tLoss: {loss:.2f}\tAccuracy: {acc:.1%}")
