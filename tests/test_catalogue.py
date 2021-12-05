"""Testing for catalogue module.

Tests the following: finding a book, author, or subject with a single word search.

Requires the following packages: unittest and chat_bot.
"""

from unittest import TestCase, main as run_tests
from unittest.mock import patch
from chat_bot.catalogue import run


class TestCatalogue(TestCase):
    """Test instance for the catalogue module."""

    @patch("builtins.input", side_effect=["1", "sport"])
    # pylint: disable=unused-argument
    def test_simple_book_search(self, mock_inputs):
        """Tests search by title option with a single word."""

        result = run()
        target = (
            "https://catalogue.solent.ac.uk/discovery/search?"
            "query=title,contains,sport&tab=Combined&"
            "search_scope=MyInstitution&vid=44SSU_INST:VU1&offset=0&mode=advanced"
        )
        self.assertEqual(result, target)

    @patch("builtins.input", side_effect=["2", "McGill"])
    # pylint: disable=unused-argument
    def test_simple_author_search(self, mock_inputs):
        """Tests search by author option with a single word."""

        result = run()
        target = (
            "https://catalogue.solent.ac.uk/discovery/search?"
            "query=creator,contains,McGill&tab=Combined&"
            "search_scope=MyInstitution&vid=44SSU_INST:VU1&offset=0&mode=advanced"
        )
        self.assertEqual(result, target)

    @patch("builtins.input", side_effect=["3", "maths"])
    # pylint: disable=unused-argument
    def test_simple_subject_search(self, mock_inputs):
        """Tests search by subject option with a single word."""

        result = run()
        target = (
            "https://catalogue.solent.ac.uk/discovery/search?"
            "query=sub,contains,maths&tab=Combined&"
            "search_scope=MyInstitution&vid=44SSU_INST:VU1&offset=0&mode=advanced"
        )
        self.assertEqual(result, target)


if __name__ == "__main__":
    run_tests()
