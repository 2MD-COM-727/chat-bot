"""Creates a graphical user interface (GUI) for the chat bot.

Requires 'tkinter' (tk) and can be imported as a class module.

    Typical usage example:
        app = ChatGUI
        app.run()
"""

# pylint: disable=super-init-not-called, too-few-public-methods, too-many-instance-attributes

from dataclasses import dataclass
from tkinter import Tk, Label, Text, Entry, Button, WORD, DISABLED, NORMAL, END
import tkinter.scrolledtext as ScrolledText
from webbrowser import open as web_open

from bot import ChatBot
from catalogue import find_item, MENU, OPTIONS_MAP_LABEL


@dataclass
class ChatWindow:
    """Class constants for the GUI window."""

    WINDOW_TITLE = "Solent Library's ChatBot"
    WINDOW_HEIGHT = 660
    WINDOW_WIDTH = 550


@dataclass
class ChatHeaderLabel:
    """Class constants for the GUI header label."""

    HEADER_LABEL_TEXT = "Welcome! I'm Solent Library's ChatBot"
    HEADER_LABEL_PAD_Y = 8


@dataclass
class Helpers:
    """Class constants for the helpers."""

    SOLENT_RED = "#CF111C"
    WHITE = "#FFFFFF"
    BLACK = "#000000"
    GRAY = "#EBEBEB"
    MSG_WRAP_LENGTH = 250
    MSG_PAD_X = 12
    MSG_PAD_Y = 9
    FONT = "Helvetica 16"


