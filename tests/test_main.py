"""Testing for catalogue module.

Tests the following: finding a book, author, or subject with a single word search.

Requires the following packages: unittest and chat_bot.
"""

import unittest
from chat_bot.gui import ChatGUI


class TestMain(unittest.TestCase):
    """Test instance for the main module."""

    def test_gui_instance(self):
        """Checks if a ChatGUI instance exists."""

        self.assertIsNotNone(ChatGUI)


if __name__ == "__main__":
    unittest.main()
