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

cat linting.txt