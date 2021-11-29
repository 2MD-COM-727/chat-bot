"""Trains chatbot based on data.
"""

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


def train(directory):
    """Takes data directory and returns trained chatbot.
    """

    query_types = [
        "borrowing_laptop",
        "computer_booking",
        "ebooks",
        "location_of_books",
        "printing",
        "study_room",
    ]

    training_lines = []
    for query_type in query_types:
        with open(f"{directory}//{query_type}_questions.txt", encoding="UTF-8") as file_q:
            with open(f"{directory}//{query_type}_answer.txt", encoding="UTF-8") as file_a:
                answer = file_a.read()
                for question in file_q.read().splitlines():
                    training_lines.append(question)
                    training_lines.append(answer)

    chatbot = ChatBot("Charlie")
    trainer = ListTrainer(
        chatbot,
        logic_adapters=[
            {
                "import_path": "chatterbot.logic.BestMatch",
                "default_response": "I am sorry, but I do not understand.",
                "maximum_similarity_threshold": 0.7,
            }
        ],
    )
    trainer.train(training_lines)

    return chatbot
