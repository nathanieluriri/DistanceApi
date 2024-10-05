from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

class MongoDB:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        uri = os.getenv("MONGO_URI")

        # Create a new client and connect to the server
        self.client = MongoClient(uri, server_api=ServerApi('1'))

        # Specify the database and collection
        self.db = self.client['your_database_name']  # Replace with your database name
        self.users_collection = self.db['users']  # This is the collection where users will be stored

    def add_user(self, name: str, phone_number: str, email: str, pick_up_details: dict, drop_off_details: dict, schedule: dict):
        # Create a dictionary for the user data
        user_data = {
            'name': name,
            'phoneNumber': phone_number,
            'email': email,
            'pickUpDetails': pick_up_details,
            'dropOffDetails': drop_off_details,
            'schedule': schedule
        }

        # Insert the user data into the users collection
        result = self.users_collection.insert_one(user_data)

        # Return the ID of the inserted document
        return result.inserted_id

# Example usage
if __name__ == "__main__":
    mongo_db = MongoDB()

    # Add a user
    user_id = mongo_db.add_user(
        name="John Doe",
        phone_number="123-456-7890",
        email="john.doe@example.com",
        pick_up_details={"location": "123 Main St", "time": "10:00 AM"},
        drop_off_details={"location": "456 Elm St", "time": "11:00 AM"},
        schedule={"date": "2024-10-05", "recurring": False}
    )

    print(f"User added with ID: {user_id}")
