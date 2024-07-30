from pymongo import MongoClient

# Connect to MongoDB (update the connection string as needed)
client = MongoClient("mongodb://localhost:27017" , username="myadmin", password="myadminpassword", authSource='admin')

# Select database and collection
db = client["user_database"]
collection = db["users"]

# JSON data (usually this comes from an external source or is already in JSON format)
users_data = [
    {   "repository" : "repo1",
        "secrets" :[
            {
                "username": "lavleshe",
                "email": "john@example.com",
                "profile": {
                    "name": "John Doe",
                    "age": 30,
                    "interests": ["coding", "hiking", "travel"]
                }
            },
            {
                "username": "lavleshe",
                "email": "john@example.com",
                "profile": {
                    "name": "John Doe",
                    "age": 30,
                    "interests": ["coding", "hiking", "travel"]
                }
            }
        ]
    }
]

# Insert data into the collection
collection.insert_many(users_data)
