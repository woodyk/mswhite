#!/usr/bin/env bash
#
# File: update_ms_white.sh
# Author: Wadih Khairallah
# Description: 
# Created: 2025-04-29 20:49:59
# Modified: 2025-04-29 21:21:08

# Exit on any error
set -e

# Check if the Archive directory exists
if [ ! -d "./Archive" ]; then
    echo "Error: './Archive' directory does not exist."
    exit 1
fi

# Get the most recent zip file
zip=$(ls -t ./Archive | head -1)

# Check if a zip file was found
if [ -z "$zip" ]; then
    echo "Error: No files found in './Archive' directory."
    exit 1
fi

# Check if the zip file exists
if [ ! -f "./Archive/$zip" ]; then
    echo "Error: File './Archive/$zip' does not exist."
    exit 1
fi

# Unzip the file with overwrite
if ! unzip -o "./Archive/$zip"; then
    echo "Error: Failed to unzip './Archive/$zip'."
    exit 1
fi

# Add all changes to git
if ! git add .; then
    echo "Error: Failed to stage changes with 'git add'."
    exit 1
fi

# Commit changes with the zip filename as the message
if ! git commit -m "$zip"; then
    echo "Error: Failed to commit changes."
    exit 1
fi

# Push changes to the remote repository
if ! git push; then
    echo "Error: Failed to push changes to remote repository."
    exit 1
fi

echo "Success: Archive '$zip' unzipped, committed, and pushed."
