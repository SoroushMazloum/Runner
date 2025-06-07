#!/bin/bash

log_dir="./Logs"
output_dir="./LogsJSON"

mkdir -p "$output_dir"

cd "$log_dir"

for file in *.rcg; do
    log_name="${file%.rcg}"

    if [[ -f "$log_name.rcl" ]]; then
        loganalyzer --path "$log_name"

        for f in *.json; do
            if [[ "$f" == "$log_name"*.json ]]; then
                mv "$f" "../$output_dir/${log_name}.json"
            fi
        done
    fi
done
