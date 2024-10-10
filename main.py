import json
from fastapi import FastAPI, HTTPException, Query
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS middleware configuration to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Replace with your Google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Conversion factor from meters to kilometers
METERS_TO_KM = 0.001

class User(BaseModel):
    """
    Pydantic model to validate and serialize user data.

    Attributes:
    - name (str): Name of the user.
    - phone_number (str): Phone number of the user.
    - email (str): Email address of the user.
    - pick_up_details (dict): Details about the pickup location.
    - drop_off_details (dict): Details about the drop-off location.
    - schedule (dict): Scheduling details for the delivery.
    """
    name: str
    phone_number: str
    email: str
    pick_up_details: dict
    drop_off_details: dict
    schedule: dict

class MongoDB:
    def __init__(self):
        """
        Initializes the MongoDB client and specifies the database and collection.

        Loads the MongoDB URI from the environment variable.
        """
        uri = os.getenv("MONGO_URI")

        # Create a new client and connect to the server
        self.client = MongoClient(uri, server_api=ServerApi('1'))

        # Specify the database and collection
        self.db = self.client['Deliveries']  # Replace with your database name
        self.users_collection = self.db['users']  # Collection for user data

    def add_user(self, user_data: User):
        """
        Adds a new user to the users collection.

        Parameters:
        - user_data (User): The user data to be added.

        Returns:
        - str: The ID of the inserted document.
        """
        existing_user = self.users_collection.find_one({
            "name":user_data.name,
            "phone_number": user_data.phone_number,
            "email": user_data.email,
            "pick_up_details":user_data.pick_up_details,
            "drop_off_details":user_data.drop_off_details,
            "schedule":user_data.schedule,
        })
        
        # Insert the user data into the users collection
        if existing_user:
            result = self.users_collection.insert_one(user_data.model_dump())
        else:
            return "Already saved" 
        

        # Return the ID of the inserted document
        return str(result.inserted_id)

mongo_db = MongoDB()

@app.post("/add_user/")
async def create_user(user: User):
    """
    Endpoint to create a new user.

    Parameters:
    - user (User): User data to be added.

    Returns:
    - dict: A message indicating successful addition and the ID of the user.
    """

    try:
        user_id = mongo_db.add_user(user)
        return {"message": "User added successfully", "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_distance/")
async def get_distance(origin_place_id: str, destination_place_id: str):
    """
    Get distance between two places using Google Distance Matrix API.

    Parameters:
    - origin_place_id (str): Place ID of the origin.
    - destination_place_id (str): Place ID of the destination.

    Returns:
    - dict: Distance in miles between the origin and destination.
    """
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    
    # Build the query parameters for the Google Distance Matrix API
    params = {
        "origins": f"place_id:{origin_place_id}",
        "destinations": f"place_id:{destination_place_id}",
        "key": GOOGLE_API_KEY
    }
    
    # Make the GET request to Google API
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from Google API.")
    
    data = response.json()
    
    # Check if the response contains the distance information
    try:
        distance_meters = data["rows"][0]["elements"][0]["distance"]["value"]
        distance_miles = distance_meters * METERS_TO_KM
    except (IndexError, KeyError):
        raise HTTPException(status_code=500, detail="Distance data not available in the response.")
    
    return {"distance_miles": round(distance_miles, 2)}




@app.post("/create-payment-link")
async def create_payment_link(
    distance: float = Query(..., description="Distance of the delivery in km"),
    unitAmount: int = Query(..., description="Price of the delivery in smallest currency unit"),
    currency: str = Query("gbp", description="Currency for the payment"),
    origin: str = Query(..., description="Origin or the pickup location"),
    destination: str = Query(..., description="Destination or the drop off location")
):
    url = "https://auto-gen-payment-link-stripe.vercel.app/api/v1/create-payment-link"
    headers = {"Content-Type": "application/json"}
    
    body = {
        "productName": f"Delivery journey for {distance} km ",
        "productDescription": f"Delivery for a distance of {distance} km is less than 12km and any distance less than 12km is a standard delivery fee of 15(£) from {origin} to {destination} with a 5(£) pounds pickup fee" if (distance<12) else f"Delivery for a distance of {distance}km which is greater than 12km additional ({distance-12} * 1.75£) + 15£ flat rate + 5£ pickup rate from {origin} to {destination} " ,
        "unitAmount": f"{unitAmount}",
        "currency": currency,
        "quantity": "1"
    }

    try:
        response = requests.post(url, headers=headers, json=body)

        if response.status_code == 201:
            return response.json()['url']  # Return the payment link details
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Failed to create payment link {response.text}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")