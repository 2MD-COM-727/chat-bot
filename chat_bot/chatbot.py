import json
import pickle
import numpy as np
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model


class ChatBot:

    def __init__(self, threshold=0.75):
        self.data = json.loads(open("../model-training/data.json").read())["categories"]
        self.all_words = pickle.load(open("../model-training/words.pkl", "rb"))
        self.model = load_model("../model-training/chatbot_model.h5")
        self.THRESHOLD = threshold

    def _bag_of_words(self, query):
        lem = WordNetLemmatizer()
        query_words = [lem.lemmatize(word) for word in word_tokenize(query)]
        bag = [1 if word in query_words else 0 for word in self.all_words]
        return np.array([bag])

    def get_response(self, query):
        bow = self._bag_of_words(query)
        prediction = self.model.predict(bow)[0]
        cat_num, confidence = max(enumerate(prediction), key=lambda x: x[1])
        print(confidence)  # for testing purposes
        if confidence < self.THRESHOLD:
            cat_num = -1
        return self.data[cat_num]["response"]
