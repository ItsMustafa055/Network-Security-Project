import sys
from NetworkSecurity.Components import data_validation
from NetworkSecurity.Components.data_ingestion import DataIngestion
from NetworkSecurity.Components.data_validation import DataValidation
from NetworkSecurity.Exception.exception import NetworkSecurityException
from NetworkSecurity.Logging.logger import logging
from NetworkSecurity.Entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig

if __name__=="__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Data ingestion started")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion Completed")



        data_validation_config=DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        logging.info("Initiate the Data Validation")
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("Data Validation Completed")
    except Exception as e:
        logging.error("Error occurred during data ingestion")
        raise NetworkSecurityException(e,sys)