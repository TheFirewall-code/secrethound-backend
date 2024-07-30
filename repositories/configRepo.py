from pymongo import MongoClient
from models.config import Config
import os

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Connect to MongoDB (update the connection string as needed)

class ConfigRepo :

    def __init__(self) :
        self.client = MongoClient(os.getenv("MONGO_URI"))
        # Select database and collection
        self.db = self.client["Secret_scan"]
        self.collection = self.db["config"]

    def insertConfig(self, config : Config) :
        self.collection.insert_one(config.dict()) #for inserting the model we have to change it  to dict


    def deleteConfig(self) :
        count = self.collection.count_documents({})

        if count  < 1:
            return True  # Collection is not empty
        self.collection.delete_one({})
        return True
    

    def getConfig(self) -> Config:
        first_document = self.collection.find_one()

        if first_document == None : 
            return Config()
        first_document.pop("_id", None)
        return Config(**first_document) #TODO: escape the object id field

    #def fetchOrgData(self) :
 