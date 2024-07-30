from pymongo import MongoClient
from models.repo import Repo
from models.org import Org

import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Connect to MongoDB (update the connection string as needed)

class ScanRepoRepo :

    def __init__(self) :
        self.client = MongoClient(os.getenv("MONGO_URI"))
        # Select database and collection
        self.db = self.client["Secret_scan_data"]
        self.collection = None
    

    def get_document_by_name(self, repository: str):
        return self.collection.find_one({"repository": repository})

    def replace_document_by_name(self, repository: str, repo_data: dict):
        result = self.collection.replace_one({"repository": repository}, repo_data)
        return result


    def setScanRepo(self, repo_data) :
        repository = repo_data.repository
        collections = sorted(self.db.list_collection_names())
        if len(collections) == 0 :
            return {"message": "No collection in database"}
        self.collection = self.db[collections[-1]]


        existing_item = self.get_document_by_name(repository)
        if not existing_item:
            raise HTTPException(status_code=404, detail="Item not found with repository "+ repository)

        # Convert Pydantic model to dict for MongoDB
        repo_data = repo_data.dict()
        self.replace_document_by_name(repository, repo_data)
        return repo_data
