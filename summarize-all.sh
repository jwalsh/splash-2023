#!/usr/bin/env bash 
# Path: summarize-clj.sh
DELIMITER="--------------------------------------------------"
echo > linting.txt
# Prepare all of the .clj files to be sent in a ChatGPT or Claude chat for review: 
for CLJ in $(find . -type f -name "*.clj"); do 
    echo $DELIMITER >> linting.txt
    echo "Linting $CLJ" >> linting.txt
    clj-kondo --lint $CLJ >> linting.txt
    echo "" >> linting.txt
    echo '```' >> linting.txt
    cat $CLJ >> linting.txt
    echo '```' >> linting.txt
    echo "" >> linting.txt
done

# Add shell and Python files to the linting.txt file:
for FILE in $(find . -type f -name "*.py") \
$(find . -type f -name "*.py") \
Makefile ; do 
    echo $DELIMITER >> linting.txt
    echo "$FILE" >> linting.txt
    echo "" >> linting.txt
    echo '```' >> linting.txt
    cat $FILE >> linting.txt
    echo '```' >> linting.txt
    echo "" >> linting.txt

done 
