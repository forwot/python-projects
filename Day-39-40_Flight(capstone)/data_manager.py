import requests
import os
from dotenv import load_dotenv

PROJECT_NAME = "Flight Deals"
SHEET_NAME = "prices"
load_dotenv()

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.header = {
            "Authorization": os.environ.get("TOKEN")
        }
        self.prices_endpoint = os.environ.get("SHEETY_PRICES_ENDPOINT")
        self.users_endpoint = os.environ.get("SHEETY_USERS_ENDPOINT")
        self.destination_data = {}
        self.users_data = {}


    def get_prices_data(self):
        response = requests.get(url=self.prices_endpoint, headers=self.header)
        response.raise_for_status()
        self.destination_data = response.json()['prices']
        return self.destination_data

    def get_users_data(self):
        response = requests.get(url=self.users_endpoint, headers=self.header)
        response.raise_for_status()
        self.users_data = response.json()['users']
        return self.users_data

    def update_codes(self,row, data):
        update_endpoint = f"{self.prices_endpoint}/{row}"
        body = {
            "price":{
                'iataCode': data,
            }
        }
        response = requests.put(url=update_endpoint, headers=self.header, json=body)
        response.raise_for_status()

    def update_prices(self, row, data):
        update_endpoint = f"{self.prices_endpoint}/{row}"
        body = {
            "price": {
                'lowestPrice': data,
            }
        }
        response = requests.put(url=update_endpoint, headers=self.header, json=body)
        response.raise_for_status()
