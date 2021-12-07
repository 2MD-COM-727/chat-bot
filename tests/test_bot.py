"""Gets answers from the chatbot for a few test queries.
"""

from chat_bot.chatbot import ChatBot


test_queries = [
    # Easy questions
    "When does the library open?",
    "What software is on the computers?",
    "I want to book a computer",
    "Can I book a study room?",
    "What ebooks are available?",
    "How much does printing cost?",
    "Where can I find this book?",
    "I need to borrow a laptop.",
    "How do I get into the library?",
    # Non-categorisable questions
    "I lost a book in the library.",  # avoid categorising as location of books
    "Can I charge my laptop in the library?",  # avoid categorising as borrowing laptops
    # Hard-to-categorise questions
    "Where can I find a book about printing?",  # avoid categorising as printing
    "Are there any ebooks about software?",  # avoid categorising as software
]

cb = ChatBot()
for query in test_queries:
    print("\nUSER:", query)
    print("BOT:", cb.get_response(query))
