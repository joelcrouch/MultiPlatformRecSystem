# raw_taste_based_clustering.py

import pandas as pd
from pymongo import MongoClient
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np

# --- 1. Connect to MongoDB ---
client = MongoClient('mongodb://localhost:27017/')
db = client['recsys_db']
reviews_collection = db['Clothing_Shoes_and_Jewelry']
meta_collection_name = 'meta_Clothing_Shoes_and_Jewelry'

print("✅ Connected to MongoDB.")

# --- 2. Define the Aggregation Pipeline for Taste Profile ---
# This pipeline performs the join, explode, and pivot operations on the server.
pipeline = [
    # Start with a sample of reviews to keep it manageable
    {'$sample': {'size': 100000}},
    
    # Join with metadata collection
    {
        '$lookup': {
            'from': meta_collection_name,
            'localField': 'parent_asin',
            'foreignField': 'parent_asin',
            'as': 'metadata'
        }
    },
    
    # Deconstruct the metadata array field from the lookup
    {'$unwind': '$metadata'},
    
    # Deconstruct the categories array field
    {'$unwind': '$metadata.categories'},
    
    # Group by user and category to count reviews in each category
    {
        '$group': {
            '_id': {
                'user_id': '$user_id',
                'category': '$metadata.categories'
            },
            'review_count': {'$sum': 1}
        }
    },
    
    # Pivot the data: group by user and create an array of category counts
    {
        '$group': {
            '_id': '$_id.user_id',
            'category_counts': {
                '$push': {
                    'k': '$_id.category',
                    'v': '$review_count'
                }
            }
        }
    },
    
    # Convert the array of k-v pairs into a document
    {
        '$project': {
            'user_id': '$_id',
            'taste_vector': {'$arrayToObject': '$category_counts'},
            '_id': 0
        }
    }
]

print("⏳ Running aggregation pipeline on MongoDB... This may take a few minutes.")
# --- 3. Execute the pipeline and create DataFrame ---
taste_profile_docs = list(reviews_collection.aggregate(pipeline, allowDiskUse=True))
print(f"✅ Aggregation complete. {len(taste_profile_docs)} user profiles retrieved.")

# Convert the list of documents into a DataFrame
# The 'taste_vector' column contains dictionaries that we can normalize
user_taste_list = []
for doc in taste_profile_docs:
    taste_vector = doc['taste_vector']
    taste_vector['user_id'] = doc['user_id']
    user_taste_list.append(taste_vector)

user_taste_df = pd.DataFrame(user_taste_list)

# Set user_id as index and fill NaNs with 0
user_taste_df.set_index('user_id', inplace=True)
user_taste_df.fillna(0, inplace=True)


print("✅ Successfully created the user taste profile DataFrame.")
print("\nUser Taste DataFrame Info:")
user_taste_df.info()
print("\nUser Taste DataFrame Head:")
print(user_taste_df.head())


# --- 4. Standardize and Cluster the Taste Profiles ---
if not user_taste_df.empty:
    print("\n⏳ Standardizing data and running KMeans clustering...")
    
    # Standardize the data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(user_taste_df)
    
    # Run KMeans
    k = 10  # We can tune this hyperparameter later
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    
    # Add cluster labels to the DataFrame
    user_taste_df['cluster'] = clusters
    
    print(f"✅ Assigned users to {k} clusters.")
    
    # --- 5. Inspect the results ---
    print("\n--- Cluster Sizes ---")
    print(user_taste_df['cluster'].value_counts())
    
    print("\n--- Sample of users with their cluster ---")
    print(user_taste_df.head())

else:
    print("Could not generate taste profiles. The aggregation returned no data.")
