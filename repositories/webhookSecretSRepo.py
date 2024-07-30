from pymongo import MongoClient
from models.webhookConfig import WebhookConfig
from fastapi.responses import FileResponse

import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Connect to MongoDB (update the connection string as needed)

class WebhookSecretSRepo :

    def __init__(self) :
        self.client = MongoClient(os.getenv("MONGO_URI"))
        # Select database and collection
        self.db = self.client["webhook"]
        self.collection = self.db["data"]

    def insertData(self, scanData : dict) :
        self.collection.insert_one(scanData) #for inserting the model we have to change it  to dict

    
    def deleteConfig(self) :
        count = self.collection.count_documents({})

        if count  < 1:
            return True  # Collection is not empty
        self.collection.delete_one({})
        return True
    

    def getData(self):
        scanData = []
        for document in self.collection.find():
            document.pop("_id", None)
            scanData.append(document)

        return {"scanData": scanData}

    def fetchSecretFile(self, date_of_scan) :
        print(date_of_scan)
        criteria = {
            'date_of_scan': date_of_scan
        }

        # Fetch documents matching the criteria
        matching_documents = self.collection.find(criteria)

        document = next(matching_documents, None)
        print(matching_documents)
        file_path =None
        if document:
            # Assuming 'secrets_link' is a field in your document
            file_path = document["secrets_link"]
    

        # Check if file exists
        if os.path.exists(str(file_path)):
            # Return the file contents in the response
            return FileResponse(path=file_path, media_type='application/x-yaml', filename="secret_report.yaml")
        else:
            # Return an error message if the file does not exist
            return 'File not found', 404
 