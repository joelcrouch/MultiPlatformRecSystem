import os
import gzip
import shutil
import zipfile
import argparse

def extract_data(category=None):
    """
    Extracts compressed datasets from the data/raw directory.
    If a category is specified, only files matching that category are extracted.
    - .jsonl.gz files are extracted to data/raw/extracted/
    - ml-32m.zip is extracted to data/
    """
    raw_dir = 'data/raw'
    extracted_dir = os.path.join(raw_dir, 'extracted')
    data_dir = 'data'

    os.makedirs(extracted_dir, exist_ok=True)

    if category:
        print(f"Starting extraction for category: {category}...")
    else:
        print("Starting full data extraction...")

    for filename in os.listdir(raw_dir):
        if category and category not in filename:
            continue

        source_path = os.path.join(raw_dir, filename)

        if filename.endswith('.jsonl.gz'):
            output_filename = filename.replace('.gz', '')
            output_path = os.path.join(extracted_dir, output_filename)

            if os.path.exists(output_path):
                print(f"File {output_filename} already exists. Skipping.")
                continue

            print(f"Extracting {filename} to {output_path}...")
            try:
                with gzip.open(source_path, 'rb') as f_in:
                    with open(output_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                print(f"Successfully extracted {filename}.")
            except Exception as e:
                print(f"Error extracting {filename}: {e}")

        elif filename == 'ml-32m.zip':
            extract_path = os.path.join(data_dir, 'ml-32m')
            if not os.path.exists(extract_path):
                print(f"Extracting {filename} to {data_dir}...")
                try:
                    with zipfile.ZipFile(source_path, 'r') as zip_ref:
                        zip_ref.extractall(data_dir)
                    print(f"Successfully extracted {filename}.")
                except Exception as e:
                    print(f"Error extracting {filename}: {e}")
            else:
                print(f"Skipping {filename}, directory {extract_path} already exists.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract data, optionally filtering by category.')
    parser.add_argument('--category', type=str, help='The category to extract (e.g., Books, Electronics).')
    args = parser.parse_args()

    extract_data(args.category)
    print("\nExtraction process finished.")
