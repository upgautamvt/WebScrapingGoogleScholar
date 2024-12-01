#!/bin/bash

# Check if the user provided a search query as a command-line argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <search_query>"
    exit 1
fi

# Get the search query from the first argument
search_query="$1"

# Call the Python script with the search query as an argument
# python3 selenium_google_scraper.py "$search_query"

# use chrome selenium driver and use it in headless mode (i.e., no gui). This mimics real user is querying
python3 selenium_google_scraper.py "$search_query"

