from time import sleep
from gui import ChatGUI


gui = ChatGUI()

n = 0
while n < 5:

    gui.window.update()
    gui.insert_user_message("This is a user message")
    sleep(1)

    gui.window.update()
    gui.insert_bot_message("This is a bot message")
    sleep(1)

    n += 1
