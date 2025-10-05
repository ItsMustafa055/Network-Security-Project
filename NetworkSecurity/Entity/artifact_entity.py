from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_training_filepath: str
    valid_testing_filepath: str
    invalid_training_filepath: str
    invalid_testing_filepath: str
    drift_report_filepath: str
