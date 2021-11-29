"""Gets answers to a few test queries from chatbot.
"""

from training import train


chatbot = train("..//training-data")

test_queries = [
    "When does the library open?",
    "What applications are on the computers?",
    "I want to book a computer",
    "Can I book a study room?",
    "What ebooks are avialable?",
    "Where can I find this book?",
    "I need to borrow a laptop",
]

for query in test_queries:
    print("\nUSER:", query)
    print("BOT:", chatbot.get_response(query))
