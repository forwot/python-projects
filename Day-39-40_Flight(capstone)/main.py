from data_manager import DataManager
from flight_search import FlightSearch
import time
from flight_data import find_cheapest
import datetime as dt
from notification_manager import NotificationManager

ORIGIN_IATA = "SIN"

data_manager = DataManager()
sheets_data = data_manager.get_prices_data()

#sheets_data = [{'city': 'Paris', 'iataCode': 'PAR', 'lowestPrice': 1272.5, 'id': 2}, {'city': 'Frankfurt', 'iataCode': 'FRA', 'lowestPrice': 1769.5, 'id': 3}, {'city': 'Tokyo', 'iataCode': 'TYO', 'lowestPrice': 746.5, 'id': 4}, {'city': 'Hong Kong', 'iataCode': 'HKG', 'lowestPrice': 463.1, 'id': 5}, {'city': 'Istanbul', 'iataCode': 'IST', 'lowestPrice': 1340.3, 'id': 6}, {'city': 'Kuala Lumpur', 'iataCode': 'KUL', 'lowestPrice': 193.7, 'id': 7}, {'city': 'New York', 'iataCode': 'NYC', 'lowestPrice': 10716.3, 'id': 8}, {'city': 'San Francisco', 'iataCode': 'SFO', 'lowestPrice': 1396.2, 'id': 9}, {'city': 'Madrid', 'id': 10}]
flight_search = FlightSearch()
notification_manager = NotificationManager()

users_data = data_manager.get_users_data()

# ==================== Update the Airport Codes in Google Sheet ====================
for row in sheets_data:
    if 'iataCode' not in row or row['iataCode'] == "":
        row_id = row['id']
        iata = flight_search.get_destination_code(row['city'])
        data_manager.update_codes(row=row_id, data=iata)
        time.sleep(2)   #slow down requests to avoid rate limit
        print(f"iatacode has been inputted for {row['city']}")

# ==================== Search for Flights and Send Notifications ====================
tmr = dt.datetime.now() + dt.timedelta(days = 1)
six_months = dt.datetime.now() + dt.timedelta(days = 180)

for destination in sheets_data:
    iata = destination['iataCode']
    flights = flight_search.check_flights(destination_iata=iata,
                                          origin_iata=ORIGIN_IATA,
                                          out_date=tmr,
                                          in_date=six_months
                                          )
    #if there are no non-stop flights
    if flights is None:
        flights = flight_search.check_flights(destination_iata=iata,origin_iata=ORIGIN_IATA,out_date=tmr,in_date=six_months,
                                              is_direct=False
                                              )
        print(f"non-stop: {flights}")
    cheapest_flight = find_cheapest(flights)

#SEND EMAIL
    if cheapest_flight == "N/A":
        print(f"No flights found for {destination['city']}.")
        data_manager.update_prices(row=destination['id'], data=cheapest_flight)
        print(f"updated prices for {destination['city']}")
        time.sleep(2)  # slow down requests to avoid rate limit
    else:
        if float(cheapest_flight.price) < float(destination['lowestPrice']):
            # update prices
            data_manager.update_prices(row=destination['id'], data=cheapest_flight.price)
            print(f"updated prices for {destination['city']}")
            time.sleep(2)  # slow down requests to avoid rate limit

            msg_body = f"Subject:Low Price Alert!\n\n" \
                       f"Only SGD${cheapest_flight.price} to fly from {ORIGIN_IATA} to {iata}," \
                       f"on {tmr.strftime('%Y-%m-%d')} until {six_months.strftime('%Y-%m-%d')}"

            # 2. Create a list of all user emails
            email_list = [row["what'sYourEmail?"] for row in users_data]

            # 3. Send one email to all users
            notification_manager.send_alert(msg_body, email_list)
