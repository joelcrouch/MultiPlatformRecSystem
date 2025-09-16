# Multi-Platform Recommendation System Project
## "RecSys Intelligence: Cross-Domain Recommendation Engine"

### Project Overview
**Duration**: 12 weeks (6 two-week sprints)  
**Goal**: Build a sophisticated recommendation system that demonstrates all key ML engineering skills while solving real business problems across multiple domains.

**Core Innovation**: A unified recommendation framework that works across different domains (e-commerce, content, social) and can transfer learning between them.

---

## Why This Project Hits All Job Requirements

### ✅ AI/ML Expertise
- **Multiple ML Paradigms**: Collaborative filtering, deep learning, graph neural networks
- **Advanced Techniques**: Transformer-based models, multi-task learning, transfer learning
- **Frameworks**: TensorFlow, PyTorch, Hugging Face transformers
- **Real-world Complexity**: Cold start problem, scalability, fairness

### ✅ Infrastructure & MLOps  
- **Cloud Deployment**: AWS/GCP/Azure comparison for recommendation serving
- **Real-time Systems**: Stream processing for user interactions
- **Model Management**: A/B testing, model versioning, automated retraining
- **Monitoring**: Performance tracking, drift detection, business metrics

### ✅ Software Engineering
- **Full-Stack Application**: React frontend, Node.js/Python backend
- **Microservices**: Separate services for different recommendation types
- **APIs**: RESTful and GraphQL endpoints
- **Scalability**: Database optimization, caching strategies

### ✅ Data Fluency
- **Multi-Source Data**: User behavior, item metadata, social signals
- **ETL Pipelines**: Real-time and batch processing
- **Database Design**: Graph databases, time-series data, traditional RDBMS
- **Analytics**: User segmentation, recommendation quality metrics

### ✅ Communication & Strategy
- **Business Impact**: Clear ROI metrics (CTR, conversion, retention)
- **Executive Dashboards**: Real-time business intelligence
- **A/B Testing**: Statistical significance, business interpretation
- **Strategic Thinking**: Cross-domain insights, platform integration

---

## Public Datasets Used

### Primary Datasets
1. **Amazon Product Data** (2023 version) - 571GB of product reviews and metadata
   - User-item interactions: 233M reviews
   - Product metadata: 15M products
   - Categories: Electronics, Books, Clothing, Home & Garden

2. **MovieLens 25M Dataset** - Movie ratings and tags
   - 25M ratings from 162K users on 62K movies
   - Genome scores for 1,128 tags
   - Content-based features from IMDB

3. **Goodreads Book Reviews** - Book ratings and reviews
   - 3M book ratings from 876K users
   - Book metadata and genres
   - Author information and social connections

4. **Reddit Comments Dataset** - Social interactions
   - 1.7B comments from Reddit
   - User interaction patterns
   - Subreddit community data

### Synthetic Data Generation
- **Cross-domain user profiles**: Simulating users active across platforms
- **Temporal interaction patterns**: Realistic usage patterns
- **Cold start scenarios**: New users and items for testing

---

## Sprint Breakdown

### Sprint 1: Foundation & Data Pipeline (Weeks 1-2)
**Story Points**: 34

#### Epic: Data Infrastructure Setup

**User Story 1: Multi-Domain Dataset Integration (13 points)**
*As a data scientist, I want diverse recommendation datasets so I can train cross-domain models.*

**Implementation:**
```python
# data/dataset_integrator.py
import pandas as pd
import numpy as np
import boto3
from google.cloud import storage
from azure.storage.blob import BlobServiceClient
import sqlite3
from pymongo import MongoClient

class MultiDomainDatasetIntegrator:
    def __init__(self):
        self.datasets = {}
        self.unified_schema = self.create_unified_schema()
        
    def download_amazon_data(self):
        """Download and process Amazon review data"""
        # Using kaggle API or direct download
        import kaggle
        kaggle.api.dataset_download_files(
            'amazon-reviews-2023',
            path='./data/amazon/',
            unzip=True
        )
        
    def process_movielens_data(self):
        """Process MovieLens 25M dataset"""
        ratings = pd.read_csv('./data/ml-25m/ratings.csv')
        movies = pd.read_csv('./data/ml-25m/movies.csv')
        tags = pd.read_csv('./data/ml-25m/tags.csv')
        
        # Standardize to unified schema
        unified_ratings = ratings.rename(columns={
            'userId': 'user_id',
            'movieId': 'item_id',
            'rating': 'rating',
            'timestamp': 'timestamp'
        })
        unified_ratings['domain'] = 'movies'
        
        return unified_ratings, movies, tags
    
    def create_unified_schema(self):
        """Create unified interaction schema across domains"""
        return {
            'user_id': 'int64',
            'item_id': 'int64', 
            'rating': 'float32',
            'timestamp': 'int64',
            'domain': 'string',
            'interaction_type': 'string',  # view, purchase, rate, share
            'context': 'string'  # device, location, etc.
        }
```

**User Story 2: Real-time Data Pipeline (13 points)**
*As a ML engineer, I want real-time user interaction processing so recommendations stay current.*

```python
# pipelines/streaming_pipeline.py
from kafka import KafkaConsumer, KafkaProducer
import json
import pandas as pd
from datetime import datetime
import asyncio
import aioredis

class RealtimeRecommendationPipeline:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'user_interactions',
            bootstrap_servers=['localhost:9092'],
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
    async def process_interaction_stream(self):
        """Process real-time interactions and update recommendations"""
        redis = await aioredis.from_url("redis://localhost")
        
        for message in self.consumer:
            interaction = message.value
            
            # Update user profile in real-time
            await self.update_user_profile(redis, interaction)
            
            # Trigger incremental model update if needed
            if self.should_trigger_update(interaction):
                await self.trigger_model_update(interaction)
```

**User Story 3: Multi-Database Feature Store (8 points)**
*As a ML engineer, I want features stored across SQL/NoSQL systems for different use cases.*

