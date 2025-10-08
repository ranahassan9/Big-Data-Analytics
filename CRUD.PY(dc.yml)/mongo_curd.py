from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get MongoDB credentials
MONGO_USER = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_PASS = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
MONGO_HOST = 'localhost'  # use 'mongo' if connecting from another Docker container
MONGO_PORT = 27017

# MongoDB URI
mongo_uri = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/"

# Connect to MongoDB
client = MongoClient(mongo_uri)

# Select database and collection
db = client['testdb']
collection = db['users']

# CRUD operations
def create_user(data):
    result = collection.insert_one(data)
    return result.inserted_id

def read_user(query):
    return collection.find_one(query)

def update_user(query, new_values):
    result = collection.update_one(query, {'$set': new_values})
    return result.modified_count

def delete_user(query):
    result = collection.delete_one(query)
    return result.deleted_count

# Test the CRUD functions
if __name__ == "__main__":
    print("Connecting to MongoDB and running CRUD operations...\n")

    # 1. Create
    user_data = {"name": "Alice", "email": "alice@example.com", "age": 25}
    user_id = create_user(user_data)
    print(f"User created with ID: {user_id}")

    # 2. Read
    user = read_user({"name": "Alice"})
    print("User found:", user)

    # 3. Update
    updated_count = update_user({"name": "Alice"}, {"age": 26})
    print(f"Updated {updated_count} user(s)")

    # 4. Delete
    deleted_count = delete_user({"name": "Alice"})
    print(f"Deleted {deleted_count} user(s)")
