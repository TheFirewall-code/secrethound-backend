from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017", username="myadmin", password="myadminpassword", authSource='admin')

# Select the database to be deleted
db = client["Whitelist_Secret"]
        
# Delete the selected database
client.drop_database(db)
