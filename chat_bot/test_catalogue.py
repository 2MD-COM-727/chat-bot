"""Testing for catalogue module.

Tests the following: finding a book, author, or subject with a single word search.

Requires the following packages: unittest and chat_bot.
"""

from unittest import TestCase, main as run_tests
from catalogue import find_item


class TestCatalogue(TestCase):
    """Test instance for the catalogue module."""

    def test_simple_book_search(self):
        """Tests search by title option with a single word."""

        result = find_item("1", "sport")
        target = (
            "https://catalogue.solent.ac.uk/discovery/search?"
            "query=title,contains,sport&tab=Combined&"
            "search_scope=MyInstitution&vid=44SSU_INST:VU1&offset=0&mode=advanced"
        )
        self.assertEqual(result, target)

    def test_simple_author_search(self):
        """Tests search by author option with a single word."""

        result = find_item("2", "McGill")
        target = (
            "https://catalogue.solent.ac.uk/discovery/search?"
            "query=creator,contains,McGill&tab=Combined&"
            "search_scope=MyInstitution&vid=44SSU_INST:VU1&offset=0&mode=advanced"
        )
        self.assertEqual(result, target)

    def test_simple_subject_search(self):
        """Tests search by subject option with a single word."""

        result = find_item("3", "maths")
        target = (
            "https://catalogue.solent.ac.uk/discovery/search?"
            "query=sub,contains,maths&tab=Combined&"
            "search_scope=MyInstitution&vid=44SSU_INST:VU1&offset=0&mode=advanced"
        )
        self.assertEqual(result, target)


if __name__ == "__main__":
    run_tests()
