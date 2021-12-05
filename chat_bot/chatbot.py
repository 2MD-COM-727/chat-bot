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
        with open("./data/data.json", encoding="utf-8") as data_file:
            self.data = json.loads(data_file.read())["categories"]

        with open("./data/words.pkl", "rb") as words_file:
            self.all_words = pickle.load(words_file)
        self.model = load_model("./data/chatbot_model.h5")
        self.threshold = threshold

    def bag_of_words(self, query):
        """[summary]

        Args:
            query ([type]): [description]

        Returns:
            [type]: [description]
        """

        lem = WordNetLemmatizer()
        query_words = [lem.lemmatize(word) for word in word_tokenize(query)]
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

        bow = self.bag_of_words(query)
        prediction = self.model.predict(bow)[0]
        cat_num, confidence = max(enumerate(prediction), key=lambda x: x[1])

        print(confidence)  # for testing purposes

        if confidence < self.threshold:
            cat_num = -1
        return self.data[cat_num]["response"]
