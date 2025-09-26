#!/bin/bash

# List of the main data categories
CATEGORIES=(
    "All_Beauty"
    "Beauty_and_Personal_Care"
    "Books"
    "Clothing_Shoes_and_Jewelry"
    "Electronics"
    "Health_and_Household"
    "Home_and_Kitchen"
    "Subscription_Boxes"
)

# Directory where the extracted .jsonl files are
SOURCE_DIR="data/raw/extracted"

echo "--- Comparing SQLite table counts with source file line counts ---"

for category in "${CATEGORIES[@]}"; do
    echo "--- Category: $category ---"
    
    # Count lines in the source .jsonl file
    # Using -l to count lines
    line_count=$(wc -l < "$SOURCE_DIR/$category.jsonl")
    echo "Source file line count: $line_count"

    # Query the database for the row count
    # The table name is the same as the category
    db_count=$(python query_db.py sqlite "$category")
    echo "Database row count: $db_count"
    
    echo "" # Add a blank line for readability
done