```python
# features/multi_db_feature_store.py
import sqlite3
from pymongo import MongoClient
import redis
import neo4j
from sqlalchemy import create_engine
import pandas as pd

class MultiDatabaseFeatureStore:
    def __init__(self):
        # SQL for structured features
        self.postgres_engine = create_engine('postgresql://user:pass@localhost/recsys')
        
        # NoSQL for flexible user profiles
        self.mongo_client = MongoClient('mongodb://localhost:27017/')
        self.mongo_db = self.mongo_client.recsys
        
        # Redis for real-time features
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        
        # Neo4j for graph features
        self.neo4j_driver = neo4j.GraphDatabase.driver(
            "neo4j://localhost:7687", 
            auth=("neo4j", "password")
        )
    
    def store_user_features_sql(self, user_features_df: pd.DataFrame):
        """Store structured user features in PostgreSQL"""
        user_features_df.to_sql(
            'user_features', 
            self.postgres_engine, 
            if_exists='replace',
            index=False
        )
    
    def store_user_profile_nosql(self, user_id: int, profile: dict):
        """Store flexible user profile in MongoDB"""
        self.mongo_db.user_profiles.update_one(
            {'user_id': user_id},
            {'$set': profile},
            upsert=True
        )
    
    def store_realtime_features_redis(self, user_id: int, features: dict):
        """Store real-time features in Redis with TTL"""
        self.redis_client.hset(f"user:{user_id}", mapping=features)
        self.redis_client.expire(f"user:{user_id}", 3600)  # 1 hour TTL
```

### Sprint 2: Model Development & Framework Comparison (Weeks 3-4)  
**Story Points**: 42

#### Epic: Multi-Framework Model Implementation

**User Story 4: Hugging Face Transformer Models (14 points)**
*As a ML engineer, I want to leverage pre-trained transformers for content-based recommendations.*

```python
# models/huggingface_models.py
from transformers import (
    AutoTokenizer, AutoModel, Trainer, TrainingArguments,
    BertModel, BertTokenizer, T5ForConditionalGeneration
)
import torch
import torch.nn as nn

class TransformerRecommender(nn.Module):
    def __init__(self, model_name: str = 'bert-base-uncased'):
        super().__init__()
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.transformer = AutoModel.from_pretrained(model_name)
        
        # Recommendation head
        self.recommendation_head = nn.Sequential(
            nn.Linear(self.transformer.config.hidden_size * 2, 512),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(512, 128),
            nn.ReLU(),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )
        
    def forward(self, user_text, item_text):
        # Encode user preferences and item descriptions
        user_encoding = self.transformer(**user_text).last_hidden_state[:, 0]  # CLS token
        item_encoding = self.transformer(**item_text).last_hidden_state[:, 0]
        
        # Concatenate and predict
        combined = torch.cat([user_encoding, item_encoding], dim=1)
        return self.recommendation_head(combined)

class GenerativeRecommender:
    def __init__(self):
        self.model = T5ForConditionalGeneration.from_pretrained('t5-base')
        self.tokenizer = AutoTokenizer.from_pretrained('t5-base')
        
    def generate_recommendations(self, user_history: str, num_recommendations: int = 5):
        """Generate recommendations using T5"""
        prompt = f"Recommend items for user who likes: {user_history}"
        
        inputs = self.tokenizer(prompt, return_tensors='pt', max_length=512, truncation=True)
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs.input_ids,
                max_length=100,
                num_return_sequences=num_recommendations,
                temperature=0.7,
                do_sample=True
            )
            
        recommendations = [
            self.tokenizer.decode(output, skip_special_tokens=True) 
            for output in outputs
        ]
        
        return recommendations
```

**User Story 5: PyTorch Deep Learning Models (14 points)**
*As a ML engineer, I want custom PyTorch architectures for specialized recommendation tasks.*

```python
# models/pytorch_models.py
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import pytorch_lightning as pl

class NeuralCollaborativeFiltering(pl.LightningModule):
    def __init__(self, n_users, n_items, embedding_dim=128, hidden_dims=[256, 128, 64]):
        super().__init__()
        
        # Embeddings
        self.user_embedding = nn.Embedding(n_users, embedding_dim)
        self.item_embedding = nn.Embedding(n_items, embedding_dim)
        
        # MLP layers
        layers = []
        input_dim = embedding_dim * 2
        
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(input_dim, hidden_dim),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.BatchNorm1d(hidden_dim)
            ])
            input_dim = hidden_dim
            
        layers.append(nn.Linear(hidden_dims[-1], 1))
        self.mlp = nn.Sequential(*layers)
        
    def forward(self, user_ids, item_ids):
        user_emb = self.user_embedding(user_ids)
        item_emb = self.item_embedding(item_ids)
        
        x = torch.cat([user_emb, item_emb], dim=-1)
        return torch.sigmoid(self.mlp(x))
    
    def training_step(self, batch, batch_idx):
        user_ids, item_ids, ratings = batch
        predictions = self(user_ids, item_ids)
        loss = F.binary_cross_entropy(predictions.squeeze(), ratings.float())
        
        self.log('train_loss', loss)
        return loss
    
    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.001)

class VariationalAutoEncoder(pl.LightningModule):
    def __init__(self, input_dim, latent_dim=200):
        super().__init__()
        self.latent_dim = latent_dim
        
        # Encoder
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 600),
            nn.Tanh(),
            nn.Linear(600, 400),
            nn.Tanh()
        )
        
        self.fc_mu = nn.Linear(400, latent_dim)
        self.fc_var = nn.Linear(400, latent_dim)
        
        # Decoder
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 400),
            nn.Tanh(),
            nn.Linear(400, 600),
            nn.Tanh(),
            nn.Linear(600, input_dim),
            nn.Sigmoid()
        )
        
    def encode(self, x):
        h = self.encoder(x)
        return self.fc_mu(h), self.fc_var(h)
    
    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std
    
    def decode(self, z):
        return self.decoder(z)
    
    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        return self.decode(z), mu, logvar
```

**User Story 6: TensorFlow/Keras Models (14 points)**
*As a ML engineer, I want TensorFlow models for production deployment and comparison.*

