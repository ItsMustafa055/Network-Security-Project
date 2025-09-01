import sys

from NetworkSecurity.Logging import logger
class NetworkSecurityException(Exception):
    def __init__(self, error_message,error_details:sys):
        self.error_message = error_message
        __,__,exc_tb = error_details.exc_info()

        self.lineno=exc_tb.tb_lineno

    def __str__(self) -> str:
        return f"Error Occored in Python Script name [{0}] Line Number [{1}] error message [{2}]".format
        (self.file_name, self.lineno, str(self.error_message))


if __name__=='__main__':
    try:
        logger.logging.info("Enter the try block")
        a=1/0
        print("This will not be printed",a)
    except Exception as e:
           raise NetworkSecurityException(e,sys)