import os
import json
from pymongo import MongoClient, errors
import re

def sanitize_collection_name(filename):
    """Sanitizes a filename to be a valid collection name."""
    name = filename.replace('.jsonl', '')
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    return name

def load_data_to_mongodb():
    """Loads all .jsonl files from the extracted data directory into a MongoDB database."""
    try:
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        # The ismaster command is cheap and does not require auth.
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

    files_to_load = [f for f in os.listdir(source_dir) if f.endswith('.jsonl')]

    for filename in files_to_load:
        collection_name = sanitize_collection_name(filename)
        collection = db[collection_name]

        print(f"Checking collection '{collection_name}'...")
        if collection.count_documents({}) > 0:
            print(f"Collection '{collection_name}' already contains documents. Skipping file {filename}.")
            continue

        print(f"Loading data from {filename} into collection '{collection_name}'...")
        
        batch_size = 50000
        batch = []
        try:
            with open(os.path.join(source_dir, filename), 'r', encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    try:
                        doc = json.loads(line)
                        batch.append(doc)
                    except json.JSONDecodeError:
                        print(f"  Warning: Could not decode JSON on line {i} in {filename}. Skipping line.")
                        continue

                    if i % batch_size == 0:
                        if batch:
                            collection.insert_many(batch, ordered=False) # ordered=False can be faster
                            print(f"  ... inserted {i} documents into '{collection_name}'.")
                            batch = []
            
            # Insert any remaining documents in the last batch
            if batch:
                collection.insert_many(batch, ordered=False)
                print(f"  ... inserted final {len(batch)} documents into '{collection_name}'.")
            
            print(f"Finished loading data from {filename}.")

        except Exception as e:
            print(f"An error occurred while processing {filename}: {e}")

    client.close()
    print("\nMongoDB data loading process finished.")

if __name__ == '__main__':
    load_data_to_mongodb()
