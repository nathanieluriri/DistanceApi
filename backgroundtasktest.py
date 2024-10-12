from bson import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import requests
import pymongo
from fastapi import FastAPI
import asyncio

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Replace 'your_connection_string' with your actual MongoDB connection string
client = MongoClient(os.getenv("MONGO_URI"))

# Select the database and collection


async def process_successful_payments():
    while True:
        db = client['Deliveries']
        collection = db['users']
        # Fetch the data from the API
        response = requests.get('https://auto-gen-payment-link-stripe.vercel.app/api/v1/successful-payments')

        # Check if the request was successful
        if response.status_code == 200:
            json_data = response.json()  # Parse the JSON response
        else:
            print(f"Error: {response.status_code} - {response.text}")
            await asyncio.sleep(20)  # Wait for 20 seconds before retrying
            continue  # Exit the loop to retry

        # Access the successfulPayments list
        successful_payments = json_data['successfulPayments']
        

        for payment in successful_payments:
            if payment['status'] == 'succeeded':
                documents = collection.find({'email': payment['buyerEmail']})
                for doc in documents:
                    if (doc['pick_up_details']['mainText'] in payment['itemsBought'][0]['productDescription']) and \
                       (doc['drop_off_details']['mainText'] in payment['itemsBought'][0]['productDescription']) and \
                       (doc['schedule']['pickUpTime'] in payment['itemsBought'][0]['productDescription']) and \
                       (doc['schedule']['pickUpDate'] in payment['itemsBought'][0]['productDescription']) and \
                       (doc['schedule']['dropOffTime'] in payment['itemsBought'][0]['productDescription']) and \
                       (doc['schedule']['dropOffDate'] in payment['itemsBought'][0]['productDescription']):
                        
                        # Create a document to insert
                        document = {
                            '_id': payment['id'],
                            'name': payment['buyerName'],
                            'email': payment['buyerEmail'],
                            'amount': payment['amount'],
                            'phoneNumber': payment['buyerPhone'],
                            'pickupTime': doc['schedule']['pickUpTime'],
                            'pickupDate': doc['schedule']['pickUpDate'],
                            'dropoffTime': doc['schedule']['dropOffTime'],
                            'dropoffDate': doc['schedule']['dropOffDate'],
                            'dropoffLocation': doc['drop_off_details']['mainText'],
                            'pickupLocationSub': doc['pick_up_details']['subText'],
                            'dropoffLocationSub': doc['drop_off_details']['subText'],
                            'pickupLocation': doc['pick_up_details']['mainText'],
                            'origin_place_id': doc['pick_up_details']['placeId'],
                            'destination_place_id': doc['drop_off_details']['placeId'],
                            'status': "pick Up"
                        }
                        
                        deliveries_collection = db['deliveries']
                        try:
                            deliveries_collection.insert_one(document=document)
                        except pymongo.errors.DuplicateKeyError:
                            print("Document already added before")
        
        # Wait for 20 seconds before the next iteration
        await asyncio.sleep(20)


# Create a simple endpoint to check if the server is running
@app.get("/")
async def read_root():
    asyncio.create_task(process_successful_payments())
    return {"message": "Payment processing is running in the background."}

# Run the application
# If using command line, run with: uvicorn filename:app --reload
