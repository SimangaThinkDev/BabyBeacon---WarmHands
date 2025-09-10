#!/bin/bash

read -p "Commit message: " message

# It is very important to clean the repo before pushing, it makes
# the push size significantly smaller

git add . && git commit -m "$message" && git push

echo "Done adding commiting and pushing"

