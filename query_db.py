
import argparse
import sqlite3
import os
from pymongo import MongoClient, errors

def query_sqlite(table_name):
    """Queries the SQLite database for the number of rows in a table."""
    db_path = 'data/recsys.db'
    if not os.path.exists(db_path):
        print(f"SQLite database not found at {db_path}")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT count(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"Table '{table_name}' has {count} rows.")
    except sqlite3.OperationalError as e:
        print(f"Error querying SQLite: {e}")
    finally:
        if conn:
            conn.close()

def query_mongodb(collection_name):
    """Queries the MongoDB database for the number of documents in a collection."""
    try:
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        client.admin.command('ismaster')
        db = client['recsys_db']
        
        if collection_name not in db.list_collection_names():
            print(f"Collection '{collection_name}' not found in the database.")
            client.close()
            return

        collection = db[collection_name]
        count = collection.count_documents({})
        print(f"Collection '{collection_name}' has {count} documents.")
    except errors.ServerSelectionTimeoutError as err:
        print(f"MongoDB connection failed: {err}")
    finally:
        if 'client' in locals() and client:
            client.close()

def main():
    parser = argparse.ArgumentParser(description='Query the number of records in a database.')
    parser.add_argument('database', choices=['sqlite', 'mongodb'], help='The database to query.')
    parser.add_argument('table_or_collection', help='The name of the table or collection to query.')
    args = parser.parse_args()

    if args.database == 'sqlite':
        query_sqlite(args.table_or_collection)
    elif args.database == 'mongodb':
        query_mongodb(args.table_or_collection)

if __name__ == '__main__':
    main()
