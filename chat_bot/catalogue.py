"""Handles search queries for the Solent Library Catalogue.

Requires the following package: webbrowser.
"""

from webbrowser import open as web_open

MENU = """
Search by:

1. Book title
2. Author
3. Subject
"""
OPTIONS_MAP_LABEL = {
    "1": "book",
    "2": "author",
    "3": "subject",
}
OPTIONS_MAP = {
    "1": "title",
    "2": "creator",
    "3": "sub",
}


def find_item(option, query):
    """Creates a query on the Solent Library's Catalogue.

    User can select between searches by book title, author, and subject area.
    Results will be shown as a redirect to the Solent Catalogue.
    """

    query_url = (
        "https://catalogue.solent.ac.uk/discovery/search?"
        f"query={OPTIONS_MAP[option]},contains,{query.strip()}&tab=Combined&"
        "search_scope=MyInstitution&vid=44SSU_INST:VU1&offset=0&mode=advanced"
    )
    web_open(query_url)
    return query_url
