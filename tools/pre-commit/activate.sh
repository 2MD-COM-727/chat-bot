#!/bin/bash

FILE_A=../.git/hooks/pre-commit.sample
if [ -f "$FILE_A" ];
then
	mv ../.git/hooks/pre-commit.sample ../.git/hooks/pre-commit
else
	echo $'#/bin/sh\nblack .\npylint chat_bot' > ../.git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit
fi
