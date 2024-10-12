import os
from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any

# Load environment variables
load_dotenv()

# Initialize MongoDB client
client = MongoClient(os.getenv("MONGO_URI"))

app = FastAPI()

# Static database and collection names

def get_documents(database_name: str, collection_name: str, query: Optional[dict] = None) -> List[dict]:
    """
    Fetch documents from the specified MongoDB collection.
    """
    db = client[database_name]
    collection = db[collection_name]
    
    if query is None:
        documents = list(collection.find())
    else:
        documents = list(collection.find(query))
    
    return documents

@app.get("/documents", response_model=List[dict])
async def fetch_documents(query: Optional[str] = Query(None)):
    """
    Fetch documents from a MongoDB collection based on an optional query parameter.
    """
    try:
        # Convert query string to a dictionary if provided
        query_dict = eval(query) if query else None  # Be cautious with eval in production

        documents = get_documents("Deliveries", "deliveries", query_dict)
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

