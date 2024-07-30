from pymongo import MongoClient

# Connect to MongoDB (update the connection string as needed)
client = MongoClient("mongodb://localhost:27017/", username="myadmin", password="myadminpassword", authSource='admin')


# Select database and collection
db = client["Dashboard"]
collection = db["dash"]



#users_with_interest_travel = collection.find({"profile.interests": "travel"})
#for user in users_with_interest_travel:
#    print(user)

for document in collection.find():
    print(len(document["data"]))