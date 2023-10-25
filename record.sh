#!/usr/bin/env bash

OUT=${1-output.aac}
ffmpeg -f avfoundation -ac 2 -i :0 -c:a aac -ab 96k $OUT
