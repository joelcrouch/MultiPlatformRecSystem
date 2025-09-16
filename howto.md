make these directrires: .
    2 ├── data/
    3 │   ├── raw/
    4 │   ├── processed/
    5 │   └── interim/
    6 ├── notebooks/
    7 │   ├── 0_data_exploration.ipynb
    8 │   ├── 1_model_prototyping.ipynb
    9 │   └── 2_evaluation_analysis.ipynb
   10 ├── src/
   11 │   ├── api/
   12 │   │   ├── __init__.py
   13 │   │   ├── main.py
   14 │   │   └── routers/
   15 │   ├── data/
   16 │   │   ├── __init__.py
   17 │   │   └── data_loader.py
   18 │   ├── models/
   19 │   │   ├── __init__.py
   20 │   │   ├── collaborative_filtering.py
   21 │   │   ├── deep_learning.py
   22 │   │   └── content_based.py
   23 │   ├── features/
   24 │   │   ├── __init__.py
   25 │   │   └── feature_engineering.py
   26 │   ├── pipelines/
   27 │   │   ├── __init__.py
   28 │   │   ├── training_pipeline.py
   29 │   │   └── inference_pipeline.py
   30 │   ├── monitoring/
   31 │   │   ├── __init__.py
   32 │   │   └── monitoring.py
   33 │   └── core/
   34 │       ├── __init__.py
   35 │       ├── config.py
   36 │       └── utils.py
   37 ├── tests/
   38 │   ├── __init__.py
   39 │   ├── test_data.py
   40 │   ├── test_models.py
   41 │   └── test_pipelines.py
   42 ├── infrastructure/
   43 │   ├── aws/
   44 │   │   ├── sagemaker.py
   45 │   │   └── terraform/
   46 │   ├── gcp/
   47 │   │   ├── vertex_ai.py
   48 │   │   └── terraform/
   49 │   └── azure/
   50 │       ├── azure_ml.py
   51 │       └── terraform/
   52 ├── dashboard/
   53 │   └── main.py
   54 ├── scripts/
   55 │   ├── setup.sh
   56 │   ├── train.py
   57 │   └── deploy.py
   58 ├── .gitignore
   59 ├── README.md
   60 └── requirements.txt


   amd mkdir -p data/amazon data/ data/ml-25m  and mkdir -p docs/ docs/dailylog

   Make sure conda is installed and do

   conda create  --name  <name>  python=3.9  && conda activate <name>


   git all the libraries you tink you will need to start , put thme into requirements.txt and do a

   pip install -r requirements.txt
   