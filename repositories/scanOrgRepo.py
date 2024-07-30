from pymongo import MongoClient
from models.repo import Repo
from models.org import Org
from threading import Lock

lock = Lock()

import logging
import re
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Connect to MongoDB (update the connection string as needed)

class ScanOrgRepo :

    def __init__(self) :
        self.client = MongoClient(os.getenv("MONGO_URI"))
        # Select database and collection
        self.db = self.client["Secret_scan_data"]
        self.collection = None
    

    def createNewCollection(self) :
        # Create new collection based on current date and timesudo docker o
        collectionName = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.db.create_collection(collectionName)
        self.collection = self.db[collectionName]
        print(f"Created new collection: {self.collection}")


    def dropLastCollection(self) :

        # List all collections and sort them
        collections = sorted(self.db.list_collection_names())

        # Delete the second-to-last collection if more than one collection exists
        if len(collections) > 1:
            second_last_collection = collections[-2]
            self.db.drop_collection(second_last_collection)
            print(f"Deleted collection: {second_last_collection}")
        else:
            print("No collection was deleted, as there aren't enough collections to delete the second-to-last one.")


    def insertRepoData(self, repo: Repo) :
        try:
            with lock:
                logger.info(f"Inserting repository data: {repo}")
                # Check the size of the repo object if needed
                # e.g., print("Size of repo data:", sys.getsizeof(repo.dict()))
                self.collection.insert_one(repo.dict())
                logger.info("Successfully inserted repository data.")
        except Exception as e:
            logger.error(f"Failed to insert repository data: {str(e)}")


    def fetchOrgData(self, start_index, end_index, keyword, sort) :
        repo = []
        collections = sorted(self.db.list_collection_names())
        if len(collections) == 0 :
            return {"message": "No collection in database"}
        self.collection = self.db[collections[-1]]

        # Search for documents containing the keyword
        query =  {"repository": {"$regex": re.escape(keyword), "$options": "i"}} if keyword else {}

        total_documents = self.collection.count_documents(query)
        total_pages = total_documents // (end_index - start_index + 1) + (1 if total_documents % (end_index - start_index + 1) > 0 else 0)

        print(total_documents)
        if start_index >0 :
            start_index = start_index -1
        if sort == True :
            # Fetching documents and sorting based on the length of the "asd" list
            documents = self.collection.find(query).sort([("secrets", -1)]).skip(start_index).limit(end_index - start_index)
        else :
            documents = self.collection.find(query).skip(start_index).limit(end_index - start_index)
        #documents = self.collection.find(query)
        for document in documents:
            document.pop("_id", None)
            print(document)
            repo.append(Repo(**document))

        org = {"name": "random", "scanedRepos": int(self.collection.count_documents({})), "startIndex": start_index,
            "endIndex": end_index, "totalPages": total_pages, "repositories": repo}

        return Org(**org)

    def getNoScannedRepo(self) :
        self.setLastCollection()
        if self.collection == None :
            return 0
        else :
            return int(self.collection.count_documents({}))


    def checkForRepo(self, repository) :
        # Check for existence
        exists = self.collection.find_one({"repository": repository}) is not None
        print(exists)
        return exists

    def orgScanStart(self) :
        self.dropLastCollection()
        self.createNewCollection()

    def setLastCollection(self) :
        collections = sorted(self.db.list_collection_names())
        if len(collections) == 0 :
            self.collection = None
        else :
            self.collection = self.db[collections[-1]]
 