```python
# models/tensorflow_models.py
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow_recommenders as tfrs

class TensorFlowRecommender(tfrs.Model):
    def __init__(self, vocabulary, embedding_dimension=64):
        super().__init__()
        
        # User and item vocabularies
        self.user_vocab = vocabulary['users']
        self.item_vocab = vocabulary['items']
        
        # Embedding layers
        self.user_embedding = keras.Sequential([
            keras.utils.StringLookup(vocabulary=self.user_vocab, mask_token=None),
            layers.Embedding(len(self.user_vocab) + 1, embedding_dimension)
        ])
        
        self.item_embedding = keras.Sequential([
            keras.utils.StringLookup(vocabulary=self.item_vocab, mask_token=None),
            layers.Embedding(len(self.item_vocab) + 1, embedding_dimension)
        ])
        
        # Prediction model
        self.rating_model = keras.Sequential([
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(128, activation='relu'),
            layers.Dense(64, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        
        # Tasks
        self.rating_task = tfrs.tasks.Ranking(
            loss=keras.losses.MeanSquaredError(),
            metrics=[keras.metrics.RootMeanSquaredError()]
        )
        
    def call(self, features):
        user_embeddings = self.user_embedding(features['user_id'])
        item_embeddings = self.item_embedding(features['item_id'])
        
        concatenated = tf.concat([user_embeddings, item_embeddings], axis=1)
        return self.rating_model(concatenated)
    
    def compute_loss(self, features, training=False):
        user_embeddings = self.user_embedding(features['user_id'])
        item_embeddings = self.item_embedding(features['item_id'])
        
        predictions = self.rating_model(
            tf.concat([user_embeddings, item_embeddings], axis=1)
        )
        
        return self.rating_task(
            labels=features['rating'],
            predictions=predictions
        )

class WideAndDeepModel(keras.Model):
    def __init__(self, wide_columns, deep_columns, num_classes=1):
        super().__init__()
        
        # Wide component (linear model)
        self.wide_model = layers.Dense(num_classes, activation='sigmoid')
        
        # Deep component (neural network)
        self.deep_model = keras.Sequential([
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu'),
            layers.Dense(num_classes, activation='sigmoid')
        ])
        
    def call(self, inputs):
        wide_features, deep_features = inputs
        
        wide_output = self.wide_model(wide_features)
        deep_output = self.deep_model(deep_features)
        
        # Combine wide and deep
        combined = (wide_output + deep_output) / 2.0
        return combined
```

### Sprint 3: Multi-Cloud Infrastructure Comparison (Weeks 5-6)
**Story Points**: 38

#### Epic: Cloud Platform Deployment & Comparison

**User Story 7: AWS Infrastructure & SageMaker (13 points)**

```python
# infrastructure/aws/sagemaker_deployment.py
import boto3
import sagemaker
from sagemaker.pytorch import PyTorchModel
from sagemaker.tensorflow import TensorFlowModel
import json

class AWSRecommenderDeployment:
    def __init__(self, region='us-west-2'):
        self.session = sagemaker.Session()
        self.role = sagemaker.get_execution_role()
        self.region = region
        
    def deploy_pytorch_model(self, model_data_s3_path, instance_type='ml.m5.large'):
        """Deploy PyTorch recommendation model to SageMaker"""
        pytorch_model = PyTorchModel(
            model_data=model_data_s3_path,
            role=self.role,
            entry_point='inference.py',
            framework_version='1.12',
            py_version='py39',
            source_dir='code/'
        )
        
        predictor = pytorch_model.deploy(
            initial_instance_count=1,
            instance_type=instance_type,
            endpoint_name='pytorch-recommender-endpoint'
        )
        
        return predictor
    
    def deploy_tensorflow_model(self, model_data_s3_path):
        """Deploy TensorFlow model to SageMaker"""
        tensorflow_model = TensorFlowModel(
            model_data=model_data_s3_path,
            role=self.role,
            entry_point='tf_inference.py',
            framework_version='2.11',
            source_dir='code/'
        )
        
        predictor = tensorflow_model.deploy(
            initial_instance_count=1,
            instance_type='ml.m5.large',
            endpoint_name='tensorflow-recommender-endpoint'
        )
        
        return predictor
    
    def setup_batch_transform(self, model_name, transform_job_name):
        """Setup batch inference for large-scale recommendations"""
        transformer = sagemaker.transformer.Transformer(
            model_name=model_name,
            instance_count=1,
            instance_type='ml.m5.large',
            output_path='s3://your-bucket/batch-output/'
        )
        
        transformer.transform(
            data='s3://your-bucket/batch-input/',
            data_type='S3Prefix',
            content_type='text/csv',
            split_type='Line',
            job_name=transform_job_name
        )
        
        return transformer
```

**User Story 8: GCP Infrastructure & Vertex AI (12 points)**

```python
# infrastructure/gcp/vertex_ai_deployment.py
from google.cloud import aiplatform
from google.cloud.aiplatform import Model, Endpoint
import os

class GCPRecommenderDeployment:
    def __init__(self, project_id, region='us-central1'):
        aiplatform.init(project=project_id, location=region)
        self.project_id = project_id
        self.region = region
        
    def deploy_custom_model(self, display_name, container_uri, model_uri):
        """Deploy custom recommendation model to Vertex AI"""
        
        # Upload model
        model = Model.upload(
            display_name=display_name,
            artifact_uri=model_uri,
            serving_container_image_uri=container_uri,
            serving_container_predict_route="/predict",
            serving_container_health_route="/health"
        )
        
        # Create endpoint
        endpoint = Endpoint.create(
            display_name=f"{display_name}-endpoint"
        )
        
        # Deploy model to endpoint
        model.deploy(
            endpoint=endpoint,
            machine_type="n1-standard-2",
            min_replica_count=1,
            max_replica_count=3,
            traffic_percentage=100
        )
        
        return model, endpoint
    
    def setup_batch_prediction(self, model, input_uri, output_uri):
        """Setup batch prediction job"""
        batch_prediction_job = model.batch_predict(
            job_display_name="recommendation-batch-prediction",
            gcs_source=input_uri,
            gcs_destination_prefix=output_uri,
            machine_type="n1-standard-4",
            starting_replica_count=1,
            max_replica_count=5
        )
        
        return batch_prediction_job
```

**User Story 9: Azure ML Infrastructure (13 points)**

