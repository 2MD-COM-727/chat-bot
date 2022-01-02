"""Creates and runs the Library ChatBot.

Requires 'ChatGUI' from 'gui'
"""

from argparse import ArgumentParser
from gui import ChatGUI
from model import Model

# pylint: disable=anomalous-backslash-in-string
ASCII_TITLE = """
______________________________________________________________
  ____  __  __ ____     ____ _           _   ____        _   
 |___ \|  \/  |  _ \   / ___| |__   __ _| |_| __ )  ___ | |_ 
   __) | |\/| | | | | | |   | '_ \ / _` | __|  _ \ / _ \| __|
  / __/| |  | | |_| | | |___| | | | (_| | |_| |_) | (_) | |_ 
 |_____|_|  |_|____/   \____|_| |_|\__,_|\__|____/ \___/ \__|
______________________________________________________________

"""
# pylint: enable=anomalous-backslash-in-string

ADMIN_MENU = """
1. Build model and show summary
2. Train and save model
3. Display evaluation graphs of epochs against loss and accuracy

"""


def args_setup():
    """Sets up CLI arguments to manipulate package"""

    parser = ArgumentParser()
    parser.add_argument("--admin", dest="admin", action="store_true")
    parser.set_defaults(admin=False)

    return parser.parse_args()


def get_admin_option():
    """Asks the user for an input for admin options.

    Returns:
        str: The option selected.
    """

    return_option = None
    while return_option is None:
        opt = input(f"{ADMIN_MENU}>>> ")
        if opt in ("1", "2", "3"):
            return_option = opt
        else:
            print("\nPlease select a valid option.")
    return return_option


if __name__ == "__main__":
    print(ASCII_TITLE)
    print("Initializing ChatBot...\n")

    args = args_setup()
    model = Model()

    if args.admin:
        option = get_admin_option()
        if option == "1":
            print(model.build_model().summary())
        elif option == "2":
            model.train_model()
        elif option == "3":
            model.evaluate()
    else:
        app = ChatGUI()
        app.run()
