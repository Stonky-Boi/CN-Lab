#!/bin/bash

sites=("google.com" "wikipedia.org")

for site in "${sites[@]}"
do
    output=$(echo "$site" | tr '.' '_')_rtt.txt
    echo "Iteration RTT(ms)" > "$output"
    for i in {1..10}
    do
        echo "Running $site iteration $i"
        rtt=$(traceroute -m 20 -q 1 -w 2 "$site" 2>/dev/null \
        | grep -oE '[0-9]+\.[0-9]+ ms' \
        | tail -1 \
        | awk '{print $1}')
        if [ -z "$rtt" ]; then
            rtt="NA"
        fi
        echo "$i $rtt" >> "$output"
        sleep 1
    done
done