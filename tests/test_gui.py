import unittest
from chat_bot.gui import ChatGUI


class TestGUI(unittest.TestCase):
    def test_window(self):
        instance = ChatGUI()
        self.assertEqual(instance.WINDOW_TITLE, "Solent Library's ChatBot")
        self.assertEqual(instance.WINDOW_HEIGHT, 420)
        self.assertEqual(instance.WINDOW_WIDTH, 340)
        self.assertEqual(instance.WINDOW_BG_COLOR, "#FFFFFF")

    def test_header_label(self):
        instance = ChatGUI()
        self.assertEqual(instance.HEADER_LABEL_BG, "#EE7A84")
        self.assertEqual(instance.HEADER_LABEL_FG, "#000000")
        self.assertEqual(
            instance.HEADER_LABEL_TEXT, "Welcome! I'm Solent Library's ChatBot"
        )
        self.assertEqual(instance.HEADER_LABEL_FONT, "Helvetica 11")
        self.assertEqual(instance.HEADER_LABEL_PAD_Y, 4)


if __name__ == "__main__":
    unittest.main()
