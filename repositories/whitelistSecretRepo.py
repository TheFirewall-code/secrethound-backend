from pymongo import MongoClient
from models.whitelistSecret import WhitelistSecret

import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Connect to MongoDB (update the connection string as needed)

class WhitelistSecretRepo :

    def __init__(self) :
        self.client = MongoClient(os.getenv("MONGO_URI"))
        # Select database and collection
        self.db = self.client["Whitelist_Secret"]
        self.collection = None

    def loadCollection(self, whitelistSecret) :
        if whitelistSecret.OrgScope == True :
            self.collection = self.db["org_whitelist"]
        else :
            self.collection = self.db["repo_whitelist"]

    def inserttWhitelist(self, whitelistSecret :WhitelistSecret ) :
        self.loadCollection(whitelistSecret)
        self.collection.insert_one(whitelistSecret.dict())

        return {"message" : "WhiteListing done !"}


    def get_document_by_key(self, secret: str):
        return self.collection.find_one({"Secret": secret})


    def deleteWhitelist(self, secret) :
        query = {"Secret": secret}

        #delete repo
        self.collection = self.db["repo_whitelist"]
        existing_item = self.get_document_by_key(secret)
        if existing_item:
            self.collection.delete_one(query)

        #delete org
        self.collection = self.db["org_whitelist"]
        existing_item = self.get_document_by_key(secret)
        if existing_item:
            self.collection.delete_one(query)

        return {"message": "Document deleted successfully !"}
        
    

    def fetchOrgWhitelist(self) :
        self.collection = self.db["org_whitelist"]

        whiteListSecrets = []
        collections = sorted(self.db.list_collection_names())
        if len(collections) == 0 :
            return {"message": "No collection in database"}


        for document in self.collection.find():
            document.pop("_id", None)
            whiteListSecrets.append(WhitelistSecret(**document))

        #total_documents = self.collection.count_documents({})

        return whiteListSecrets

    def fetchRepoWhitelist(self) :
        self.collection = self.db["repo_whitelist"]

        whiteListSecrets = []
        collections = sorted(self.db.list_collection_names())
        if len(collections) == 0 :
            return {"message": "No collection in database"}


        for document in self.collection.find():
            document.pop("_id", None)
            whiteListSecrets.append(WhitelistSecret(**document))

        #total_documents = self.collection.count_documents({})

        return whiteListSecrets

    #def fetchOrgData(self) :
 