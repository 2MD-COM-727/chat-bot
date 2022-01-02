"""Testing for bot module.

Tests the following: bag of words operations.

Requires the following packages: unittest and chat_bot.
"""

import unittest
from bot import ChatBot


class TestGUI(unittest.TestCase):
    """Test instance for the bot module."""

    def test_bag_of_words(self):
        """Tests the bag of words operation."""

        self.assertEqual(len(ChatBot().bag_of_words("Where are the books?")), 1)


if __name__ == "__main__":
    unittest.main()
