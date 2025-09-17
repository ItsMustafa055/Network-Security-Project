# Import required system modules
import os  # For operating system operations and environment variables
import sys  # For system-specific parameters and functions
import json  # For JSON data handling

# Load environment variables from .env file
from dotenv import load_dotenv  # Import load_dotenv to access environment variables
load_dotenv()  # Initialize and load environment variables

# Get MongoDB connection URL from environment variables
MONGODB_URL = os.getenv("MONGODB_URL_KEY")  # Retrieve MongoDB connection string
print(MONGODB_URL)  # Debug print to verify MongoDB URL

# Import SSL certificate handling for MongoDB connection
import certifi  # For SSL certificate verification
ca = certifi.where()  # Get path to SSL certificates

# Import data handling and database libraries
import pandas as pd  # For data manipulation
import numpy as np  # For numerical operations
import pymongo  # MongoDB driver for Python

# Import custom exception and logging modules
from NetworkSecurity.Exception.exception import NetworkSecurityException
from NetworkSecurity.Logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass  # Initialize class (currently empty)
        except Exception as e:
            raise NetworkSecurityException(e,sys)  # Handle any initialization errors

    def csv_to_jsonconvertor(self,file_path):
        try:
            data = pd.read_csv(file_path)  # Read CSV file into pandas DataFrame
            data.reset_index(drop=True,inplace=True)  # Reset DataFrame index
            records = list(json.loads(data.T.to_json()).values())  # Convert DataFrame to JSON format
            return records  # Return JSON records
        except Exception as e:
            raise NetworkSecurityException(e,sys)  # Handle any conversion errors

    def insert_data_toMongoDB(self,records,database,collection):
        try:
            # Store parameters as instance variables
            self.database = database
            self.collection = collection
            self.records = records

            # Create MongoDB connection and insert data
            self.mongo_client = pymongo.MongoClient(MONGODB_URL)  # Connect to MongoDB
            self.database = self.mongo_client[self.database]  # Select database
            self.collection = self.database[self.collection]  # Select collection
            self.collection.insert_many(self.records)  # Insert records into collection
            return(len(self.records))  # Return number of inserted records
        except Exception as e:
            raise NetworkSecurityException(e,sys)  # Handle any database errors

# Main execution block
if __name__=='__main__':
    FILE_PATH = "/home/nsl/Documents/Network-Security-Project/Network_data/phisingData.csv"  # Path to input CSV file
    DATABASE = "PhisingData"  # MongoDB database name
    Collection = "NetworkData"  # MongoDB collection name
    
    networkobj = NetworkDataExtract()  # Create instance of NetworkDataExtract
    records = networkobj.csv_to_jsonconvertor(file_path=FILE_PATH)  # Convert CSV to JSON
    print(records)  # Debug print of converted records
    
    no_of_records = networkobj.insert_data_toMongoDB(records,DATABASE,Collection)  # Insert data into MongoDB
    print(no_of_records)  # Print number of inserted records