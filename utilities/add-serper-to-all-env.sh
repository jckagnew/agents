#!/bin/bash

# Add Serper API key to all .env files
SERPER_KEY="4d7237480b1009d11c895f2b9dc757dba924e36e"

echo "Adding Serper API key to all .env files..."

# Find all .env files and add the Serper key
find /Users/jackagnew/projects/agents -name ".env" -type f | while read file; do
    if ! grep -q "SERPER_API_KEY" "$file"; then
        echo "" >> "$file"
        echo "# Serper (for web search)" >> "$file"
        echo "SERPER_API_KEY=$SERPER_KEY" >> "$file"
        echo "Added to: $file"
    else
        echo "Already exists in: $file"
    fi
done

# Also check for .env.local files
find /Users/jackagnew/projects/agents -name ".env.local" -type f | while read file; do
    if ! grep -q "SERPER_API_KEY" "$file"; then
        echo "" >> "$file"
        echo "# Serper (for web search)" >> "$file"
        echo "SERPER_API_KEY=$SERPER_KEY" >> "$file"
        echo "Added to: $file"
    else
        echo "Already exists in: $file"
    fi
done

echo "Done! Serper API key added to all .env files."
