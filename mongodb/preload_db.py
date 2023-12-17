import pandas as pd
import os
import numpy as np
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient(os.getenv("MONGODB_URI"))
database = client[os.getenv("MONGODB_DATABASE")]
collection = database[os.getenv("MONGODB_COLLECTION")]

# Load CSV data into DataFrame
data = pd.read_csv("/usr/src/app/pokedex.csv", dtype=str)
data = data.replace({np.nan: ''})
print(data)
count = 0
for index, row in data.iterrows():
    pokemon_name = row['Pokemon']
    if not collection.find_one({"Pokemon": pokemon_name}):
        collection.insert_one(row.to_dict())
        count += 1
print(count)
collection_size = collection.estimated_document_count()
print(f"Size of the collection: {collection_size}")

# Insert
# try:
#     result = collection.insert_many(data.to_dict("records"))
#     print(f"Inserted {len(result.inserted_ids)} documents into collection '{os.getenv('MONGODB_COLLECTION')}'.")
# except Exception as e:
#     print(f"An error occurred while inserting documents: {e}")

