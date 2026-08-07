#!/bin/bash

sites=(
    "google.com"
    "youtube.com"
    "wikipedia.org"
    "github.com"
    "stackoverflow.com"
    "cloudflare.com"
    "amazon.com"
    "microsoft.com"
    "apple.com"
    "bbc.com"
)

for site in "${sites[@]}"
do
    filename=$(echo "$site" | tr '.' '_').txt
    echo "Tracing $site..."
    echo "Traceroute result for $site" > "$filename"
    echo "============================" >> "$filename"
    traceroute -w 1 -q 2 -m 20 "$site" > "$filename" 2>&1
    echo "Saved $filename"
done

echo "Completed all traceroutes."