#!/usr/bin/env sh 
# get from  parameter otherwise default 
if [ -z "$1" ]
then
    url="https://www.youtube.com/watch?v=e0V9-8unJbg"
else
    url=$1
fi

yt-dlp \
    --ignore-errors \
    --write-info-json \
    --add-metadata \
    --write-sub \
    --sub-lang en,de,ja \
    --write-thumbnail \
    --embed-subs -f "mp4" ${url}
