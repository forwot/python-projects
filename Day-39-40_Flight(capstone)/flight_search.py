import os
import requests
from dotenv import load_dotenv
load_dotenv()

class FlightSearch:
    def __init__(self):
        self._api_key = os.environ.get("AMADEUS_APIKEY")
        self._api_secret = os.environ.get("APIKEY_SECRET")
        self._token = self.get_token()

    def get_token(self):
        token_endpoint = "https://test.api.amadeus.com/v1/security/oauth2/token"
        header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        body = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret
        }
        response = requests.post(url=token_endpoint, headers=header, data=body)
        response.raise_for_status()
        return response.json()['access_token']


    def get_destination_code(self, city_name):
        code_endpoint = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
        header = {
            "Authorization": f"Bearer {self._token}"
        }
        body = {
            "keyword": city_name,
            "max": 2,
            "include": "AIRPORTS"
        }
        try:
            response = requests.get(url=code_endpoint, headers=header, params=body)
            response.raise_for_status()
            data = response.json()
            iata_code = data['data'][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}")
            return "Not Found"
        return iata_code


    def check_flights(self, destination_iata, origin_iata, out_date, in_date, is_direct=True):

        flight_endpoint = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        header = {
            "Authorization": f"Bearer {self._token}"
        }
        if is_direct:
            body_direct = {
                "originLocationCode": origin_iata,
                "destinationLocationCode": destination_iata,
                "departureDate": out_date.strftime("%Y-%m-%d"),
                "returnDate": in_date.strftime("%Y-%m-%d"),
                "adults": 1,
                "currencyCode": "SGD",
                "nonStop": "true",
                "travelClass": "ECONOMY",
                "max": 10
            }
        else:
            body_direct = {
                "originLocationCode": origin_iata,
                "destinationLocationCode": destination_iata,
                "departureDate": out_date.strftime("%Y-%m-%d"),
                "returnDate": in_date.strftime("%Y-%m-%d"),
                "adults": 1,
                "currencyCode": "SGD",
                "travelClass": "ECONOMY",
                "max": 10
            }

        response = requests.get(url=flight_endpoint, headers=header, params=body_direct)

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            return None
        elif not response.json()['data']:
            print(f"No direct flights found for {destination_iata}.")
            return None
        return response.json()