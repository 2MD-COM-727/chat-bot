# GUI - DONE, 23.11.21
#from tkinter import Tk, Label, Text, Entry, Button, WORD # doesnt work
from tkinter import *
import tkinter.scrolledtext as ScrolledText

class ChatApp:
    def __init__(self):
        # define window
        self.window = Tk()
        # helper function
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("Solent Library's Chatbot")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=340, height=420, bg="#FFFFFF")

        # header
        header_label = Label(
            self.window,
            bg="#EE7A84",
            fg="#000000",
            text="Welcome! I'm Solent's Library Chatbot",
            font="Helvetica 11",
            pady=4,
        )
        header_label.place(relwidth=1)

        # divider
        line = Label(self.window,
                     width=350,
                     bg="#FCCE8E")
        line.place(relwidth=1, rely=0.065, relheight=0.005)

        # text widget area
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

        # scroll bal
        self.text_widget = ScrolledText.ScrolledText()

        self.text_widget.place(relheight=0.83, relwidth=1, rely=0.065)

        #chatbot initial message
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        initial_msg = Label(self.text_widget,
                            text="Hi, I'm Solent Lib Chatbot. I can help you with any query regarding "
                                 "library's opening times, printing info, booking group/individual "
                                 "study rooms or computers, borrowing laptops, available software and "
                                 "computer types alongside their location and lastly, books location.",
                            background='#ffdbde',
                            wraplength=180,
                            justify='left',
                            padx=10,
                            pady=5)
        self.text_widget.window_create('end', window=initial_msg)

        # bottom label
        bottom_label = Label(self.window, bg="#F6F6F7", height=80)
        bottom_label.place(relwidth=1, rely=0.895)

        # question entry box
        self.entry_box = Entry(bottom_label,
                               bg="#FFFFFF",
                               fg="#000000",
                               font="Helvetica 11")
        self.entry_box.place(relwidth=0.74, relheight=0.02, rely=0.008, relx=0.011)
        self.entry_box.focus()
        self.entry_box.bind("<Return>", self._on_enter_pressed)

        # send button
        send_button = Button(
            bottom_label,
            text="Send",
            font="Helvetica 10",
            width=20,
            bg="#EE7A84",
            command=lambda: self._on_enter_pressed(None),
        )
        send_button.place(relx=0.77, rely=0.007, relheight=0.022, relwidth=0.22)

    def _on_enter_pressed(self, event):
        msg = self.entry_box.get()
        self.insert_message(msg)

    def insert_message(self, msg):
        #in case of no message
        if not msg:
            return
        #after sending the message, we're deleting it
        self.entry_box.delete(0, END)

        #msg1 = f"{sender}: {msg}\n\n"
        msg1 = Label(self.text_widget,
                     text=f"{msg}",
                     background='#ffffd0',
                     wraplength=180,
                     justify='left',
                     padx=10,
                     pady=5)

        self.text_widget.tag_configure('tag-right', justify='right')
        self.text_widget.tag_configure('tag-left', justify='left')

        self.text_widget.configure(cursor="arrow", state=NORMAL)
        self.text_widget.insert('end', '\n\n', 'tag-right')
        self.text_widget.window_create('end', window=msg1)
        # this allings the label to the right hand side
        self.text_widget.tag_add("tag-right", "end-1c linestart", "end-1c lineend")
        self.text_widget.configure(state=DISABLED)

        #chatbot's response
        #msg2 = f"{bot_name}: {get_response(msg)}\n\n"
        msg="[Insert Bot's response here]"
        msg2 = Label(self.text_widget,
                     text=f"{msg}",
                     background='#ffdbde',
                     wraplength=180,
                     justify='left',
                     padx=10,
                     pady=5)
        self.text_widget.configure(cursor="arrow", state=NORMAL)
        self.text_widget.insert('end', '\n\n', 'tag-left')
        self.text_widget.window_create('end', window=msg2)
        self.text_widget.configure(state=DISABLED)

        #to see the end
        self.text_widget.see(END)

if __name__ == "__main__":
    app = ChatApp()
    app.run()