```python
# infrastructure/azure/azure_ml_deployment.py
from azureml.core import Workspace, Environment, Model
from azureml.core.webservice import AciWebservice, Webservice
from azureml.core.model import InferenceConfig
import os

class AzureRecommenderDeployment:
    def __init__(self, subscription_id, resource_group, workspace_name):
        self.ws = Workspace(subscription_id, resource_group, workspace_name)
        
    def deploy_pytorch_model(self, model_name, model_version=1):
        """Deploy PyTorch model to Azure Container Instance"""
        
        # Get registered model
        model = Model(self.ws, name=model_name, version=model_version)
        
        # Define environment
        env = Environment.from_conda_specification(
            name="pytorch-env",
            file_path="conda_env.yml"
        )
        
        # Inference configuration
        inference_config = InferenceConfig(
            entry_script="score.py",
            environment=env
        )
        
        # Deployment configuration
        deployment_config = AciWebservice.deploy_configuration(
            cpu_cores=2,
            memory_gb=4,
            description="PyTorch Recommender Service"
        )
        
        # Deploy
        service = Model.deploy(
            workspace=self.ws,
            name="pytorch-recommender-service",
            models=[model],
            inference_config=inference_config,
            deployment_config=deployment_config
        )
        
        service.wait_for_deployment(show_output=True)
        return service
```

### Sprint 4: MLOps & Experiment Management (Weeks 7-8)
**Story Points**: 36

#### Epic: Production ML Pipeline

**User Story 10: MLflow Experiment Tracking (15 points)**

```python
# mlops/experiment_tracking.py
import mlflow
import mlflow.pytorch
import mlflow.tensorflow
from mlflow.tracking import MlflowClient
import wandb

class ComprehensiveExperimentTracker:
    def __init__(self):
        # MLflow setup
        mlflow.set_tracking_uri("http://localhost:5000")
        self.mlflow_client = MlflowClient()
        
        # Weights & Biases setup
        wandb.init(project="recommendation-system")
        
    def track_model_comparison(self, models_results):
        """Track multiple models and frameworks"""
        
        with mlflow.start_run(run_name="model_comparison") as run:
            for model_name, results in models_results.items():
                # Log metrics
                mlflow.log_metrics({
                    f"{model_name}_precision": results['precision'],
                    f"{model_name}_recall": results['recall'],
                    f"{model_name}_ndcg": results['ndcg'],
                    f"{model_name}_training_time": results['training_time'],
                    f"{model_name}_inference_latency": results['inference_latency']
                })
                
                # Log model artifacts
                if 'pytorch' in model_name:
                    mlflow.pytorch.log_model(results['model'], f"{model_name}_model")
                elif 'tensorflow' in model_name:
                    mlflow.tensorflow.log_model(results['model'], f"{model_name}_model")
                
                # Also log to W&B
                wandb.log({
                    f"{model_name}_metrics": results
                })
    
    def track_cloud_deployment_metrics(self, cloud_provider, metrics):
        """Track deployment performance across cloud providers"""
        
        with mlflow.start_run(run_name=f"{cloud_provider}_deployment") as run:
            mlflow.log_params({
                "cloud_provider": cloud_provider,
                "deployment_date": datetime.now().isoformat()
            })
            
            mlflow.log_metrics(metrics)
```

**User Story 11: A/B Testing Framework (11 points)**

```python
# testing/ab_testing.py
import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple

class RecommendationABTesting:
    def __init__(self):
        self.experiments = {}
        
    def create_experiment(self, experiment_name: str, variants: List[str], 
                         traffic_split: List[float]):
        """Create new A/B test experiment"""
        
        self.experiments[experiment_name] = {
            'variants': variants,
            'traffic_split': traffic_split,
            'results': {variant: [] for variant in variants},
            'start_time': datetime.now(),
            'status': 'running'
        }
        
    def assign_user_to_variant(self, experiment_name: str, user_id: int) -> str:
        """Assign user to experiment variant"""
        experiment = self.experiments[experiment_name]
        
        # Consistent assignment based on user_id hash
        hash_value = hash(f"{experiment_name}_{user_id}") % 100
        
        cumulative_split = np.cumsum(experiment['traffic_split']) * 100
        
        for i, threshold in enumerate(cumulative_split):
            if hash_value < threshold:
                return experiment['variants'][i]
                
        return experiment['variants'][-1]
    
    def log_conversion(self, experiment_name: str, user_id: int, 
                      converted: bool, metric_value: float = None):
        """Log conversion event for A/B test"""
        variant = self.assign_user_to_variant(experiment_name, user_id)
        
        self.experiments[experiment_name]['results'][variant].append({
            'user_id': user_id,
            'converted': converted,
            'metric_value': metric_value,
            'timestamp': datetime.now()
        })
        
    def analyze_experiment(self, experiment_name: str) -> Dict:
        """Analyze A/B test results"""
        experiment = self.experiments[experiment_name]
        results = {}
        
        for variant in experiment['variants']:
            data = experiment['results'][variant]
            
            if len(data) == 0:
                continue
                
            conversions = [d['converted'] for d in data]
            metric_values = [d['metric_value'] for d in data if d['metric_value']]
            
            results[variant] = {
                'sample_size': len(data),
                'conversion_rate': np.mean(conversions),
                'avg_metric_value': np.mean(metric_values) if metric_values else 0,
                'confidence_interval': stats.binom.interval(0.95, len(data), np.mean(conversions))
            }
            
        return results
```

**User Story 12: Model Monitoring & Drift Detection (10 points)**

```python
# monitoring/model_monitoring.py
import numpy as np
from scipy import stats
from sklearn.metrics import mean_squared_error
import pandas as pd

class ModelDriftMonitor:
    def __init__(self, reference_data: pd.DataFrame):
        self.reference_data = reference_data
        self.feature_stats = self.compute_reference_stats()
        
    def detect_data_drift(self, new_data: pd.DataFrame, threshold: float = 0.05) -> Dict:
        """Detect data drift using statistical tests"""
        
        drift_results = {}
        
        for column in self.reference_data.select_dtypes(include=[np.number]).columns:
            if column in new_data.columns:
                # KS test for continuous variables
                ks_statistic, p_value = stats.ks_2samp(
                    self.reference_data[column], 
                    new_data[column]
                )
                
                drift_results[column] = {
                    'ks_statistic': ks_statistic,
                    'p_value': p_value,
                    'drift_detected': p_value < threshold,
                    'severity': self.categorize_drift(ks_statistic)
                }
                
        return drift_results
    
    def detect_concept_drift(self, predictions: np.array, 
                           actual: np.array, window_size: int = 1000) -> Dict:
        """Detect concept drift using performance degradation"""
        
        current_mse = mean_squared_error(actual[-window_size:], predictions[-window_size:])
        reference_mse = self.feature_stats.get('reference_mse', current_mse)
        
        drift_ratio = current_mse / reference_mse
        
        return {
            'current_mse': current_mse,
            'reference_mse': reference_mse,
            'drift_ratio': drift_ratio,
            'concept_drift_detected': drift_ratio > 1.2,  # 20% degradation threshold
            'severity': 'high' if drift_ratio > 1.5 else 'medium' if drift_ratio > 1.2 else 'low'
        }
    
    def categorize_drift(self, ks_statistic: float) -> str:
        """Categorize drift severity"""
        if ks_statistic > 0.3:
            return 'high'
        elif ks_statistic > 0.1:
            return 'medium'
        else:
            return 'low'
```

