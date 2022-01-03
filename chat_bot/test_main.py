"""Testing for main module.

Tests the following: Checks if there's an instance of GUI.

Requires the following packages: unittest and chat_bot.
"""

import unittest
from gui import ChatGUI


class TestMain(unittest.TestCase):
    """Test instance for the main module."""

    def test_gui_instance(self):
        """Checks if a ChatGUI instance exists."""

        self.assertIsNotNone(ChatGUI)


if __name__ == "__main__":
    unittest.main()
