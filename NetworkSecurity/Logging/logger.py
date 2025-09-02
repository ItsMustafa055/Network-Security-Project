import logging  # Standard Python logging library
import os  # Operating system utilities for path and directory handling
from datetime import datetime  # For generating timestamped log filenames

tell = logging.INFO  # Set desired log level (INFO)
LOG_FILE=f"{datetime.now().strftime('%m_%d_%y_%H_%M_%S')}.log"  # Create a unique timestamped log filename

log_path=os.path.join(os.getcwd(),"Logs",LOG_FILE)  # Build path for log directory (note: includes filename; likely unintended)
os.makedirs(log_path,exist_ok=True)  # Create the directory path if it does not exist

LOG_FILE_PATH=os.path.join(log_path,LOG_FILE)  # Full file path for the log (duplicates filename; results in .../filename.log/filename.log)


logging.basicConfig(  # Configure global logging settings
    filename=LOG_FILE_PATH,  # Write logs to the specified file path
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",  # Log message format
    level=tell,  # Minimum severity level to record
)