### Sprint 5: Advanced Analytics & Business Intelligence (Weeks 9-10)
**Story Points**: 34

#### Epic: Business Intelligence Dashboard

**User Story 13: Executive Dashboard Development (12 points)**
*As an executive, I want real-time business metrics so I can make data-driven decisions about the recommendation system.*

```python
# dashboard/executive_dashboard.py
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

class ExecutiveDashboard:
    def __init__(self):
        self.setup_dashboard()
        
    def setup_dashboard(self):
        st.set_page_config(
            page_title="RecSys Intelligence Dashboard",
            page_icon="📊",
            layout="wide"
        )
        
    def display_kpi_metrics(self, metrics: Dict):
        """Display key business metrics"""
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Click-Through Rate",
                value=f"{metrics['ctr']:.2%}",
                delta=f"{metrics['ctr_change']:+.2%}"
            )
            
        with col2:
            st.metric(
                label="Conversion Rate", 
                value=f"{metrics['conversion_rate']:.2%}",
                delta=f"{metrics['conversion_change']:+.2%}"
            )
            
        with col3:
            st.metric(
                label="Revenue Impact",
                value=f"${metrics['revenue_impact']:,.0f}",
                delta=f"${metrics['revenue_change']:+,.0f}"
            )
            
        with col4:
            st.metric(
                label="User Engagement",
                value=f"{metrics['engagement_score']:.1f}",
                delta=f"{metrics['engagement_change']:+.1f}"
            )
    
    def display_model_performance_comparison(self, performance_data: pd.DataFrame):
        """Compare model performance across frameworks and cloud providers"""
        
        # Framework comparison
        fig_framework = px.bar(
            performance_data,
            x='framework',
            y='ndcg_score',
            color='model_type',
            title='Model Performance by Framework',
            labels={'ndcg_score': 'NDCG@10 Score'}
        )
        
        st.plotly_chart(fig_framework, use_container_width=True)
        
        # Cloud provider comparison
        fig_cloud = px.scatter(
            performance_data,
            x='latency_ms',
            y='throughput_rps',
            color='cloud_provider',
            size='cost_per_1k_requests',
            title='Cloud Provider Performance vs Cost',
            labels={
                'latency_ms': 'Latency (ms)',
                'throughput_rps': 'Throughput (requests/sec)'
            }
        )
        
        st.plotly_chart(fig_cloud, use_container_width=True)
    
    def display_ab_test_results(self, ab_results: Dict):
        """Display A/B testing results"""
        
        st.subheader("A/B Test Results")
        
        for experiment_name, results in ab_results.items():
            st.write(f"**{experiment_name}**")
            
            variants_df = pd.DataFrame(results).T
            
            fig = px.bar(
                variants_df,
                x=variants_df.index,
                y='conversion_rate',
                title=f'{experiment_name} - Conversion Rates',
                error_y='confidence_interval'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistical significance
            if len(variants_df) == 2:
                p_value = self.calculate_significance(variants_df)
                
                if p_value < 0.05:
                    st.success(f"✅ Statistically significant result (p={p_value:.4f})")
                else:
                    st.warning(f"⚠️ Not statistically significant (p={p_value:.4f})")
    
    def display_business_impact_analysis(self, impact_data: Dict):
        """Show business impact analysis"""
        
        st.subheader("Business Impact Analysis")
        
        # Revenue attribution
        col1, col2 = st.columns(2)
        
        with col1:
            # Revenue by domain
            revenue_by_domain = px.pie(
                values=list(impact_data['revenue_by_domain'].values()),
                names=list(impact_data['revenue_by_domain'].keys()),
                title="Revenue Attribution by Domain"
            )
            st.plotly_chart(revenue_by_domain)
            
        with col2:
            # User lifetime value impact
            ltv_data = impact_data['ltv_analysis']
            
            fig_ltv = go.Figure()
            fig_ltv.add_trace(go.Bar(
                name='Before Recommendations',
                x=ltv_data['user_segments'],
                y=ltv_data['ltv_before']
            ))
            fig_ltv.add_trace(go.Bar(
                name='After Recommendations',
                x=ltv_data['user_segments'],
                y=ltv_data['ltv_after']
            ))
            
            fig_ltv.update_layout(
                title='User Lifetime Value Impact',
                xaxis_title='User Segments',
                yaxis_title='LTV ($)',
                barmode='group'
            )
            
            st.plotly_chart(fig_ltv)
```

**User Story 14: Advanced Analytics Pipeline (12 points)**
*As a data analyst, I want sophisticated analytics to understand user behavior and recommendation effectiveness.*

