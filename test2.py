import json
from bson import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
import os

import pymongo
load_dotenv()
import pprint

# Replace 'your_connection_string' with your actual MongoDB connection string
client = MongoClient(os.getenv("MONGO_URI"))

# Select the database
db = client['Deliveries']
# Select the collection
collection = db['users']
# Find multiple documents


# Sample JSON data (as a string)
json_data = '''
{
  "successfulPayments": [
    {
      "id": "pi_3M2dtXDP8fjNWXz9M7p8Xr5v",
      "amount": 5999,
      "currency": "usd",
      "status": "succeeded",
      "created": "2024-10-05T15:43:25.000Z",
      "buyerEmail": "uririnathaniel@gmail.com",
      "buyerPhone": "08053964826",
      "buyerName": "Nat",
      "itemsBought": [
        {
          "productName": "Delivery journey for 9.23 km",
          "productDescription": "Delivery for a distance of 9.23 km is less than 12km and any distance less than 12km is a standard delivery fee of 15(£) from Maitama to Utako to be picked up at 20:35 2024-10-11 and dropped of at 2024-10-11 20:35  with a 5(£) pounds pickup fee",
          "quantity": 1
        }
      ]
    },
    {
      "id": "pi_3M2dtXDP8fjNWXz9M7p8Xr5d",
      "amount": 5999,
      "currency": "usd",
      "status": "succeeded",
      "created": "2024-10-05T15:43:25.000Z",
      "buyerEmail": "uririnathaniel@gmail.com",
      "buyerPhone": "08053964826",
      "buyerName": "Nat",
      "itemsBought": [
        {
          "productName": "Delivery journey for 9.23 km",
          "productDescription": "Delivery for a distance of 9.23 km is less than 12km and any distance less than 12km is a standard delivery fee of 15(£) from Maitama to Utako to be picked up at 09:20 2024-10-11 and dropped of at 2024-10-11 21:20  with a 5(£) pounds pickup fee",
          "quantity": 1
        }
      ]
    },
    {
      "id": "pi_3M2dtXDP8fjNWXz9M7p8Xr5c",
      "amount": 5999,
      "currency": "usd",
      "status": "succeeded",
      "created": "2024-10-05T15:43:25.000Z",
      "buyerEmail": "uririnathaniel@gmail.com",
      "buyerPhone": "08053964826",
      "buyerName": "Nathaniel Uriri",
      "itemsBought": [
        {
          "productName": "Delivery journey for 9.23 km",
          "productDescription": "Delivery for a distance of 9.23 km is less than 12km and any distance less than 12km is a standard delivery fee of 15(£) from Maitama to Maitama Junction to be picked up at 21:53 2024-10-10 and dropped of at 2024-10-10 08:55  with a 5(£) pounds pickup fee",
          "quantity": 1
        }
      ]
    }
  ]
}
'''

# Parse the JSON data
data = json.loads(json_data)

# Access the successfulPayments list
successful_payments = data['successfulPayments']

# Example comparison: Check if the payment status is 'succeeded' and the amount is greater than 5000
for payment in successful_payments:
    if payment['status'] == 'succeeded':
       documents = collection.find({'email': payment['buyerEmail']})  
       for doc in documents:  
          if  (doc['pick_up_details']['mainText'] in payment['itemsBought'][0]['productDescription']) and (doc['drop_off_details']['mainText']in payment['itemsBought'][0]['productDescription']) and (doc['schedule']['pickUpTime'] in payment['itemsBought'][0]['productDescription']) and (doc['schedule']['pickUpDate'] in payment['itemsBought'][0]['productDescription']) and (doc['schedule']['dropOffTime'] in payment['itemsBought'][0]['productDescription'])  and (doc['schedule']['dropOffDate'] in payment['itemsBought'][0]['productDescription'])  :
                documents = {'_id':payment['id'],
                            'name': payment['buyerName'],
                            'email': payment['buyerEmail'],
                            'amount':payment['amount'],
                            'phoneNumber':payment['buyerPhone'],
                            'pickupTime': doc['schedule']['pickUpTime'],
                            'pickupDate':doc['schedule']['pickUpDate'],
                            'dropoffTime':doc['schedule']['dropOffTime'],
                            'dropoffDate':doc['schedule']['dropOffDate'],
                            'dropoffLocation':doc['drop_off_details']['mainText'],
                            'pickupLocationSub':doc['pick_up_details']['subText'],
                            'dropoffLocationSub':doc['drop_off_details']['subText'],
                            'pickupLocation':doc['pick_up_details']['mainText'],
                            'origin_place_id':doc['pick_up_details']['placeId'],
                            'destination_place_id':doc['drop_off_details']['placeId'],
                            'status':"pick Up"
                            
                             }
                deliveries_collection = db['deliveries']
                try:
                    deliveries_collection.insert_one(document=documents)
                except pymongo.errors.DuplicateKeyError:
                    print("added before")
           

