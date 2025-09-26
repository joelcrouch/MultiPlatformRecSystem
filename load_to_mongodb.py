import os
import json
from pymongo import MongoClient, errors
import re
import shutil
import argparse

def check_disk_space(path, min_free_gb=20):
    """Check if sufficient disk space is available"""
    free_bytes = shutil.disk_usage(path).free
    free_gb = free_bytes / (1024**3)
    print(f"Checking disk space for '{path}'. Available: {free_gb:.1f}GB. Required: {min_free_gb}GB.")
    if free_gb < min_free_gb:
        raise Exception(f"Insufficient disk space: {free_gb:.1f}GB available, but {min_free_gb}GB is required.")

def sanitize_collection_name(filename):
    """Sanitizes a filename to be a valid collection name."""
    name = filename.replace('.jsonl', '')
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    return name

def load_data_to_mongodb(category=None):
    """Loads .jsonl files from the extracted data directory into a MongoDB database, optionally filtering by category."""
    try:
        home_path = os.path.expanduser('~')
        check_disk_space(home_path, min_free_gb=20)
    except Exception as e:
        print(f"Pre-flight check failed: {e}")
        return

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

    files_to_load = [f for f in os.listdir(source_dir) if f.endswith('.jsonl')]
    if category:
        files_to_load = [f for f in files_to_load if category in f]
        print(f"Found {len(files_to_load)} files for category '{category}'.")

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
                            collection.insert_many(batch, ordered=False)
                            print(f"  ... inserted {i} documents into '{collection_name}'.")
                            batch = []
            
            if batch:
                collection.insert_many(batch, ordered=False)
                print(f"  ... inserted final {len(batch)} documents into '{collection_name}'.")
            
            print(f"Finished loading data from {filename}.")

        except Exception as e:
            print(f"An error occurred while processing {filename}: {e}")

    client.close()
    print("\nMongoDB data loading process finished.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load data into MongoDB, optionally filtering by category.')
    parser.add_argument('--category', type=str, help='The category to load (e.g., Books, Electronics).')
    args = parser.parse_args()

    load_data_to_mongodb(args.category)