class ChatGUI(ChatWindow, ChatHeaderLabel, Helpers):
    """Tkinter GUI for interacting with the ChatBot.

    Attributes:
        window: A tkinter window instance.
    """

    def __init__(self):
        self.window = Tk()
        self.flow_type = "query"
        self.default_answer_given = False
        self.text_widget = None
        self.bot = ChatBot()
        self.catalogue_option = None

        self.__setup_main_window()
        self.text_widget.tag_configure("tag-right", justify="right")
        self.text_widget.tag_configure("tag-left", justify="left")
        self.window.resizable(True, True)

        self.__insert_chat_bot_message(
            "Hi! I'm the Solent Library's Chatbot. I can answer questions about the "
            "library's opening times and access, booking study rooms or computers, the "
            "location of books, available ebooks, borrowing laptops, printing at the library, "
            "and available software and computer types along with their locations.\n"
            "I can also search the library's catalogue of books and journals.\n\n"
            "What can I help you with?"
        )

    def run(self):
        """Initiates the main loop for the tkinter window."""

        self.window.mainloop()  # pragma: no cover

    def __setup_main_window(self):
        self.window.title(self.WINDOW_TITLE)
        self.window.resizable(width=False, height=False)
        self.window.configure(
            width=self.WINDOW_WIDTH,
            height=self.WINDOW_HEIGHT,
            bg=self.WHITE,
        )

        # Header
        self.header_label = Label(
            self.window,
            bg=self.SOLENT_RED,
            fg=self.WHITE,
            text=self.HEADER_LABEL_TEXT,
            font=f"{self.FONT} bold",
            pady=self.HEADER_LABEL_PAD_Y,
        )
        self.header_label.place(relwidth=1)

        # Text widget area
        self.text_widget = Text(
            self.window,
            width=50,
            height=14,
            wrap=WORD,
            bg=self.WHITE,
            fg=self.WHITE,
            font=self.FONT,
            padx=5,
            pady=5,
        )

        # Scroll bar
        self.text_widget = ScrolledText.ScrolledText()
        self.text_widget.place(relheight=0.83, relwidth=1, rely=0.065)

        # Bottom label
        bottom_label = Label(self.window, bg=self.WHITE, height=80)
        bottom_label.place(relwidth=1, rely=0.895)

        # Question entry box
        self.entry_box = Entry(
            bottom_label, bg=self.WHITE, fg=self.BLACK, font=self.FONT
        )
        self.entry_box.place(relwidth=0.74, relheight=0.02, rely=0.008, relx=0.011)
        self.entry_box.focus()
        self.entry_box.bind("<Return>", self.__on_enter_pressed)

        # Send button
        send_button = Button(
            bottom_label,
            text="Send",
            font=self.FONT,
            width=20,
            bg="#EE7A84",
            command=lambda: self.__on_enter_pressed(None),
        )
        send_button.place(relx=0.77, rely=0.007, relheight=0.022, relwidth=0.22)

    def __insert_user_message(self, query):  # pragma: no cover
        """Handles the user's input and shows it in the window.

        Args:
            query (str): The message from the input.
        """

        # No message guard
        if not query:
            return

        # After sending the message, deletes it from the input.
        self.entry_box.delete(0, END)

        query_label = Label(
            self.text_widget,
            text=query,
            bg=self.SOLENT_RED,
            fg=self.WHITE,
            wraplength=self.MSG_WRAP_LENGTH,
            justify="left",
            padx=self.MSG_PAD_X,
            pady=self.MSG_PAD_Y,
        )
        self.text_widget.configure(cursor="arrow", state=NORMAL)
        self.text_widget.insert("end", "\n\n", "tag-right")
        self.text_widget.window_create("end", window=query_label)
        self.text_widget.configure(state=DISABLED)
        self.text_widget.tag_add("tag-right", "end-1c linestart", "end-1c lineend")
        self.text_widget.see(END)

    def __insert_chat_bot_message(self, response):
        """Inserts a text bubble on the window from the bot.

        Args:
            response (str): The bot response to show on the GUI.
        """

        response_label = Label(
            self.text_widget,
            text=response,
            bg=self.GRAY,
            fg=self.BLACK,
            wraplength=self.MSG_WRAP_LENGTH,
            justify="left",
            padx=self.MSG_PAD_X,
            pady=self.MSG_PAD_Y,
        )
        self.text_widget.configure(cursor="arrow", state=NORMAL)
        self.text_widget.insert("end", "\n\n", "tag-left")
        self.text_widget.window_create("end", window=response_label)
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)

    # pylint: disable-next=unused-argument, inconsistent-return-statements
    def __on_enter_pressed(self, event):  # pragma: no cover
        """An on enter press event listener.

        Gets the message and passes it to a flow handler.
        """

        user_input = self.entry_box.get()
        self.__insert_user_message(user_input)

        query_response = self.bot.get_response(user_input)
        bot_response = self.__get_response(user_input, query_response)

        if query_response == "catalogue":
            self.__insert_chat_bot_message(
                "You can find the full catalogues of books,"
                " journals and papers here:"
                " https://catalogue.solent.ac.uk/discovery/search?vid=44SSU_INST:VU1\n\n"
                "Would you like to search the Solent Library Catalogue?"
            )
            self.flow_type = "catalogue"
        else:
            self.__insert_chat_bot_message(bot_response)

    # pylint: disable-next=too-many-branches
    def __get_response(self, user_input, query_response):  # pragma: no cover
        """Takes user input and returns an appropriate response.

        Args:
            user_input (str): The text that the user typed into the box.

        Returns:
            str: What the chatbot should say in response to the user's input.
        """

        neg_input = user_input.lower().startswith("n")

        if self.flow_type == "query":
            if query_response:
                response = query_response + "\n\nWas this response helpful?"
                self.default_answer_given = False
                self.flow_type = "feedback"
            else:
                if not self.default_answer_given:
                    response = "I'm sorry, could you rephrase that?"
                    self.default_answer_given = True
                else:
                    response = "\n".join(
                        (
                            "I'm sorry, I don't know how to answer that.",
                            "Would you like to speak with a person?",
                        )
                    )
                    self.default_answer_given = False
                    self.flow_type = "human"

        elif self.flow_type == "feedback":
            if neg_input:
                response = "Would you like to speak with a person?"
                self.flow_type = "human"
            else:
                response = "Do you have any more questions?"
                self.flow_type = "more"

        elif self.flow_type == "more":
            if neg_input:
                response = "\n".join(
                    (
                        "Thank you for using the library's chatbot.",
                        "You can close this window now.",
                    )
                )
            else:
                response = "What else can I help you with?"
                self.flow_type = "query"

        elif self.flow_type == "human":
            if neg_input:
                response = "Do you have any more questions?"
                self.flow_type = "more"
            else:
                response = "Taking you to speak with a person..."
                web_open("https://libguides.solent.ac.uk/chat")

        elif self.flow_type == "catalogue":
            if neg_input:
                response = "Do you have any more questions?"
                self.flow_type = "more"
            else:
                response = MENU
                self.flow_type = "catalogue-1"
        elif self.flow_type == "catalogue-1":
            response = (
                f"What {OPTIONS_MAP_LABEL[user_input]} would you like to search for?"
            )
            self.catalogue_option = user_input
            self.flow_type = "catalogue-2"
        elif self.flow_type == "catalogue-2":
            find_item(self.catalogue_option, user_input)
            response = "Do you have any more questions?"
            self.flow_type = "more"

        return response