```python
# analytics/advanced_analytics.py
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import networkx as nx
from lifetimes import BetaGeoFitter, GammaGammaFitter

class AdvancedRecommendationAnalytics:
    def __init__(self):
        self.user_segments = {}
        self.cohort_analysis = {}
        
    def perform_user_segmentation(self, user_data: pd.DataFrame) -> Dict:
        """Segment users based on behavior patterns"""
        
        # Feature engineering for segmentation
        features = self.create_segmentation_features(user_data)
        
        # K-means clustering
        kmeans = KMeans(n_clusters=5, random_state=42)
        user_data['segment'] = kmeans.fit_predict(features)
        
        # Analyze segments
        segment_profiles = {}
        for segment in range(5):
            segment_users = user_data[user_data['segment'] == segment]
            
            segment_profiles[f'segment_{segment}'] = {
                'size': len(segment_users),
                'avg_lifetime_value': segment_users['lifetime_value'].mean(),
                'avg_engagement': segment_users['engagement_score'].mean(),
                'top_categories': segment_users['preferred_categories'].value_counts().head(3).to_dict(),
                'recommendation_response_rate': segment_users['rec_click_rate'].mean()
            }
            
        return segment_profiles
    
    def cohort_analysis(self, interaction_data: pd.DataFrame) -> pd.DataFrame:
        """Perform cohort analysis to understand user retention"""
        
        # Define cohorts by first interaction month
        interaction_data['order_period'] = interaction_data['timestamp'].dt.to_period('M')
        interaction_data['cohort_group'] = interaction_data.groupby('user_id')['timestamp'].transform('min').dt.to_period('M')
        
        # Calculate period number
        interaction_data['period_number'] = (interaction_data['order_period'] - interaction_data['cohort_group']).apply(attrgetter('n'))
        
        # Create cohort table
        cohort_data = interaction_data.groupby(['cohort_group', 'period_number'])['user_id'].nunique().reset_index()
        cohort_counts = cohort_data.pivot(index='cohort_group', columns='period_number', values='user_id')
        
        # Calculate cohort sizes
        cohort_sizes = interaction_data.groupby('cohort_group')['user_id'].nunique()
        cohort_table = cohort_counts.divide(cohort_sizes, axis=0)
        
        return cohort_table
    
    def recommendation_effectiveness_analysis(self, rec_data: pd.DataFrame) -> Dict:
        """Analyze recommendation system effectiveness"""
        
        analysis_results = {}
        
        # Diversity analysis
        analysis_results['diversity'] = self.calculate_recommendation_diversity(rec_data)
        
        # Novelty analysis
        analysis_results['novelty'] = self.calculate_recommendation_novelty(rec_data)
        
        # Serendipity analysis
        analysis_results['serendipity'] = self.calculate_serendipity(rec_data)
        
        # Coverage analysis
        analysis_results['coverage'] = self.calculate_catalog_coverage(rec_data)
        
        return analysis_results
    
    def customer_lifetime_value_prediction(self, transaction_data: pd.DataFrame) -> pd.DataFrame:
        """Predict customer lifetime value using BG/NBD and Gamma-Gamma models"""
        
        # Prepare data for RFM analysis
        summary_data = self.create_rfm_summary(transaction_data)
        
        # Fit BG/NBD model for purchase frequency
        bgf = BetaGeoFitter(penalizer_coef=0.0)
        bgf.fit(summary_data['frequency'], summary_data['recency'], summary_data['T'])
        
        # Predict future purchases
        summary_data['predicted_purchases'] = bgf.conditional_expected_number_of_purchases_up_to_time(
            90, summary_data['frequency'], summary_data['recency'], summary_data['T']
        )
        
        # Fit Gamma-Gamma model for monetary value
        returning_customers = summary_data[summary_data['frequency'] > 0]
        
        ggf = GammaGammaFitter(penalizer_coef=0.0)
        ggf.fit(returning_customers['frequency'], returning_customers['monetary_value'])
        
        # Predict CLV
        summary_data['predicted_clv'] = ggf.customer_lifetime_value(
            bgf,
            summary_data['frequency'],
            summary_data['recency'],
            summary_data['T'],
            summary_data['monetary_value'],
            time=90,  # 90 days
            discount_rate=0.01  # monthly discount rate
        )
        
        return summary_data
    
    def network_analysis(self, user_item_data: pd.DataFrame) -> Dict:
        """Analyze user-item network for community detection and influence"""
        
        # Create bipartite graph
        G = nx.Graph()
        
        # Add nodes
        users = user_item_data['user_id'].unique()
        items = user_item_data['item_id'].unique()
        
        G.add_nodes_from(users, bipartite=0)
        G.add_nodes_from(items, bipartite=1)
        
        # Add edges
        edges = [(row['user_id'], row['item_id'], {'weight': row['rating']}) 
                for _, row in user_item_data.iterrows()]
        G.add_edges_from(edges)
        
        # Network analysis
        analysis = {
            'network_density': nx.density(G),
            'clustering_coefficient': nx.average_clustering(G),
            'connected_components': nx.number_connected_components(G),
            'diameter': nx.diameter(G) if nx.is_connected(G) else None
        }
        
        # Community detection
        communities = nx.community.greedy_modularity_communities(G)
        analysis['communities'] = len(communities)
        
        # Centrality measures
        degree_centrality = nx.degree_centrality(G)
        betweenness_centrality = nx.betweenness_centrality(G, k=1000)  # Sample for large graphs
        
        analysis['top_influential_users'] = sorted(
            [(node, centrality) for node, centrality in degree_centrality.items() if node in users],
            key=lambda x: x[1], reverse=True
        )[:10]
        
        return analysis
```

**User Story 15: Cross-Domain Transfer Learning Analysis (10 points)**
*As a research scientist, I want to analyze how knowledge transfers between domains.*

```python
# analytics/transfer_learning_analysis.py
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity

class TransferLearningAnalyzer:
    def __init__(self):
        self.domain_embeddings = {}
        self.transfer_matrices = {}
        
    def analyze_embedding_similarity(self, embeddings_by_domain: Dict) -> Dict:
        """Analyze similarity between domain embeddings"""
        
        similarity_analysis = {}
        
        domains = list(embeddings_by_domain.keys())
        
        for i, domain1 in enumerate(domains):
            for domain2 in domains[i+1:]:
                # Calculate cosine similarity between domain embeddings
                sim_matrix = cosine_similarity(
                    embeddings_by_domain[domain1],
                    embeddings_by_domain[domain2]
                )
                
                similarity_analysis[f"{domain1}_to_{domain2}"] = {
                    'mean_similarity': np.mean(sim_matrix),
                    'max_similarity': np.max(sim_matrix),
                    'similarity_distribution': np.histogram(sim_matrix.flatten(), bins=50)
                }
                
        return similarity_analysis
    
    def visualize_domain_embeddings(self, embeddings_by_domain: Dict):
        """Create t-SNE visualization of domain embeddings"""
        
        # Combine all embeddings
        all_embeddings = []
        domain_labels = []
        
        for domain, embeddings in embeddings_by_domain.items():
            all_embeddings.extend(embeddings)
            domain_labels.extend([domain] * len(embeddings))
            
        all_embeddings = np.array(all_embeddings)
        
        # Apply t-SNE
        tsne = TSNE(n_components=2, random_state=42, perplexity=30)
        embeddings_2d = tsne.fit_transform(all_embeddings)
        
        # Create visualization
        plt.figure(figsize=(12, 8))
        
        unique_domains = list(set(domain_labels))
        colors = plt.cm.Set3(np.linspace(0, 1, len(unique_domains)))
        
        for domain, color in zip(unique_domains, colors):
            mask = np.array(domain_labels) == domain
            plt.scatter(
                embeddings_2d[mask, 0],
                embeddings_2d[mask, 1],
                c=[color],
                label=domain,
                alpha=0.6
            )
            
        plt.legend()
        plt.title('Domain Embeddings Visualization (t-SNE)')
        plt.xlabel('t-SNE 1')
        plt.ylabel('t-SNE 2')
        plt.grid(True, alpha=0.3)
        
        return plt.gcf()
    
    def measure_transfer_effectiveness(self, 
                                    source_performance: Dict,
                                    target_performance: Dict,
                                    transfer_performance: Dict) -> Dict:
        """Measure effectiveness of transfer learning"""
        
        transfer_metrics = {}
        
        for domain in target_performance.keys():
            if domain in transfer_performance and domain in source_performance:
                
                baseline_score = target_performance[domain]['ndcg']
                transfer_score = transfer_performance[domain]['ndcg']
                source_score = source_performance.get('source_domain', {}).get('ndcg', 0)
                
                # Transfer effectiveness ratio
                transfer_effectiveness = (transfer_score - baseline_score) / baseline_score
                
                # Knowledge retention from source
                if source_score > 0:
                    knowledge_retention = transfer_score / source_score
                else:
                    knowledge_retention = 0
                
                transfer_metrics[domain] = {
                    'transfer_effectiveness': transfer_effectiveness,
                    'knowledge_retention': knowledge_retention,
                    'absolute_improvement': transfer_score - baseline_score,
                    'baseline_score': baseline_score,
                    'transfer_score': transfer_score
                }
                
        return transfer_metrics
```

