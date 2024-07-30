from pymongo import MongoClient, DESCENDING

import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Connect to MongoDB (update the connection string as needed)

class LogRepo :

    def __init__(self) :
        self.client = MongoClient(os.getenv("MONGO_URI"))
        # Select database and collection
        self.db = self.client["Logs"]
        self.collection = self.db["middleware_logs"]
    

    def insertLogs(self, logs) :
        self.collection.insert_one(logs)


    def getLogs(self, start_index, end_index) :
        logs = []
        documents = self.collection.find().sort([("_id", DESCENDING)]).skip(start_index).limit(end_index - start_index + 1)
        for document in documents :
            document.pop("_id", None)
            logs.append(document)

        return {"logs" : logs}