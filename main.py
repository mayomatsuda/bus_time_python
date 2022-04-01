# modules
from nbformat import read
import requests
from datetime import datetime, date

# store the URL
url = "http://gtfs.ltconline.ca/TripUpdate/TripUpdates.json"

# store the response of URL
response = requests.get(url)

# turn to json
tx = response.text

# get time of bus arrival at specific stop and route
def get_time(route, stop):

    times = []

    # lowest occurence of desired route
    ind1_low = tx.find('route_id":"' + route)
    if ind1_low == -1:
        ind1_low = tx.find('route_id": "' + route)

    # next occurence of desired route
    ind1_high = tx.find('route_id":"' + route, ind1_low + 1)
    if ind1_high == -1:
        ind1_high = tx.find('route_id": "' + route, ind1_low + 1)

    print("*** " + route + " at " + stop + " ***")

    while (True):
        
        # this will eventually happen, terminating the loop
        if (ind1_low == -1 or ind1_high == -1):
            return sorted(times)

        # ensure instance of the stop exists on the route
        here = tx.find(stop, ind1_low, ind1_high)
        if (here != -1):

            # find occurence of desired stop
            ind2 = tx.find('stop_id":"' + stop, ind1_low)
            if ind2 == -1:
                ind2 = tx.find('stop_id": "' + stop, ind1_low)

            # find occurence of time at most 50 characters before stop
            ind3 = tx.find('time', ind2 - 50)

            # convert UNIX time to UTC, then to EST
            timeunix = int(tx[ind3+6:ind3+16])
            hour = int(datetime.utcfromtimestamp(timeunix).strftime('%H'))
            if (daylightSavings):
                hour = str((hour - 4) % 12)
            else:
                hour = str((hour - 5) % 12)
            if (hour == '0'): hour = '12'
            minute = str(datetime.utcfromtimestamp(timeunix).strftime('%M'))
            time = hour + ":" + minute
            times.append(time)
        
        ind1_low = ind1_high
        ind1_high = tx.find('route_id":"' + route, ind1_low + 1)
        if ind1_high == -1:
            ind1_high = tx.find('route_id": "' + route, ind1_low + 1)

def isDaylightSavings():
    today = date.today()
    m = int(today.strftime("%m"))
    d = int(today.strftime("%d"))

    if (m >= 3 and m <= 11):
        if (m == 3):
            if (d >= 13):
                return True
        elif (m == 11):
            if (d <= 6):
                return True
        else:
            return True

# isDaylightSavings
daylightSavings = isDaylightSavings()

print(get_time("02", "WHARMOIR"))
print(get_time("102", "WHARMOIR"))