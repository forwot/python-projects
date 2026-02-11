class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, price, origin_airport, destination_airport, out_date, return_date, stops=0):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops

def find_cheapest(data):
    if not data or 'data' not in data or not data['data']:
        return "N/A"

    #data from first json
    first_flight = data['data'][0]
    lowest_price = float(first_flight["price"]["grandTotal"])
    origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    destination = first_flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
    out_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
    cheapest_flight = FlightData(
        price=lowest_price,
        origin_airport=origin,
        destination_airport=destination,
        out_date=out_date,
        return_date=return_date
    )

    for flight in data['data']:
        price = float(flight['price']['grandTotal'])
        if price < lowest_price:
            lowest_price = price
            # FIXED SECTION: These lines now reference the `flight` variable
            origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            destination = flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
            out_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
            cheapest_flight = FlightData(
                price=lowest_price,
                origin_airport=origin,
                destination_airport=destination,
                out_date=out_date,
                return_date=return_date
            )

    return cheapest_flight