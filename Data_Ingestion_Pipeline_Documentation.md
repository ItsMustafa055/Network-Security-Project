# Data Ingestion Pipeline Documentation
## Network Security Project - Phishing Detection

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Pipeline Components](#pipeline-components)
4. [Data Flow](#data-flow)
5. [Configuration Management](#configuration-management)
6. [Process Steps](#process-steps)
7. [File Structure](#file-structure)
8. [Environment Setup](#environment-setup)
9. [Error Handling & Logging](#error-handling--logging)
10. [Usage Instructions](#usage-instructions)

---

## 🎯 Overview

This document explains the **Data Ingestion Pipeline** for a Network Security project focused on **Phishing Detection**. The pipeline is designed to extract data from MongoDB, process it, and prepare it for machine learning model training.

### Key Objectives:
- Extract network security data from MongoDB Atlas
- Clean and preprocess the data
- Split data into training and testing sets
- Store processed data in organized file structure
- Maintain comprehensive logging and error handling

---

## 🏗️ Architecture

The data ingestion pipeline follows a **modular, object-oriented design** with clear separation of concerns:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MongoDB       │───▶│  Data Ingestion  │───▶│  File Storage   │
│   (Source)      │    │    Component     │    │   (Artifacts)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  Logging System  │
                       └──────────────────┘
```

---

## 🔧 Pipeline Components

### 1. **DataIngestion Class** (`NetworkSecurity/Components/data_ingestion.py`)
The main orchestrator class that handles the entire data ingestion process.

**Key Methods:**
- `export_collection_as_dataframe()`: Extracts data from MongoDB
- `export_data_to_feature_store()`: Saves raw data to feature store
- `split_train_test_from_data()`: Splits data into train/test sets
- `initiate_data_ingestion()`: Main method that orchestrates the entire process

### 2. **Configuration Management**
- **TrainingPipelineConfig**: Manages overall pipeline configuration
- **DataIngestionConfig**: Handles data ingestion specific settings
- **Constants**: Centralized configuration values

### 3. **Data Artifacts**
- **DataIngestionArtifact**: Stores paths to generated files
- **Feature Store**: Raw data storage
- **Training/Testing Files**: Split datasets

---

## 📊 Data Flow

```mermaid
graph TD
    A[MongoDB Collection] --> B[Data Extraction]
    B --> C[Data Cleaning]
    C --> D[Feature Store CSV]
    D --> E[Train/Test Split]
    E --> F[Training Dataset]
    E --> G[Testing Dataset]
    F --> H[Artifacts Directory]
    G --> H
    H --> I[DataIngestionArtifact]
    
    B --> J[Logging System]
    C --> J
    D --> J
    E --> J
```

### Detailed Process Flow:

1. **Data Source**: MongoDB Atlas with collection "NetworkData" in database "PhisingData"
2. **Extraction**: Convert MongoDB documents to pandas DataFrame
3. **Cleaning**: Remove MongoDB "_id" column and replace "na" values with NaN
4. **Storage**: Save cleaned data to feature store
5. **Splitting**: Split data into 80% training and 20% testing sets
6. **Output**: Generate train.csv and test.csv files
7. **Artifact**: Return file paths for downstream processes

---

## ⚙️ Configuration Management

### Constants (`NetworkSecurity/Constants/Training_Pipeline/__init__.py`)

```python
# Pipeline Configuration
PIPELINE_NAME = "PhisingData"
ARTIFACT_DIR = "Artifacts"
FILE_NAME = "phisingData.csv"

# File Names
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

# Data Ingestion Settings
DATA_INGESTION_COLLECTION_NAME = "NetworkData"
DATA_INGESTION_DATABASE_NAME = "PhisingData"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO = 0.2  # 20% for testing
```

### Environment Variables
The pipeline uses environment variables for sensitive configuration:
- `MONGODB_URL_KEY`: MongoDB connection string
- `MONGO_DB_NAME`: Database name
- `MONGO_COLLECTION_NAME`: Collection name

---

## 🔄 Process Steps

### Step 1: Data Extraction (`export_collection_as_dataframe`)
```python
def export_collection_as_dataframe(self):
    # Connect to MongoDB
    self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
    collection = self.mongo_client[database_name][collection_name]
    
    # Convert to DataFrame
    df = pd.DataFrame(list(collection.find()))
    
    # Clean data
    if "_id" in df.columns:
        df.drop(columns="_id", axis=1, inplace=True)
    df.replace({"na": np.nan}, inplace=True)
    
    return df
```

### Step 2: Feature Store Export (`export_data_to_feature_store`)
```python
def export_data_to_feature_store(self, dataframe):
    # Create directory structure
    dir_path = os.path.dirname(feature_store_file_path)
    os.makedirs(dir_path, exist_ok=True)
    
    # Save to CSV
    dataframe.to_csv(feature_store_file_path, index=False, header=True)
    return dataframe
```

### Step 3: Train/Test Split (`split_train_test_from_data`)
```python
def split_train_test_from_data(self, dataframe):
    # Split data (80% train, 20% test)
    train_set, test_set = train_test_split(
        dataframe, 
        test_size=self.data_ingestion_config.train_test_split_ratio
    )
    
    # Save both sets
    train_set.to_csv(training_file_path, index=False, header=True)
    test_set.to_csv(testing_file_path, index=False, header=True)
```

### Step 4: Main Orchestration (`initiate_data_ingestion`)
```python
def initiate_data_ingestion(self):
    # Execute all steps in sequence
    df = self.export_collection_as_dataframe()
    dataframe = self.export_data_to_feature_store(df)
    self.split_train_test_from_data(dataframe)
    
    # Return artifact with file paths
    return DataIngestionArtifact(
        trained_file_path=self.data_ingestion_config.training_file_path,
        test_file_path=self.data_ingestion_config.testing_file_path
    )
```

---

## 📁 File Structure

The pipeline creates a timestamped directory structure:

```
Artifacts/
└── {timestamp}/                    # e.g., 09_19_2025_00_17_50
    └── data_ingestion/
        ├── feature_store/
        │   └── phisingData.csv     # Raw data from MongoDB
        └── ingested/
            ├── train.csv           # Training dataset (80%)
            └── test.csv            # Testing dataset (20%)
```

### Directory Naming Convention:
- **Timestamp Format**: `MM_DD_YYYY_HH_MM_SS`
- **Feature Store**: Contains raw, unprocessed data
- **Ingested**: Contains processed train/test splits

---

## 🔧 Environment Setup

### Required Dependencies:
```python
# Core Libraries
pymongo          # MongoDB connection
pandas           # Data manipulation
numpy            # Numerical operations
scikit-learn     # Train/test split
python-dotenv    # Environment variables

# Custom Modules
NetworkSecurity.Exception.exception
NetworkSecurity.Logging.logger
NetworkSecurity.Entity.config_entity
NetworkSecurity.Entity.artifact_entity
```

### Environment Variables (.env file):
```env
MONGODB_URL_KEY=mongodb+srv://username:password@cluster.mongodb.net/
MONGO_DB_NAME=PhisingData
MONGO_COLLECTION_NAME=NetworkData
```

---

## 📝 Error Handling & Logging

### Exception Handling
- **Custom Exception**: `NetworkSecurityException` for consistent error handling
- **Try-Catch Blocks**: Comprehensive error handling in all methods
- **Graceful Failures**: Pipeline stops gracefully on errors

### Logging System (`NetworkSecurity/Logging/logger.py`)
```python
# Log Configuration
LOG_LEVEL = logging.INFO
LOG_FORMAT = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "{timestamp}.log"
```

### Log Structure:
```
Logs/
└── {timestamp}.log/
    └── {timestamp}.log
```

**Log Messages Include:**
- Pipeline start/end events
- Data processing steps
- Error messages with stack traces
- File path confirmations

---

## 🚀 Usage Instructions

### Running the Pipeline

1. **Set up environment variables** in `.env` file
2. **Install dependencies** from `reqmnt.txt`
3. **Run the main script**:

```bash
python main.py
```

### Main Script (`main.py`):
```python
if __name__ == "__main__":
    try:
        # Initialize configuration
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        
        # Create data ingestion instance
        data_ingestion = DataIngestion(data_ingestion_config)
        
        # Execute pipeline
        logging.info("Data ingestion started")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        
    except Exception as e:
        logging.error("Error occurred during data ingestion")
        raise NetworkSecurityException(e, sys)
```

### Expected Output:
```
DataIngestionArtifact(trained_file_path='Artifacts/09_19_2025_00_17_50/data_ingestion/ingested/train.csv', 
                     test_file_path='Artifacts/09_19_2025_00_17_50/data_ingestion/ingested/test.csv')
```

---

## 🔍 Key Features

### ✅ **Strengths:**
- **Modular Design**: Easy to maintain and extend
- **Comprehensive Logging**: Full audit trail of operations
- **Error Handling**: Robust exception management
- **Configuration Management**: Centralized settings
- **Timestamped Artifacts**: Version control for data
- **Environment Security**: Sensitive data in environment variables

### ⚠️ **Areas for Improvement:**
- **Data Validation**: Add schema validation for incoming data
- **Data Quality Checks**: Implement data quality metrics
- **Incremental Processing**: Support for delta data ingestion
- **Monitoring**: Add data pipeline monitoring and alerting
- **Testing**: Unit tests for individual components

---

## 📈 Next Steps

1. **Data Validation**: Implement data quality checks
2. **Feature Engineering**: Add feature transformation pipeline
3. **Model Training**: Integrate with ML training pipeline
4. **Monitoring**: Add pipeline health monitoring
5. **CI/CD**: Implement automated testing and deployment

---

## 📞 Support

For questions or issues with the data ingestion pipeline:
1. Check the logs in the `Logs/` directory
2. Verify environment variables are correctly set
3. Ensure MongoDB connection is accessible
4. Review the error messages in the console output

---

*This documentation was generated for the Network Security Project - Phishing Detection Data Ingestion Pipeline.*
