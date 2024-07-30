from pymongo import MongoClient
from models.repo import Repo
from models.org import Org
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Connect to MongoDB (update the connection string as needed)

class DashboardRepo :

    def __init__(self) :
        self.client = MongoClient(os.getenv("MONGO_URI"))

        # Select database and collection
        self.db = self.client["Dashboard"]
        self.collection = self.db["dash"]

    def storeDash(self, dashData) :
        try:
            logger.info(f"Inserting repository data")
            # Check the size of the repo object if needed
            # e.g., print("Size of repo data:", sys.getsizeof(repo.dict()))
            self.collection.insert_one(dashData)
            print(len(dashData["data"]))
            logger.info("Successfully inserted repository data.")
        except Exception as e:
            logger.error(f"Failed to insert repository data: {str(e)}")

        #self.collection.insert_one(dashData)

    def getOrgCollections(self) :
        client = MongoClient(os.getenv("MONGO_URI"))

        db = client["Secret_scan_data"]
        collections = sorted(db.list_collection_names())
        if len(collections) == 0 :
            return {"message": "No collection in database"}
        
        return db[collections[-1]]

    def fetchScanOrgData(self, collection) :
        repo = []
        for document in collection.find():
            document.pop("_id", None)
            repo.append(Repo(**document))

        total_documents = collection.count_documents({})
        org = {"name": "random", "scanedRepos": int(total_documents), "repositories": repo}

        return Org(**org)

    def getLastDash(self) :
        document = None
        latest_document = self.collection.find().sort("_id", -1).limit(1)
        for document in latest_document:
            document.pop("_id", None)

        return document

    def getDashData(self, start_index, end_index) :

        total_documents = self.collection.count_documents({})
    
        # Calculate the total number of pages
        page_size = end_index - start_index + 1
        total_pages = total_documents // page_size + (1 if total_documents % page_size > 0 else 0)

        # Calculate the MongoDB skip value by reversing the index calculation
        # We calculate how many documents to skip from the start to reach the desired end_index from the end
        diff_index = end_index - start_index
        skip_count = max(0, total_documents - diff_index)
        limit_count =  min(skip_count + diff_index, total_documents) #min(end_index - start_index + 1, total_documents - skip_count)
        print(skip_count, " ", limit_count)
        # Retrieve documents using the calculated skip and limit
        # Since we want the latest documents first, we should sort by an appropriate field here if possible
        documents = self.collection.find().sort("_id", -1).skip(start_index).limit(end_index - start_index + 1)

        dashData = {"pages": total_pages, "data": []}
        # Append documents to the data list
        
        documents.sort("_id", -1)
        for doc in documents:
            doc.pop("_id", None)
            print(len(doc["data"]))
            dashData["data"].append(doc)


        return dashData

    
