#!/bin/bash

##
#Run with FILE_PATH 2> <somename>.log to get a log file to identify any corrupt or broken video files
##

target="$1"

for file in "$target"/*
do
    base=`basename "$file"`
    if [[ -f $file && $base = *.* ]]; then
      
      OUTPUT=$(ffprobe -loglevel 16 "$file")
      echo "$OUTPUT"
    
    fi
  
done

