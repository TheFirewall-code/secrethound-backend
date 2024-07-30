from pymongo import MongoClient
from models.webhookConfig import WebhookConfig

import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Connect to MongoDB (update the connection string as needed)

class WebhookConfigRepo :

    def __init__(self) :
        self.client = MongoClient(os.getenv("MONGO_URI"))
        # Select database and collection
        self.db = self.client["webhook"]
        self.collection = self.db["config"]

    def insertConfig(self, webhookConfig : WebhookConfig) :
        self.collection.insert_one(webhookConfig.dict()) #for inserting the model we have to change it  to dict


    def deleteConfig(self) :
        count = self.collection.count_documents({})

        if count  < 1:
            return True  # Collection is not empty
        self.collection.delete_many({})
        return True
    

    def getConfig(self) -> WebhookConfig:
        first_document = self.collection.find_one()

        if first_document == None : 
            return WebhookConfig()
        first_document.pop("_id", None)
        return WebhookConfig(**first_document) #TODO: escape the object id field

    #def fetchOrgData(self) :
 