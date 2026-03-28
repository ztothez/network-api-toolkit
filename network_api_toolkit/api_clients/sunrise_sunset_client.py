import requests, time , pgeocode
from datetime import datetime, timedelta

def timeconv(time,name):
    in_time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z")
    localtime = in_time+timedelta(hours=timezone)
    out_time = localtime.strftime("%H:%M:%S")
    print(name+": "+out_time)
    print(in_time)
country = input("Add country code: ")
postalcode = input("Add postalcode: ")
nomi = pgeocode.Nominatim(country)
lists = nomi.query_postal_code(postalcode).tolist()
url = "https://api.sunrise-sunset.org/json?lat="+str(lists[9])+"&lng="+str(lists[10])+"&formatted=0"
timezone = int(time.strftime("%z").replace("0","").replace("+",""))
json_data = requests.get(url).json()
timeconv(json_data["results"]["sunrise"],"sunrise")
timeconv(json_data["results"]["sunset"],"sunset")

