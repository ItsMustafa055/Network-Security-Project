import os
import sys
import numpy as np
import pandas as pd





DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"
DATA_INGESTION_DATABASE_NAME: str = "NetworkSecurity"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTON_FEATURE_STROE_DIR: str = "feature_store"
DATA_INGESTION_INGESTION_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2