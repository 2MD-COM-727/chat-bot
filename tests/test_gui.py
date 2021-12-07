"""Testing for gui module.

Tests the following: the tkinter window and header instance/style.

Requires the following packages: unittest and chat_bot.
"""

import unittest
from chat_bot.gui import ChatGUI


class TestGUI(unittest.TestCase):
    """Test instance for the gui module."""

    def test_window(self):
        """Tests the tkinter window style."""

        instance = ChatGUI()
        self.assertEqual(instance.WINDOW_TITLE, "Solent Library's ChatBot")
        self.assertEqual(instance.WINDOW_HEIGHT, 420)
        self.assertEqual(instance.WINDOW_WIDTH, 340)

    def test_header_label(self):
        """Tests the tkinter header style."""

        instance = ChatGUI()
        self.assertEqual(
            instance.HEADER_LABEL_TEXT, "Welcome! I'm Solent Library's ChatBot"
        )
        self.assertEqual(instance.HEADER_LABEL_FONT, "Helvetica 16 bold")
        self.assertEqual(instance.HEADER_LABEL_PAD_Y, 8)


if __name__ == "__main__":
    unittest.main()
