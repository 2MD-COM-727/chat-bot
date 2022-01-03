# AE1 Software and Technical Report for a Chat Bot

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

## Details

| Key                            | Value                                                                                                                                                        |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Module Title                   | Introduction to Artificial Intelligence                                                                                                                      |
| Module Code                    | COM727                                                                                                                                                       |
| Level                          | 7                                                                                                                                                            |
| Assessment Title               | AE2-Project                                                                                                                                                  |
| Assessment Number              | 1                                                                                                                                                            |
| Assessment Type                | Software Prototype with Technical Report                                                                                                                     |
| Word Count                     | 2000 for Technical Report                                                                                                                                    |
| Consequence of exceeding count | There is no penalty for submitting below the word/count limit, but students should be aware that there is a risk they may not maximise their potential mark. |
| Individual/Group               | Group                                                                                                                                                        |
| Assessment Weighting           | 60%                                                                                                                                                          |
| Issue Date                     | Sep 2021                                                                                                                                                     |
| Hand-in                        | 10th of Jan 2022 by 4pm (presentation to be announced later on SOL)                                                                                          |
| Planned Feedback Date          | Within 4 working weeks                                                                                                                                       |
| Mode of Submission             | Online via SOL                                                                                                                                               |
| Number of Copies to Submit     | 1                                                                                                                                                            |
| Anonymous Marking              | This assessment will not be marked anonymously                                                                                                               |

## Brief

The recent growth and developments in AI (Artificial Intelligence) have revolutionised the way we live. Applications of AI are increasing day by day. Some of the mind-boggling applications include other fascinating applications include medical diagnostics, face recognition, speech recognition and synthesis, robotics, self-driving cars, chatbots, language translation, and many more.

This assignment asks to identify a real-world problem which can potentially be solved by apply AI techniques. You would design and implement a working prototype by applying appropriate AI methods to solve the identified problem. You should be able to demonstrate your prototype. You will consider legal, social, ethical, and professional issues as appropriate and relevant to your project.

You are required to build a working prototype for the following:

- Automatic chatbot tool (Automated responders and online customer support) A chatbot is an intelligent piece of software that is capable of communicating and performing actions similar to a human. Chatbots are used a lot in customer interaction, marketing on social network sites and instantly messaging the client. You need to propose and develop an approach for an automatic chatbot tool.

You will be expected to demonstrate your working prototype and the session will be arranged by your tutor. You will also be required to send your source code along with the instruction to run the prototype. Your technical report structure could have the following sections although you need to add more subsections; Introduction, Statement of the problem, Aims and Objectives, Proposed Solution along with the justification, Prototype Development & AI Algorithms, Limitation and Conclusion. Your submission should consist of the following:

- Your technical report (Word or PDF)
- Your source code with instructions on how to run the prototype

You will be working in groups (typically 4 to 5 students per group but it could be flexible to accommodate your personal preference) for the implementation of the prototype. However, the report needs to be written individually.

## Specifications

The best way to run this project is using MacOS as it has 'make' installed by default.

- Python 3.9
- Latest pip version
- Use a terminal (not Windows Cmd prompt if possible)

## How to run

You can have a look at the **Makefile** to see all the commands available.

### Training and running chat bot

- Install all dependencies with **make init** or **pip install -r requirements.txt**. If you are getting issues with install tensorflow on MacOS M1 chip, you'll need to follow [this guide](https://developer.apple.com/metal/tensorflow-plugin/).
- If there isn't already a **h5** file in **chat_bot/data**. Use **make start-admin** or **python chat_bot --admin** to run the project in admin mode where you can train the model with **option 2**.
- You can run the chat bot with **make start** or **python chat_bot**. If you experience any issue, you may have to run **python chat_bot/**main**.py**, but it is unlikely if you are using the correct version of python as per the specifications.

### Unit tests

You can use **make test** or **coverage run -m unittest discover -v chat_bot** followed by **coverage report -m**. You can generate and host the coverage report with **make host-cov** or **coverage html** followed by **cd htmlcov && python -m http.server && cd ..**.

If the **&&** doesn't work on your terminal, run each command on its own line.

Open a web browser and in the url go to **localhost:8000** or whatever it says in the terminal.

### Documentations

You'll need to generate the documentations first. Do this with **make build-docs** or **cd docs && sphinx-build -b html source build && cd ..**.

Then you can host it using **make host-docs** or **cd docs/build && python -m http.server && cd ../..**.

If the **&&** doesn't work on your terminal, run each command on its own line.

Open a web browser and in the url go to **localhost:8000** or whatever it says in the terminal.
