import csv
from pymongo import MongoClient

# Replace these variables with your MongoDB Atlas connection string and other details
CONNECTION_STRING = "mongodb+srv://richardli1793:Dog12345@cluster0.nopn49m.mongodb.net/"
DATABASE_NAME = "database1"
COLLECTION_NAME = "pokemon"
CSV_FILE_PATH = "./web_app/pokemon_csv/pokedex.csv"

def import_data():
    # Connect to MongoDB Atlas
    client = MongoClient(CONNECTION_STRING)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    print("HERE")


    # Read data from CSV file and insert into MongoDB
    with open(CSV_FILE_PATH, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            collection.insert_one(row)

    print("Data imported successfully.")

import_data()

# if __name__ == "__main__":
#     # Declare the client outside the function
#     client = MongoClient(CONNECTION_STRING)
#     import_data()

#     # Close MongoDB connection explicitly
#     client.close()