### Sprint 6: Production Optimization & Final Integration (Weeks 11-12)
**Story Points**: 40

#### Epic: Production Readiness & Performance Optimization

**User Story 16: Performance Optimization & Caching (15 points)**
*As a systems engineer, I want optimized recommendation serving with intelligent caching.*

```python
# optimization/recommendation_cache.py
import redis
import pickle
import hashlib
from typing import List, Dict, Optional
import asyncio
import aioredis
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class CacheConfig:
    redis_url: str = "redis://localhost:6379"
    default_ttl: int = 3600  # 1 hour
    max_cache_size: int = 1000000  # 1M entries
    eviction_policy: str = "LRU"

class IntelligentRecommendationCache:
    def __init__(self, config: CacheConfig):
        self.config = config
        self.redis_client = redis.from_url(config.redis_url)
        
    async def get_recommendations(self, user_id: int, context: Dict) -> Optional[List[Dict]]:
        """Get cached recommendations with context awareness"""
        
        cache_key = self.generate_cache_key(user_id, context)
        
        try:
            cached_data = await self.redis_client.get(cache_key)
            if cached_data:
                recommendations = pickle.loads(cached_data)
                
                # Check if cache is still valid based on user activity
                if self.is_cache_valid(user_id, recommendations['timestamp']):
                    return recommendations['items']
                    
        except Exception as e:
            print(f"Cache retrieval error: {e}")
            
        return None
    
    async def cache_recommendations(self, user_id: int, context: Dict, 
                                  recommendations: List[Dict], ttl: Optional[int] = None):
        """Cache recommendations with intelligent TTL"""
        
        cache_key = self.generate_cache_key(user_id, context)
        ttl = ttl or self.calculate_adaptive_ttl(user_id, context)
        
        cache_data = {
            'items': recommendations,
            'timestamp': datetime.utcnow(),
            'user_id': user_id,
            'context': context
        }
        
        try:
            serialized_data = pickle.dumps(cache_data)
            await self.redis_client.setex(cache_key, ttl, serialized_data)
            
            # Update cache statistics
            await self.update_cache_stats(user_id, 'cache_write')
            
        except Exception as e:
            print(f"Cache storage error: {e}")
    
    def generate_cache_key(self, user_id: int, context: Dict) -> str:
        """Generate cache key based on user and context"""
        
        # Include relevant context factors
        context_str = f"{context.get('device', 'web')}_{context.get('location', 'unknown')}_{context.get('time_of_day', 'unknown')}"
        
        key_components = f"rec:{user_id}:{context_str}"
        
        # Hash for consistent key length
        return hashlib.md5(key_components.encode()).hexdigest()
    
    def calculate_adaptive_ttl(self, user_id: int, context: Dict) -> int:
        """Calculate adaptive TTL based on user behavior patterns"""
        
        # Get user activity level
        user_activity = self.get_user_activity_level(user_id)
        
        base_ttl = self.config.default_ttl
        
        # High activity users need fresher recommendations
        if user_activity == 'high':
            return base_ttl // 4  # 15 minutes
        elif user_activity == 'medium':
            return base_ttl // 2  # 30 minutes
        else:
            return base_ttl  # 1 hour
    
    def invalidate_user_cache(self, user_id: int):
        """Invalidate all cache entries for a user"""
        
        pattern = f"rec:{user_id}:*"
        
        for key in self.redis_client.scan_iter(match=pattern):
            self.redis_client.delete(key)

class RecommendationPrecomputation:
    def __init__(self, cache: IntelligentRecommendationCache):
        self.cache = cache
        
    async def precompute_popular_recommendations(self, batch_size: int = 1000):
        """Precompute recommendations for active users"""
        
        # Get list of active users
        active_users = await self.get_active_users()
        
        for i in range(0, len(active_users), batch_size):
            batch_users = active_users[i:i + batch_size]
            
            tasks = [
                self.precompute_user_recommendations(user_id)
                for user_id in batch_users
            ]
            
            await asyncio.gather(*tasks)
    
    async def precompute_user_recommendations(self, user_id: int):
        """Precompute recommendations for a single user"""
        
        # Get user contexts (different devices, times, etc.)
        contexts = await self.get_user_contexts(user_id)
        
        for context in contexts:
            # Generate recommendations using model
            recommendations = await self.generate_recommendations(user_id, context)
            
            # Cache with longer TTL for precomputed results
            await self.cache.cache_recommendations(
                user_id, context, recommendations, ttl=7200  # 2 hours
            )
```

**User Story 17: Auto-scaling & Load Balancing (13 points)**
*As a DevOps engineer, I want auto-scaling recommendation services across cloud providers.*

