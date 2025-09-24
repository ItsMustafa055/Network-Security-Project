from NetworkSecurity.Constants.Training_Pipeline import SCHEMA_FILEPATH
from NetworkSecurity.Entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from NetworkSecurity.Entity.config_entity import DataValidationConfig
from NetworkSecurity.Exception.exception import NetworkSecurityException
from NetworkSecurity.Logging.logger import logging
from NetworkSecurity.Utils.main_utils.utils import read_yaml_file

from scipy.stats import ks_2samp
import pandas as pd
import os, sys

class DataValidation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact, data_validation_artifact:DataValidationConfig):

        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_artifact=data_validation_artifact
            self._schema_config = read_yaml_file(SCHEMA_FILEPATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)


