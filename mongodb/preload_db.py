import pandas as pd
import os
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient(os.getenv("MONGODB_URI"))
database = client[os.getenv("MONGODB_DATABASE")]
collection = database[os.getenv("MONGODB_COLLECTION")]

# Load CSV data into DataFrame
data = pd.read_csv("/usr/src/app/pokedex.csv") 
print(data)

# Insert
try:
    result = collection.insert_many(data.to_dict("records"))
    print(f"Inserted {len(result.inserted_ids)} documents into collection '{os.getenv('MONGODB_COLLECTION')}'.")
except Exception as e:
    print(f"An error occurred while inserting documents: {e}")