```python
# infrastructure/auto_scaling.py
import boto3
from kubernetes import client, config
from google.cloud import monitoring_v3
import asyncio
from typing import Dict, List
import logging

class MultiCloudAutoScaler:
    def __init__(self):
        self.aws_client = boto3.client('application-autoscaling')
        self.gcp_monitoring = monitoring_v3.MetricServiceClient()
        config.load_incluster_config()  # For Kubernetes
        self.k8s_apps_v1 = client.AppsV1Api()
        
    async def setup_aws_autoscaling(self, service_name: str, cluster_name: str):
        """Setup AWS ECS autoscaling"""
        
        # Register scalable target
        self.aws_client.register_scalable_target(
            ServiceNamespace='ecs',
            ResourceId=f'service/{cluster_name}/{service_name}',
            ScalableDimension='ecs:service:DesiredCount',
            MinCapacity=2,
            MaxCapacity=20,
            RoleARN='arn:aws:iam::account:role/aws-ecs-autoscaling-role'
        )
        
        # Create scaling policy
        self.aws_client.put_scaling_policy(
            PolicyName=f'{service_name}-scale-up',
            ServiceNamespace='ecs',
            ResourceId=f'service/{cluster_name}/{service_name}',
            ScalableDimension='ecs:service:DesiredCount',
            PolicyType='TargetTrackingScaling',
            TargetTrackingScalingPolicyConfiguration={
                'TargetValue': 70.0,
                'PredefinedMetricSpecification': {
                    'PredefinedMetricType': 'ECSServiceAverageCPUUtilization'
                },
                'ScaleOutCooldown': 300,
                'ScaleInCooldown': 300
            }
        )
    
    async def setup_gke_autoscaling(self, deployment_name: str, namespace: str = 'default'):
        """Setup GKE Horizontal Pod Autoscaler"""
        
        hpa_manifest = {
            'apiVersion': 'autoscaling/v2',
            'kind': 'HorizontalPodAutoscaler',
            'metadata': {
                'name': f'{deployment_name}-hpa',
                'namespace': namespace
            },
            'spec': {
                'scaleTargetRef': {
                    'apiVersion': 'apps/v1',
                    'kind': 'Deployment',
                    'name': deployment_name
                },
                'minReplicas': 3,
                'maxReplicas': 50,
                'metrics': [
                    {
                        'type': 'Resource',
                        'resource': {
                            'name': 'cpu',
                            'target': {
                                'type': 'Utilization',
                                'averageUtilization': 70
                            }
                        }
                    },
                    {
                        'type': 'Resource',
                        'resource': {
                            'name': 'memory',
                            'target': {
                                'type': 'Utilization',
                                'averageUtilization': 80
                            }
                        }
                    }
                ]
            }
        }
        
        # Create HPA
        hpa_api = client.AutoscalingV2Api()
        hpa_api.create_namespaced_horizontal_pod_autoscaler(
            namespace=namespace,
            body=hpa_manifest
        )
    
    async def custom_scaling_logic(self, metrics: Dict[str, float]) -> Dict[str, int]:
        """Custom scaling decisions based on recommendation-specific metrics"""
        
        scaling_decisions = {}
        
        # Scale based on recommendation request rate
        if metrics.get('requests_per_second', 0) > 1000:
            scaling_decisions['api_service'] = min(
                int(metrics['requests_per_second'] / 100), 20
            )
        
        # Scale based on model inference latency
        if metrics.get('inference_latency_p95', 0) > 500:  # 500ms
            scaling_decisions['model_service'] = scaling_decisions.get('model_service', 2) + 2
        
        # Scale based on cache hit ratio
        if metrics.get('cache_hit_ratio', 1.0) < 0.8:
            scaling_decisions['cache_service'] = 3
            
        return scaling_decisions
```

**User Story 18: Comprehensive Testing & Quality Assurance (12 points)**
*As a QA engineer, I want comprehensive testing across all system components.*

```python
# testing/comprehensive_testing.py
import pytest
import asyncio
from unittest.mock import Mock, patch
import numpy as np
import pandas as pd
from locust import HttpUser, task, between

class TestRecommendationSystem:
    
    @pytest.fixture
    def sample_user_data(self):
        return pd.DataFrame({
            'user_id': range(1000),
            'age': np.random.normal(35, 12, 1000),
            'gender': np.random.choice(['M', 'F'], 1000),
            'location': np.random.choice(['NYC', 'LA', 'CHI'], 1000)
        })
    
    @pytest.fixture
    def sample_interactions(self):
        return pd.DataFrame({
            'user_id': np.random.randint(1, 1000, 10000),
            'item_id': np.random.randint(1, 5000, 10000),
            'rating': np.random.uniform(1, 5, 10000),
            'timestamp': pd.date_range('2023-01-01', periods=10000, freq='H')
        })
    
    def test_collaborative_filtering_model(self, sample_interactions):
        """Test collaborative filtering model training and inference"""
        from models.collaborative_filtering import CollaborativeFilteringModels
        
        cf_model = CollaborativeFilteringModels()
        
        # Test SVD training
        user_factors, item_factors = cf_model.matrix_factorization_svd(sample_interactions)
        
        assert user_factors.shape[1] == item_factors.shape[1]  # Same embedding dimension
        assert len(user_factors) > 0
        assert len(item_factors) > 0
        
        # Test recommendations generation
        recommendations = cf_model.get_recommendations('svd', user_id=1, n_recommendations=10)
        assert len(recommendations) <= 10
    
    def test_deep_learning_models(self, sample_interactions):
        """Test PyTorch and TensorFlow model compatibility"""
        import torch
        from models.pytorch_models import NeuralCollaborativeFiltering
        
        # Test PyTorch model
        n_users = sample_interactions['user_id'].nunique()
        n_items = sample_interactions['item_id'].nunique()
        
        pytorch_model = NeuralCollaborativeFiltering(n_users, n_items)
        
        # Test forward pass
        user_ids = torch.randint(0, n_users, (32,))
        item_ids = torch.randint(0, n_items, (32,))
        
        output = pytorch_model(user_ids, item_ids)
        assert output.shape == (32, 1)
        assert torch.all(output >= 0) and torch.all(output <= 1)  # Sigmoid output
    
    def test_feature_store_operations(self, sample_user_data):
        """Test multi-database feature store operations"""
        from features.multi_db_feature_store import MultiDatabaseFeatureStore