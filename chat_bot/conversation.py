"""Simple TUI chatbot conversation with user.
"""

from training import train


chatbot = train("..//training-data")

print("BOT: Welcome!")

HUMAN = False
while True:
    print("BOT: How can I help?")
    query = input("YOU: ")
    print(f"BOT: {chatbot.get_response(query)}")
    print("BOT: Was this answer helpful?")
    response = input("YOU: ")
    if response == "no":  # and all other possibilities for no
        print("BOT: Sorry! Would you like to speak to a human?")
        response = input("YOU: ")
        if response == "yes":  # and all other possibilities for yes
            HUMAN = True
            break
    print("BOT: Do you have any other questions?")
    response = input("YOU: ")
    if response == "no":  # and all other possibilities for no
        break

if HUMAN:
    print("BOT: You will be connected to a human now.")

print("BOT: Goodbye.")
