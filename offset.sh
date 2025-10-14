#!/bin/bash
# offset.sh

# Check for correct number of arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <filename-prefix> <offset>"
    echo "Example: $0 12-129 -5"
    exit 1
fi

# Assign parameters to variables
FILENAME=$1
OFFSET=$2

# Define file paths
INPUT_FILE="./pacenotes/${FILENAME}.json"
TEMP_FILE="./pacenotes/${FILENAME}.json.temp"

# Run the command
python3 offset_notes.py "$INPUT_FILE" "$OFFSET" > "$TEMP_FILE" && mv "$TEMP_FILE" "$INPUT_FILE"
