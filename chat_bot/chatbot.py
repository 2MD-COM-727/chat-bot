"""Contains the ChatBot functionality.

Requires the following modules: json, pickle, numpy, nltk, and tensorflow.
"""

import json
import pickle
import numpy as np
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model


class ChatBot:
    """A ChatBot to interface with GUI and Model.

    Generates a predicted response based on query using a trained model.
    """

    def __init__(self, threshold=0.75):

        # Loads data saved during training with model.py.
        with open("../chat_bot/data/data.json", encoding="utf-8") as data_file:
            self.data = json.loads(data_file.read())["categories"]
        with open("./data/words.pkl", "rb") as words_file:
            self.all_words = pickle.load(words_file)
        self.model = load_model("./data/chatbot_model.h5")

        # Sets confidence threshold below which a default response will be returned.
        self.threshold = threshold

    def bag_of_words(self, query):
        """Converts user query into an array that the model can use as input.

        Args:
            query (str): Raw query from user.

        Returns:
            numpy array: Array of 1s and 0s generated according to the bag-of-words
                         model (en.wikipedia.org/wiki/Bag-of-words_model), making the
                         assumption that the query contains only one of each word.
        """

        # Splits up the query into words and converts words into stems.
        lem = WordNetLemmatizer()
        query_words = [lem.lemmatize(word) for word in word_tokenize(query)]

        # Use 1 to indicate a word is present in the query and 0 if not.
        bag = [1 if word in query_words else 0 for word in self.all_words]

        return np.array([bag])

    def get_response(self, query):
        """Predicts which category/label the query falls into.
        If confidence is lower than the threshold it will return a default response.

        Args:
            query (str): The query to get the a predicted response from.

        Returns:
            str: The response that corresponds with the predicted category.
        """

        # Converts query to numpy array that model can use for prediction.
        bow = self.bag_of_words(query)

        # Gets model's prediction of likelihood of each category.
        prediction = self.model.predict(bow)[0]

        # Finds most likely catgory and gets its category number and confidence.
        cat_num, confidence = max(enumerate(prediction), key=lambda x: x[1])

        print(confidence)  # for testing purposes (remove later)

        # Assigns last (default) category in json file if confidence is below threshold.
        if confidence < self.threshold:
            cat_num = -1

        # Returns response from json data file according to category number.
        return self.data[cat_num]["response"]
