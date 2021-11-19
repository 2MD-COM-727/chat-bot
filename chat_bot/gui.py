#STILL WORKING ON IT

from tkinter import *

red = "#E30D34"
in_between_colour = "#FCCE8E"
light_colour = "#FBE7D3"
white_colour = "#FFFFFF"
text_colour = "#000000"
font = "Helvetica 14"
font_bold = "Helvetica 13 bold"


class ChatApp:
    def __init__(self):
        # define window
        self.window = Tk()
        # helper function
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("Solent's Library Chatbot")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=440, height=520, bg=white_colour)

        # header
        header_label = Label(self.window, bg="#EE7A84", fg=text_colour, text="Welcome! Solent's Library Chatbot",
                             font=font, pady=5)
        header_label.place(relwidth=1)

        # divider
        line = Label(self.window, width=460, bg=in_between_colour)
        line.place(relwidth=1, rely=0.065, relheight=0.005)

        # text widget, so we don't display too many caracters in a line
        self.text_widget = Text(self.window, width=20, height=2, bg=white_colour, fg=text_colour, font=font, padx=5,
                                pady=5)
        self.text_widget.place(relheight=0.8, relwidth=1, rely=0.065)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # scroll bal
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        # bottom label
        bottom_label = Label(self.window, bg="#F6F6F7", height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        # question entry box
        self.entry_box = Entry(bottom_label, bg="#DEDEE1", fg=text_colour, font=font)
        self.entry_box.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.entry_box.focus()
        self.entry_box.bind("<Return>", self._on_enter_pressed)

        # send button
        send_button = Button(bottom_label, text="Send", font=font_bold, width=20, bg="#EE7A84",
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

    def _on_enter_pressed(self, event):
        msg = self.entry_box.get()
        self.insert_message(msg, "You")

    def insert_message(self, msg, sender):
        if not msg:
            return
        self.entry_box.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)
        # text area
        """
        This is to get the answer back from the chatbot:
        msg2 = f"{bot_name}: {get_response(msg)}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)
        """


if __name__ == "__main__":
    app = ChatApp()
    app.run()

