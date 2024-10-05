from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Replace with your Google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Conversion factor from meters to miles
METERS_TO_Km = 0.001

@app.get("/get_distance/")
async def get_distance(origin_place_id: str, destination_place_id: str):
    """
    Get distance between two places using Google Distance Matrix API and return it in miles.
    
    Parameters:
    - origin_place_id: Place ID of the origin.
    - destination_place_id: Place ID of the destination.
    
    Returns:
    - Distance in miles.
    """
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    
    # Build the query parameters
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
        distance_miles = distance_meters * METERS_TO_Km
    except (IndexError, KeyError):
        raise HTTPException(status_code=500, detail="Distance data not available in the response.")
    
    return {"distance_miles": round(distance_miles, 2)}
