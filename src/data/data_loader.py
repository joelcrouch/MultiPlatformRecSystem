import pandas as pd
import numpy as np
import dask.dataframe as dd
# Removed urllib.request as we are no longer downloading Amazon data
import zipfile
import os
import gzip
from tqdm.auto import tqdm

class MultiDomainDatasetIntegrator:
    def __init__(self):
        self.datasets = {'amazon': {}, 'movielens': {}}
        self.unified_schema = self.create_unified_schema()

    def download_amazon_data(self, categories):
        """
        Loads and processes Amazon review data for a given list of categories
        from manually downloaded .jsonl.gz files in ./data/raw/{category}/.
        Saves processed data to Parquet files in ./data/amazon/.
        """
        raw_data_base_dir = './data/raw' # New base directory for raw files
        processed_data_save_dir = './data/amazon' # Directory to save parquet files
        os.makedirs(processed_data_save_dir, exist_ok=True)

        for category in tqdm(categories, desc="Amazon Categories"): # tqdm for categories loop
            print(f"Processing Amazon category: {category}...")
            self.datasets['amazon'][category] = {}

            # --- Load and process reviews ---
            # Expecting file at data/raw/{category}_reviews.jsonl.gz
            review_raw_gz_path = os.path.join(raw_data_base_dir, f"{category}.jsonl.gz")
            review_parquet_path = os.path.join(processed_data_save_dir, f"{category}_reviews.parquet")

            if not os.path.exists(review_raw_gz_path):
                print(f"  Warning: Raw review file not found for {category} at {review_raw_gz_path}. Skipping.")
                continue # Skip to next category if file not found

            print(f"  Loading reviews for {category} from {review_raw_gz_path}...")
            reviews_ddf = dd.read_json(review_raw_gz_path, lines=True)
            
            print(f"  Saving reviews for {category} to {review_parquet_path}...")
            reviews_ddf.to_parquet(review_parquet_path, index=False, overwrite=True)
            self.datasets['amazon'][category]['reviews_path'] = review_parquet_path
            # os.remove(review_raw_gz_path) # Do not remove raw files, user downloaded them manually

            # --- Load and process metadata ---
            # Expecting file at data/raw/meta_{category}.jsonl.gz
            meta_raw_gz_path = os.path.join(raw_data_base_dir, f"meta_{category}.jsonl.gz")
            meta_parquet_path = os.path.join(processed_data_save_dir, f"meta_{category}.parquet")

            if not os.path.exists(meta_raw_gz_path):
                print(f"  Warning: Raw meta file not found for {category} at {meta_raw_gz_path}. Skipping.")
                continue # Skip to next category if file not found

            print(f"  Loading metadata for {category} from {meta_raw_gz_path}...")
            meta_ddf = dd.read_json(meta_raw_gz_path, lines=True)
            
            print(f"  Saving metadata for {category} to {meta_parquet_path}...")
            meta_ddf.to_parquet(meta_parquet_path, index=False, overwrite=True)
            self.datasets['amazon'][category]['metadata_path'] = meta_parquet_path
            # os.remove(meta_raw_gz_path) # Do not remove raw files, user downloaded them manually

        print("Amazon data processing complete. Data saved to Parquet files.")


    def download_movielens_data(self):
        """
        Extracts the MovieLens 32M dataset from a manually downloaded zip file
        located in ./data/raw/ml-32m.zip.
        """
        raw_zip_path = "./data/raw/ml-32m.zip" # Expecting zip file here
        processed_movielens_dir = "./data/processed/movielens/"
        os.makedirs(processed_movielens_dir, exist_ok=True)

        print(f"Checking for MovieLens zip file at: {raw_zip_path}")
        if not os.path.exists(raw_zip_path):
            print(f"  Warning: MovieLens 32M zip file not found at {raw_zip_path}. Skipping MovieLens processing.")
            return # Skip if file not found

        print("Extracting MovieLens 32M dataset...")
        with zipfile.ZipFile(raw_zip_path, 'r') as zip_ref:
            zip_ref.extractall(processed_movielens_dir)
        print("Extraction complete.")
        
        self.datasets['movielens']['path'] = os.path.join(processed_movielens_dir, 'ml-32m')


    def process_movielens_data(self):
        """Process MovieLens 32M dataset"""
        # This function will now load from the extracted files, not from memory
        movielens_path = self.datasets['movielens']['path']
        processed_movielens_dir = os.path.dirname(movielens_path) # This will be ./data/processed/movielens/

        ratings_df = pd.read_csv(os.path.join(movielens_path, 'ratings.csv'))
        movies_df = pd.read_csv(os.path.join(movielens_path, 'movies.csv'))
        tags_df = pd.read_csv(os.path.join(movielens_path, 'tags.csv'))

        # Save to Parquet
        ratings_df.to_parquet(os.path.join(processed_movielens_dir, 'ratings.parquet'), index=False)
        movies_df.to_parquet(os.path.join(processed_movielens_dir, 'movies.parquet'), index=False)
        tags_df.to_parquet(os.path.join(processed_movielens_dir, 'tags.parquet'), index=False)

        print("MovieLens data processed and saved to Parquet files.")

        # Return paths to the parquet files instead of dataframes
        return {
            'ratings_path': os.path.join(processed_movielens_dir, 'ratings.parquet'),
            'movies_path': os.path.join(processed_movielens_dir, 'movies.parquet'),
            'tags_path': os.path.join(processed_movielens_dir, 'tags.parquet')
        }

    def create_unified_schema(self):
        """Create unified interaction schema across domains"""
        return {
            'user_id': 'int64',
            'item_id': 'int64',
            'rating': 'float32',
            'timestamp': 'int64',
            'domain': 'string',
            'interaction_type': 'string',
            'context': 'string'
        }

if __name__ == '__main__':
    integrator = MultiDomainDatasetIntegrator()
    print("Starting data processing from raw files...")

    amazon_categories_to_download = [
        'Electronics',
        'Home_and_Kitchen',
        'Clothing_Shoes_and_Jewelry',
        'Beauty_and_Personal_Care',
        'Health_and_Household',
        'Books',
        'All_Beauty',
        'Subscription_Boxes'
    ]
    
    integrator.download_amazon_data(amazon_categories_to_download)
    integrator.download_movielens_data()
    integrator.process_movielens_data()
    
    print("Data processing finished. All data saved to Parquet files in ./data/processed/.")
    # Example of how to load data later:
    # electronics_reviews = pd.read_parquet(integrator.datasets['amazon']['Electronics']['reviews_path'])
    # movielens_ratings = dd.read_parquet(os.path.join('./data/processed/movielens/', 'ratings.parquet'))