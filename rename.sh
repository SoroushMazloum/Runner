#!/bin/bash

cd Bins || { echo "Bins dir not found"; exit 1; }

for dir in */ ; do
    dir=${dir%/}
    
    if [ -f "$dir/start" ]; then
        start_file="$dir/start"
    elif [ -f "$dir/start.sh" ]; then
        start_file="$dir/start.sh"
    else
        continue
    fi

    teamname=$(grep '^teamname=' "$start_file" | cut -d'"' -f2)

    if [ -z "$teamname" ]; then
        continue
    fi

    if [ "$dir" != "$teamname" ]; then
        mv "$dir" "$teamname"
    fi
done