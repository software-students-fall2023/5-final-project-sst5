import pandas as pd
import os
import numpy as np
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient(os.getenv("MONGODB_URI"))
database = client[os.getenv("MONGODB_DATABASE")]
collection = os.getenv("MONGODB_COLLECTION")

if collection in database.list_collection_names():
    database[collection].drop()

# Load CSV data into DataFrame
data = pd.read_csv("/usr/src/app/pokedex.csv", dtype=str)
data = data.replace({np.nan: ''})
print(data)

collection = database[collection]

# Insert
try:
    result = collection.insert_many(data.to_dict("records"))
    print(f"Inserted {len(result.inserted_ids)} documents into collection '{os.getenv('MONGODB_COLLECTION')}'.")
except Exception as e:
    print(f"An error occurred while inserting documents: {e}")

