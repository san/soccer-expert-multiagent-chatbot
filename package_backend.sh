#!/bin/bash

# Package backend folder, respecting .gitignore rules
# Usage: ./package_backend.sh

set -e

# Define output filename with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="backend_${TIMESTAMP}.tar.gz"

echo "📦 Packaging backend folder to $OUTPUT_FILE..."

# Create tarball using git archive (respects .gitignore automatically)
# This only includes tracked files in the backend directory
git archive --format=tar.gz HEAD backend/ -o "$OUTPUT_FILE"

if [ -f "$OUTPUT_FILE" ]; then
    SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    echo "✅ Successfully created: $OUTPUT_FILE ($SIZE)"
else
    echo "❌ Failed to create package"
    exit 1
fi
