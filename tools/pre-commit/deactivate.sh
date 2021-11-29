#!/bin/bash

FILE_A=.git/hooks/pre-commit
if [ -f "$FILE_A" ];
then
    mv .git/hooks/pre-commit .git/hooks/pre-commit.sample
    echo $'\n** pre-commit has been deactivated **'
else
    echo $'\n** pre-commit has already been deactivated **'
fi