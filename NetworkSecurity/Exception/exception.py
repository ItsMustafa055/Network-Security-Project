import sys  # Imports the sys module, used for accessing system-specific parameters and functions

from NetworkSecurity.Logging import logger  # Imports the logger object from the project's Logging module

class NetworkSecurityException(Exception):  # Defines a custom exception class inheriting from Python's Exception
    def __init__(self, error_message, error_details:sys):  # Constructor takes an error message and error details (sys)
        self.error_message = error_message  # Stores the error message in the instance
        __,__,exc_tb = error_details.exc_info()  # Retrieves the traceback object from the current exception info

        self.lineno = exc_tb.tb_lineno  # Stores the line number where the exception occurred
        self.file_name = exc_tb.tb_frame.f_code.co_filename  # Gets the filename where the exception occurred

    def __str__(self) -> str:  # Defines how the exception is represented as a string
        return f"Error Occurred in Python Script name [{self.file_name}] Line Number [{self.lineno}] error message [{str(self.error_message)}]"  # Formats the error details for display

if __name__=='__main__':  # Checks if this script is being run directly
    try:  # Starts a try block to catch exceptions
        logger.logging.info("Enter the try block")  # Logs an info message indicating entry into the try block
        a=1/0  # Deliberately causes a ZeroDivisionError
        print("This will not be printed",a)  # This line will not execute due to the exception above
    except Exception as e:  # Catches any exception that occurs in the try block
           raise NetworkSecurityException(e,sys)  # Raises the custom exception with the error and