#!/bin/bash

cd Bins || { echo "Not fond Bins"; exit 1; }

for dir in */ ; do
    dir=${dir%/}
    start_file="$dir/start"

    [ ! -f "$start_file" ] && continue

    teamname=$(grep '^teamname=' "$start_file" | cut -d'"' -f2)

    if [ -z "$teamname" ]; then
        continue
    fi

    if [ "$dir" != "$teamname" ]; then
        mv "$dir" "$teamname"
    fi
done
