import os
import sqlite3
import json
import re
import argparse

def sanitize_table_name(filename):
    """Sanitizes a filename to be a valid SQL table name."""
    table_name = filename.replace('.jsonl', '')
    table_name = re.sub(r'[^a-zA-Z0-9_]', '_', table_name)
    return table_name

def load_data_to_sqlite(category=None):
    """
    Loads .jsonl files from the extracted data directory into an SQLite database,
    optionally filtering by category.
    """
    db_path = 'data/recsys.db'
    source_dir = 'data/raw/extracted'

    if not os.path.exists(source_dir):
        print(f"Source directory not found: {source_dir}")
        print("Please make sure the data has been extracted first.")
        return

    print(f"Connecting to SQLite database at {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    files_to_load = [f for f in os.listdir(source_dir) if f.endswith('.jsonl')]
    if category:
        files_to_load = [f for f in files_to_load if category in f]
        print(f"Found {len(files_to_load)} files for category '{category}'.")

    for filename in files_to_load:
        table_name = sanitize_table_name(filename)
        file_path = os.path.join(source_dir, filename)

        try:
            cursor.execute(f"""SELECT name FROM sqlite_master WHERE type='table' AND name=?""", (table_name,))
            if cursor.fetchone():
                print(f"Table '{table_name}' already exists. Skipping file {filename}.")
                continue

            print(f"Processing {filename} into table '{table_name}'...")

            with open(file_path, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                if not first_line:
                    print(f"File {filename} is empty. Skipping.")
                    continue
                sample_data = json.loads(first_line)
                columns = list(sample_data.keys())
            
            sanitized_columns = [f'`{col}`' for col in columns]
            
            create_table_sql = f"""CREATE TABLE {table_name} ({ ', '.join([f'{col} TEXT' for col in sanitized_columns]) })"""
            print(f"  Creating table '{table_name}'...")
            cursor.execute(create_table_sql)

            batch_size = 50000
            batch = []
            
            print(f"  Loading data from {filename}...")
            with open(file_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    try:
                        data = json.loads(line)
                        ordered_values = [data.get(col) for col in columns]
                        batch.append(tuple(ordered_values))
                    except json.JSONDecodeError:
                        print(f"    Warning: Could not decode JSON on line {i} in {filename}. Skipping line.")
                        continue

                    if i % batch_size == 0:
                        placeholders = ', '.join(['?' for _ in sanitized_columns])
                        insert_sql = f"""INSERT INTO {table_name} ({ ', '.join(sanitized_columns) }) VALUES ({placeholders})"""
                        cursor.executemany(insert_sql, batch)
                        conn.commit()
                        batch = []
                        print(f"    ... inserted {i} rows into '{table_name}'.")

                if batch:
                    placeholders = ', '.join(['?' for _ in sanitized_columns])
                    insert_sql = f"""INSERT INTO {table_name} ({ ', '.join(sanitized_columns) }) VALUES ({placeholders})"""
                    cursor.executemany(insert_sql, batch)
                    conn.commit()
                    print(f"    ... inserted final {len(batch)} rows into '{table_name}'.")
            
            print(f"Finished loading data from {filename}.")

        except Exception as e:
            print(f"An error occurred while processing {filename}: {e}")
            conn.rollback()

    print("\nDatabase loading process finished.")
    conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load data into SQLite, optionally filtering by category.')
    parser.add_argument('--category', type=str, help='The category to load (e.g., Books, Electronics).')
    args = parser.parse_args()

    load_data_to_sqlite(args.category)
