import os
import pickle
import numpy as np
import scipy.sparse as sparse
from implicit.als import AlternatingLeastSquares

class ALSRecommender:
    """
    A recommender system using the Alternating Least Squares (ALS) algorithm
    from the 'implicit' library.
    """
    def __init__(self, factors=100, regularization=0.01, iterations=15, random_state=42):
        """
        Initializes the ALS recommender model.

        Args:
            factors (int): Number of latent factors to use.
            regularization (float): Regularization parameter for ALS.
            iterations (int): Number of ALS iterations to run.
            random_state (int): Random seed for reproducibility.
        """
        self.model = AlternatingLeastSquares(
            factors=factors,
            regularization=regularization,
            iterations=iterations,
            random_state=random_state
        )
        self.user_item_matrix = None # To store the matrix used for training

    def fit(self, user_item_matrix: sparse.csr_matrix):
        """
        Trains the ALS model on the given user-item interaction matrix.

        Args:
            user_item_matrix (sparse.csr_matrix): A sparse matrix where rows are users
                                                  and columns are items, containing
                                                  interaction strengths (e.g., counts).
        """
        print("Training ALS model...")
        self.user_item_matrix = user_item_matrix.T.tocsr() # ALS expects item-user matrix
        self.model.fit(self.user_item_matrix)
        print("ALS model training complete.")

    def recommend(self, user_id: int, user_items: sparse.csr_matrix, N: int = 10):
        """
        Generates top N recommendations for a given user.

        Args:
            user_id (int): The ID of the user for whom to generate recommendations.
            user_items (sparse.csr_matrix): A sparse row vector representing items
                                            the user has already interacted with.
                                            Used to filter out already seen items.
            N (int): The number of recommendations to generate.

        Returns:
            list: A list of (item_id, score) tuples for the top N recommendations.
        """
        # The recommend method expects the user_item_matrix used for training
        # to filter out already seen items.
        recommendations = self.model.recommend(
            user_id,
            self.user_item_matrix[user_id], # Pass the user's row from the item-user matrix
            N=N
        )
        return recommendations

    def save_model(self, path: str):
        """
        Saves the trained ALS model to a specified path.

        Args:
            path (str): The file path to save the model to (e.g., 'models/als_model.pkl').
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"ALS model saved to {path}")

    def load_model(self, path: str):
        """
        Loads a trained ALS model from a specified path.

        Args:
            path (str): The file path from which to load the model.
        """
        with open(path, 'rb') as f:
            self.model = pickle.load(f)
        print(f"ALS model loaded from {path}")
