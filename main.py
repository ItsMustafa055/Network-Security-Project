import sys
from NetworkSecurity.Components import data_validation
from NetworkSecurity.Components.data_ingestion import DataIngestion
from NetworkSecurity.Components.data_validation import DataValidation
from NetworkSecurity.Components.data_transformation import DataTransformation
from NetworkSecurity.Exception.exception import NetworkSecurityException
from NetworkSecurity.Logging.logger import logging
from NetworkSecurity.Entity.config_entity import DataIngestionConfig, DataTransformationConfig, TrainingPipelineConfig, DataValidationConfig

if __name__=="__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Data ingestion started")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion Completed")
        print(data_ingestion_artifact)



        data_validation_config=DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        logging.info("Initiate the Data Validation")
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("Data Validation Completed")
        print(data_validation_artifact)


        data_transformartion_config=DataTransformationConfig(training_pipeline_config)
        logging.info("Initiate Data Transformation")
        data_transformation = DataTransformation(data_validation_artifact,data_transformartion_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data Transformation Completed")
        print(data_transformation_artifact)

    except Exception as e:
        logging.error("Error occurred during data ingestion")
        raise NetworkSecurityException(e,sys)