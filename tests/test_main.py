import unittest
from chat_bot.gui import ChatGUI


class TestMain(unittest.TestCase):
    def test_gui_instance(self):
        self.assertIsNotNone(ChatGUI)


if __name__ == "__main__":
    unittest.main()
