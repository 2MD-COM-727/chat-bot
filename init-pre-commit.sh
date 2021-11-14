#!/bin/bash

echo $'#/bin/sh\nblack .\npylint chat_bot' > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
