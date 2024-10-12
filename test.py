import pprint
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize MongoDB client
client = MongoClient(os.getenv("MONGO_URI"))

def get_documents(database_name: str, collection_name: str, query: dict = None):
    """
    Fetch documents from the specified MongoDB collection.

    :param database_name: The name of the database.
    :param collection_name: The name of the collection.
    :param query: The query to filter documents (default is None for all documents).
    :return: List of documents matching the query.
    """
    # Select the database
    db = client[database_name]
    
    # Select the collection
    collection = db[collection_name]
    
    # Fetch documents based on the query
    if query is None:
        documents = list(collection.find())  # Get all documents if no query is provided
    else:
        documents = list(collection.find(query))  # Get documents that match the query
    
    return documents

# Example usage:
if __name__ == "__main__":
    database_name = 'Deliveries'
    collection_name = 'deliveries'
    
    # Get all documents from the 'users' collection
    all_documents = get_documents(database_name, collection_name)
    
    
    # Get documents with a specific query
    specific_query = {'status': 'pick Up'}  # Example query to get active users
    pick_up_orders = get_documents(database_name, collection_name, specific_query)

