from time import sleep
from gui import ChatGUI


gui = ChatGUI()

while True:
    gui.window.update()
    gui.insert_user_message("This is a user message")
    sleep(1)
    gui.window.update()
    gui.insert_bot_message("This is a bot message")
    sleep(1)
