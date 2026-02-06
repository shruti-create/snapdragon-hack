import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
db_name = os.getenv("MONGO_DB", "snapdragon")

client = MongoClient(mongo_uri)
db = client[db_name]

# Path to the exercise dataset
dataset_path = r"C:\Users\QCWorkshop9\Desktop\exercise_dataset"


def import_json_file(file_name, collection_name):
    """Import JSON data from a file into a MongoDB collection."""
    file_path = os.path.join(dataset_path, file_name)
    
    if not os.path.exists(file_path):
        print(f"⚠️  File not found: {file_path}")
        return
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if not data:
        print(f"⚠️  No data found in {file_name}")
        return
    
    collection = db[collection_name]
    
    # Clear existing data
    collection.delete_many({})
    
    # Insert new data
    result = collection.insert_many(data)
    print(f"✓ Imported {len(result.inserted_ids)} documents into '{collection_name}' collection")


def main():
    print("Starting data import into MongoDB...\n")
    
    # Import all JSON files
    import_json_file("exercises.json", "exercises")
    import_json_file("bodyParts.json", "bodyParts")
    import_json_file("equipments.json", "equipments")
    import_json_file("muscles.json", "muscles")
    
    print("\n✅ Data import completed!")
    
    # Display summary
    print("\n📊 Collection Summary:")
    for collection_name in ["exercises", "bodyParts", "equipments", "muscles"]:
        count = db[collection_name].count_documents({})
        print(f"  - {collection_name}: {count} documents")
    
    client.close()


if __name__ == "__main__":
    main()
