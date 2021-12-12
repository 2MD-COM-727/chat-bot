"""Creates a graphical user interface (GUI) for the chat bot.

Requires 'tkinter' (tk) and can be imported as a class module.

    Typical usage example:
        app = ChatGUI
        app.run()
"""

# pylint: disable=super-init-not-called
# pylint: disable=too-few-public-methods

from dataclasses import dataclass
from tkinter import Tk, Label, Text, Entry, Button, WORD, DISABLED, NORMAL, END
import tkinter.scrolledtext as ScrolledText
from webbrowser import open as web_open

from bot import ChatBot


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

        self.__setup_main_window()
        self.text_widget.tag_configure("tag-right", justify="right")
        self.text_widget.tag_configure("tag-left", justify="left")
        self.window.resizable(True, True)

        self.__insert_chat_bot_message(
            "Hi, I'm Solent Lib Chatbot. I can help you with any query regarding "
            "library's opening times, printing info, booking group/individual "
            "study rooms or computers, borrowing laptops, available software and "
            "computer types alongside their location and lastly, books location."
        )

    def run(self):
        """Initiates the main loop for the tkinter window."""

        self.window.mainloop()

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

    def __insert_user_message(self, query):
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

    # pylint: disable-next=unused-argument, too-many-branches
    def __on_enter_pressed(self, event):
        """An on enter press event listener.

        Gets the message and passes it to a flow handler.
        """

        user_input = self.entry_box.get()
        self.__insert_user_message(user_input)

        neg_input = user_input.lower().startswith("n")
        if self.flow_type == "query":
            response = self.bot.get_response(user_input)
            if response is None:
                if not self.default_answer_given:
                    self.__insert_chat_bot_message(
                        "I'm sorry, could you rephrase that?"
                    )
                    self.default_answer_given = True
                else:
                    self.__insert_chat_bot_message(
                        "I'm sorry, I don't know how to answer that."
                    )
                    self.__insert_chat_bot_message(
                        "Would you like to speak with a person?"
                    )
                    self.default_answer_given = False
                    self.flow_type = "human"
            else:
                self.__insert_chat_bot_message(response)
                self.default_answer_given = False
                self.__insert_chat_bot_message("Was this response helpful?")
                self.flow_type = "feedback"
        elif self.flow_type == "feedback":
            if neg_input:
                self.__insert_chat_bot_message("Would you like to speak with a person?")
                self.flow_type = "human"
            else:
                self.__insert_chat_bot_message("Do you have more questions?")
                self.flow_type = "more"
        elif self.flow_type == "more":
            if neg_input:
                self.__insert_chat_bot_message("Would you like to speak with a person?")
                self.flow_type = "human-end"
            else:
                self.__insert_chat_bot_message("What else can I help you with?")
                self.flow_type = "query"
        elif self.flow_type in ("human", "human-end"):
            if neg_input:
                if self.flow_type == "human-end":
                    self.__insert_chat_bot_message("Thank you for using our chat bot.")
                else:
                    self.__insert_chat_bot_message("Do you have more questions?")
                    self.flow_type = "more"
            else:
                self.__insert_chat_bot_message("Taking you to speak with a person...")
                web_open("https://libguides.solent.ac.uk/chat")
