import os
import sys
import numpy as np
import pandas as pd

"""
defining common constants variable for training pipeline
"""

TARGET_COLUMN = "Result"
PIPELINE_NAME = "PhisingData"
ARTIFACT_DIR = "Artifacts"
FILE_NAME = "phisingData.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"



"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""

DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"
DATA_INGESTION_DATABASE_NAME: str = "PhisingData"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTON_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTION_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2