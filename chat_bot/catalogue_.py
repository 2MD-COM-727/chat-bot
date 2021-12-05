"""Handles search queries for the Solent Library Catalogue.

Requires the following package: webbrowser.
"""

import webbrowser

MENU = """Search by?
1. Book title
2. Author
3. Subject
"""
OPTIONS_MAP = {
    "1": "title",
    "2": "creator",
    "3": "sub",
}
OPTIONS_MAP_LABEL = {
    "1": "book",
    "2": "author",
    "3": "subject",
}


def search():
    """Creates a query on the Solent Libray Catalogue.

    User can select between searches by book title, author, and subject area.
    Results will be shown as a redirect to the Solent Catalogue.
    """

    print(MENU)
    option = input(">>> ")
    print(f"What {OPTIONS_MAP_LABEL[option]} would you like to search for?")
    query = input(">>> ")

    query_url = ("https://catalogue.solent.ac.uk/discovery/search?"
                 f"query={OPTIONS_MAP[option]},contains,{query.strip()}&tab=Combined&"
                 "search_scope=MyInstitution&vid=44SSU_INST:VU1&offset=0&mode=advanced")
    webbrowser.open(query_url)
