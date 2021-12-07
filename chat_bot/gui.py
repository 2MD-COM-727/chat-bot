"""Creates a graphical user interface (GUI) for the chat bot.

Requires 'tkinter' (tk) and can be imported as a class module.

    Typical usage example:
        app = ChatGUI
        app.run()
"""

# pylint: disable=super-init-not-called

from dataclasses import dataclass
from tkinter import Tk, Label, Text, Entry, Button, WORD, DISABLED, NORMAL, END
import tkinter.scrolledtext as ScrolledText

@dataclass
class ChatWindow:
    """Class constants for the GUI window."""

    WINDOW_TITLE = "Solent Library's ChatBot"
    WINDOW_HEIGHT = 420
    WINDOW_WIDTH = 340
    WINDOW_BG_COLOR = "#FFFFFF"


@dataclass
class ChatHeaderLabel:
    """Class constants for the GUI header label."""

    HEADER_LABEL_BG = "#EE7A84"
    HEADER_LABEL_FG = "#000000"
    HEADER_LABEL_TEXT = "Welcome! I'm Solent Library's ChatBot"
    HEADER_LABEL_FONT = "Helvetica 11"
    HEADER_LABEL_PAD_Y = 4


class ChatGUI(ChatWindow, ChatHeaderLabel):
    """Tkinter GUI for interacting with the ChatBot.

    Attributes:
        window: A tkinter window instance.
    """

    def __init__(self):
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        """Initiates the main loop for the tkinter window."""

        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title(self.WINDOW_TITLE)
        self.window.resizable(width=False, height=False)
        self.window.configure(
            width=self.WINDOW_WIDTH,
            height=self.WINDOW_HEIGHT,
            bg=self.WINDOW_BG_COLOR,
        )

        # Header
        self.header_label = Label(
            self.window,
            bg=self.HEADER_LABEL_BG,
            fg=self.HEADER_LABEL_FG,
            text=self.HEADER_LABEL_TEXT,
            font=self.HEADER_LABEL_FONT,
            pady=self.HEADER_LABEL_PAD_Y,
        )
        self.header_label.place(relwidth=1)

        # Divider
        line = Label(self.window, width=350, bg="#FCCE8E")
        line.place(relwidth=1, rely=0.065, relheight=0.005)

        # Text widget area
        self.text_widget = Text(
            self.window,
            width=50,
            height=13,
            wrap=WORD,
            bg="#FFFFFF",
            fg="#000000",
            font="Helvetica 11",
            padx=5,
            pady=5,
        )

        # Scroll bar
        self.text_widget = ScrolledText.ScrolledText()

        self.text_widget.place(relheight=0.83, relwidth=1, rely=0.065)

        # ChatBot's initial message
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        initial_msg = Label(
            self.text_widget,
            text="Hi, I'm Solent Lib Chatbot. I can help you with any query regarding "
            "library's opening times, printing info, booking group/individual "
            "study rooms or computers, borrowing laptops, available software and "
            "computer types alongside their location and lastly, books location.",
            background="#ffdbde",
            wraplength=180,
            justify="left",
            padx=10,
            pady=5,
        )
        self.text_widget.window_create("end", window=initial_msg)

        # Bottom label
        bottom_label = Label(self.window, bg="#F6F6F7", height=80)
        bottom_label.place(relwidth=1, rely=0.895)

        # Question entry box
        self.entry_box = Entry(
            bottom_label, bg="#FFFFFF", fg="#000000", font="Helvetica 11"
        )
        self.entry_box.place(relwidth=0.74, relheight=0.02, rely=0.008, relx=0.011)
        self.entry_box.focus()
        self.entry_box.bind("<Return>", self._on_enter_pressed)

        # Send button
        send_button = Button(
            bottom_label,
            text="Send",
            font="Helvetica 10",
            width=20,
            bg="#EE7A84",
            command=lambda: self._on_enter_pressed(None),
        )
        send_button.place(relx=0.77, rely=0.007, relheight=0.022, relwidth=0.22)

    # pylint: disable-next=unused-argument
    def _on_enter_pressed(self, event):
        """An on enter press event listener.

        Gets the message and passes it to the insert_message function.
        """
        msg = self.entry_box.get()
        self.insert_message(msg)

    def insert_message(self, msg):
        """Handles the user's input and shows it in the window.

        Args:
            msg (str): The message from the input.
        """

        # No message guard
        if not msg:
            return

        # After sending the message, deletes it from the input.
        self.entry_box.delete(0, END)

        msg1 = Label(
            self.text_widget,
            text=f"{msg}",
            background="#ffffd0",
            wraplength=180,
            justify="left",
            padx=10,
            pady=5,
        )

        self.text_widget.tag_configure("tag-right", justify="right")
        self.text_widget.tag_configure("tag-left", justify="left")

        self.text_widget.configure(cursor="arrow", state=NORMAL)
        self.text_widget.insert("end", "\n\n", "tag-right")
        self.text_widget.window_create("end", window=msg1)
        # this allings the label to the right hand side
        self.text_widget.tag_add("tag-right", "end-1c linestart", "end-1c lineend")
        self.text_widget.configure(state=DISABLED)

        # chatbot's response
        msg = "[Insert Bot's response here]"
        msg2 = Label(
            self.text_widget,
            text=f"{msg}",
            background="#ffdbde",
            wraplength=180,
            justify="left",
            padx=10,
            pady=5,
        )
        self.text_widget.configure(cursor="arrow", state=NORMAL)
        self.text_widget.insert("end", "\n\n", "tag-left")
        self.text_widget.window_create("end", window=msg2)
        self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)
