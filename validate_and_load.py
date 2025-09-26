
import os
import json
import re
from pymongo import MongoClient, errors

def sanitize_collection_name(filename):
    """Sanitizes a filename to be a valid collection name."""
    name = filename.replace('.jsonl', '')
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    return name

def count_file_lines(filepath):
    """Counts the number of lines in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return sum(1 for line in f)

def load_collection_in_batches(db, collection_name, file_path):
    """Drops a collection and re-loads it from a file in batches."""
    collection = db[collection_name]
    
    print(f"  -> Dropping collection '{collection_name}'...")
    db.drop_collection(collection_name)
    
    print(f"  -> Loading data from {os.path.basename(file_path)} into collection '{collection_name}'...")
    
    batch_size = 50000
    batch = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                try:
                    doc = json.loads(line)
                    batch.append(doc)
                except json.JSONDecodeError:
                    print(f"    Warning: Could not decode JSON on line {i}. Skipping line.")
                    continue

                if i % batch_size == 0:
                    if batch:
                        collection.insert_many(batch, ordered=False)
                        print(f"    ... inserted {i} documents.")
                        batch = []
        
        if batch:
            collection.insert_many(batch, ordered=False)
            print(f"    ... inserted final {len(batch)} documents.")
        
        print(f"  -> Finished loading data for '{collection_name}'.")
        return True
    except Exception as e:
        print(f"An error occurred while processing {os.path.basename(file_path)}: {e}")
        return False

def validate_and_load():
    """
    Validates data integrity between source files and MongoDB.
    If a discrepancy is found, the corresponding collection is dropped and re-loaded.
    """
    try:
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        client.admin.command('ismaster')
        print("MongoDB connection successful.")
    except errors.ServerSelectionTimeoutError as err:
        print(f"MongoDB connection failed: {err}")
        print("Please ensure the mongod service is running.")
        return

    db = client['recsys_db']
    source_dir = 'data/raw/extracted'

    if not os.path.exists(source_dir):
        print(f"Source directory not found: {source_dir}")
        return

    source_files = [f for f in os.listdir(source_dir) if f.endswith('.jsonl')]
    
    print(f"Found {len(source_files)} source files to validate...")

    for filename in source_files:
        collection_name = sanitize_collection_name(filename)
        file_path = os.path.join(source_dir, filename)
        
        print(f"\n--- Validating: {collection_name} ---")

        # 1. Count source lines
        source_line_count = count_file_lines(file_path)
        print(f"Source file has {source_line_count} lines.")

        # 2. Count documents in MongoDB
        db_doc_count = db[collection_name].count_documents({})
        print(f"MongoDB collection has {db_doc_count} documents.")

        # 3. Compare
        if source_line_count == db_doc_count:
            print("Counts match. Skipping.")
            continue
        else:
            print(f"Discrepancy found ({source_line_count} vs {db_doc_count}). Reloading data.")
            # 4. Drop and reload
            load_collection_in_batches(db, collection_name, file_path)

    client.close()
    print("\n\nValidation and loading process finished.")

if __name__ == '__main__':
    validate_and_load()
