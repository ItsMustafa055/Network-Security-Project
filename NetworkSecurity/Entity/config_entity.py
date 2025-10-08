from datetime import datetime
import os

from NetworkSecurity.Constants import Training_Pipeline

print(Training_Pipeline.PIPELINE_NAME)
print(Training_Pipeline.ARTIFACT_DIR)


class TrainingPipelineConfig:
    def __init__(self):
        timestamp=datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name = Training_Pipeline.PIPELINE_NAME
        self.artifact_name = Training_Pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name,timestamp)
        self.timestamp: str=timestamp


class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir:str=os.path.join(
            training_pipeline_config.artifact_dir,Training_Pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path: str=os.path.join(
            self.data_ingestion_dir, Training_Pipeline.DATA_INGESTON_FEATURE_STORE_DIR, Training_Pipeline.FILE_NAME
        )
        self.training_file_path: str=os.path.join(
            self.data_ingestion_dir, Training_Pipeline.DATA_INGESTION_INGESTION_DIR, Training_Pipeline.TRAIN_FILE_NAME
        )
        self.testing_file_path: str=os.path.join(
            self.data_ingestion_dir, Training_Pipeline.DATA_INGESTION_INGESTION_DIR, Training_Pipeline.TEST_FILE_NAME
        )

        self.train_test_split_ratio: float = Training_Pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO 
        self.collection_name: str = Training_Pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name: str = Training_Pipeline.DATA_INGESTION_DATABASE_NAME


class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir: str = os.path.join(training_pipeline_config.artifact_dir, Training_Pipeline.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir: str = os.path.join(self.data_validation_dir, Training_Pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir: str = os.path.join(self.data_validation_dir,  Training_Pipeline.DATA_VALIDATION_INVALID_DIR)
        self.valid_training_filepath: str = os.path.join(self.data_validation_dir, Training_Pipeline.TRAIN_FILE_NAME)
        self.invalid_training_filepath: str = os.path.join(self.data_validation_dir, Training_Pipeline.TRAIN_FILE_NAME)
        self.valid_testing_filepath: str = os.path.join(self.data_validation_dir, Training_Pipeline.TEST_FILE_NAME)
        self.invalid_testing_filepath: str = os.path.join(self.data_validation_dir, Training_Pipeline.TEST_FILE_NAME)
        self.drift_report_filepath: str = os.path.join(
            self.data_validation_dir,
            Training_Pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            Training_Pipeline.DATA_VALIDATION_DRIFT_REPORT_FILENAME,
        )


class DataTransformationConfig:
     def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join( training_pipeline_config.artifact_dir,Training_Pipeline.DATA_TRANSFORMATION_DIR_NAME )
        self.transformed_train_file_path: str = os.path.join( self.data_transformation_dir,Training_Pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            Training_Pipeline.TRAIN_FILE_NAME.replace("csv", "npy"),)
        self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir,  Training_Pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            Training_Pipeline.TEST_FILE_NAME.replace("csv", "npy"), )
        self.transformed_object_file_path: str = os.path.join( self.data_transformation_dir, Training_Pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            Training_Pipeline.PREPROCESSING_OBJECT_FILE_NAME,)