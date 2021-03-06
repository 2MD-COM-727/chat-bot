# AE1 Software and Technical Report for a Chat Bot

## Specification

The best way to run this project is using MacOS as it has 'make' installed by default.

- Python 3.9
- Latest pip version
- Use a terminal (not Windows Cmd prompt if possible)

## Usage

```
# Installs all dependencies (pip install)
make init

# Runs the ChatBot package
make start

# Generates documentation from docstrings (sphinx)
make build-docs

# Spins up dev server to view documentation (localhost:8000)
make host-docs

# Run unit tests
make test

# Spins up dev server to view coverage (localhost:8000)
make host-cov

```

## Usage (detailed)

You can have a look at the **Makefile** to see all the commands available.

### Training and running chat bot

- Install all dependencies with **make init** or **pip install -r requirements.txt**. If you are getting issues with install tensorflow on MacOS M1 chip, you'll need to follow [this guide](https://developer.apple.com/metal/tensorflow-plugin/).
- If there isn't already a **h5** file in **chat_bot/data**. Use **make start-admin** or **python chat_bot --admin** to run the project in admin mode where you can train the model with **option 2**.
- You can run the chat bot with **make start** or **python chat_bot**. If you experience any issue, you may have to run **python chat_bot/__main__.py**, but it is unlikely if you are using the correct version of python as per the specifications.

### Unit tests

You can use **make test** or **coverage run -m unittest discover -v chat_bot** followed by **coverage report -m**. You can generate and host the coverage report with **make host-cov** or **coverage html** followed by **cd htmlcov && python -m http.server && cd ..**.

If the **&&** doesn't work on your terminal, run each command on its own line.

Open a web browser and in the url go to **localhost:8000** or whatever it says in the terminal.

### Documentations

You'll need to generate the documentations first. Do this with **make build-docs** or **cd docs && sphinx-build -b html source build && cd ..**.

Then you can host it using **make host-docs** or **cd docs/build && python -m http.server && cd ../..**.

If the **&&** doesn't work on your terminal, run each command on its own line.

Open a web browser and in the url go to **localhost:8000** or whatever it says in the terminal.

## Important information

- If you evaluate the optimal number of epochs using option 3 on the admin TUI. It will change some crucial files used to run the chat bot. Please retrain the chat bot again before running the chat bot, otherwise, it will be very inaccurate.

