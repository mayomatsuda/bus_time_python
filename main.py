# modules
import json
import requests
import ast
from datetime import datetime

# store the URL
url = "http://gtfs.ltconline.ca/TripUpdate/TripUpdates.json"
  
# store the response of URL
response = requests.get(url)

# turn to json
tx = response.text

# get time of bus arrival at specific stop and route
def get_time(route, stop):

    found = False
    ind1_low = tx.find('route_id":"' + route)
    ind1_high = tx.find('route_id":"' + route, ind1_low)
    print("*** " + route + " at " + stop + " ***")

    while (not found):
        print(ind1_low)
        here = tx.find(stop, ind1_low, ind1_high)
        if (here != -1):
            found = True
            ind2 = tx.find('stop_id":"' + stop, ind1_low)
            ind3 = tx.find('time', ind2 - 50)
            timeunix = int(tx[ind3+6:ind3+16])
            hour = int(datetime.utcfromtimestamp(timeunix).strftime('%H'))
            hour = str(hour - 5)
            minute = str(datetime.utcfromtimestamp(timeunix).strftime('%M'))
            time = hour + ":" + minute
            print(time)
        else:
            ind1_low = ind1_high
            ind1_high = tx.find('route_id":"' + route, ind1_low)

    # print(time)

get_time("02", "WHARMOIR")
get_time("102", "WHARMOIR")