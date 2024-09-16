import pymongo
import json

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Adjust the URI as needed
db = client['ElsaQuiz']  # Database name
questions_collection = db['questions']  # Collection name

# Read data from the JSON file
with open('mock-questions.json', 'r') as file:
    questions_data = json.load(file)

# Insert the data into the questions collection
try:
    if isinstance(questions_data, list):
        insert_result = questions_collection.insert_many(questions_data)
        print(f"Inserted {len(insert_result.inserted_ids)} documents.")
    else:
        insert_result = questions_collection.insert_one(questions_data)
        print(f"Inserted document with id {insert_result.inserted_id}.")
except Exception as e:
    print(f"An error occurred: {e}")
