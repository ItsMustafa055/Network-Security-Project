from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str

class DataValidationArtifact:
    validation_status: bool
    valid_train_filepath: str
    valid_test_filepath: str
    invaid_train_filepath: str
    invalid_test_filepath: str
    drift_report_filepath: str
