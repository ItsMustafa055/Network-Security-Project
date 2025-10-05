import yaml
from NetworkSecurity.Constants.Training_Pipeline import SCHEMA_FILE_PATH
from NetworkSecurity.Entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from NetworkSecurity.Entity.config_entity import DataValidationConfig
from NetworkSecurity.Exception.exception import NetworkSecurityException
from NetworkSecurity.Logging.logger import logging
from NetworkSecurity.Utils.main_utils.utils import read_yaml_file, write_yaml_file

from scipy.stats import ks_2samp
import pandas as pd
import os
import sys

class DataValidation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact, data_validation_config:DataValidationConfig):

        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

 # Below method will be used to read the data from the file path
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            schema_columns_list = self._schema_config.get("columns", [])
            required_columns = []
            for column_map in schema_columns_list:
              required_columns.extend(list(column_map.keys()))

            number_of_columns = len(required_columns)
            logging.info(f"Required number of columns:{number_of_columns}")
            logging.info(f"Data frame has columns:{len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def validate_numerical_columns_exist(self, dataframe: pd.DataFrame) -> bool:
        try:
            required_numerical_columns = set(self._schema_config.get("numerical_columns", []))
            if not required_numerical_columns:
                logging.info("No 'numerical_columns' specified in schema; skipping numerical column existence check")
                return True

            present_columns = set(dataframe.columns)
            missing_columns = sorted(list(required_numerical_columns - present_columns))

            if missing_columns:
                logging.error(f"Missing numerical columns: {missing_columns}")
                return False

            logging.info("All required numerical columns are present")
            return True
        except Exception as e:
            raise NetworkSecurityException(e, sys)

 # Check data drift
    def detect_data_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_same_dist=ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                    
                    }})
            drift_report_filepath = self.data_validation_config.drift_report_filepath

            #Create directory
            dir_path = os.path.dirname(drift_report_filepath)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_filepath,content=report)

        except Exception as e:
            raise NetworkSecurityException(e,sys)




    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            # Delcare file paths for test and train
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
             
             # Read the data from train and test
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)


            # Validate Number of columns
            status=self.validate_number_of_columns(dataframe=train_df)
            if not status:
                error_message="Validation Failed. Number of columns in train dataframe is not equal to required number of columns"
                raise Exception(error_message)

            status=self.validate_number_of_columns(dataframe=test_df)
            if not status:
                error_message="Validation Failed. Number of columns in test dataframe is not equal to required number of columns"
                raise Exception(error_message)

            # checking DataDrifts
            status=self.detect_data_drift(base_df=train_df , current_df=test_df)
            dir_path=os.path.dirname(self.data_validation_config.valid_training_filepath)
            os.makedirs(dir_path,exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_training_filepath, index=False, header=True)
            test_df.to_csv(self.data_validation_config.valid_testing_filepath, index=False, header=True)

            data_validation_artifact = DataValidationArtifact(
                validation_status = status,
                valid_training_filepath = self.data_validation_config.valid_training_filepath,
                valid_testing_filepath = self.data_validation_config.valid_testing_filepath,
                invalid_training_filepath = None,
                invalid_testing_filepath = None,
                drift_report_filepath = self.data_validation_config.drift_report_filepath

            )

            # Validate numerical columns presence
            status = self.validate_numerical_columns_exist(dataframe=train_df)
            if not status:
                error_message = "Validation Failed. Train dataframe is missing required numerical columns"
                raise Exception(error_message)

            status = self.validate_numerical_columns_exist(dataframe=test_df)
            if not status:
                error_message = "Validation Failed. Test dataframe is missing required numerical columns"
                raise Exception(error_message)

            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)


           

          
           # self.validate_number_of_columns(train_df=train_df, test_df=test_df)