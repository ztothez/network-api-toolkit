import requests
import json
from tabulate import *
from my_apic_em_functions import *

api_url = "https://sandboxapicem.cisco.com/api/v1/network-device"
ticket = get_ticket()
headers = {
 "content-type": "application/json",
 "X-Auth-Token": ticket
}

resp = requests.get(api_url, headers=headers, verify=True)
print("Status of /host request: ", resp.status_code,"\n")
if resp.status_code != 200:
    raise Exception("Status code does not equal 200. Response text: " + resp.text,"\n")
response_json = resp.json()
device_list = []
i = 0
for item in response_json["response"]:
     i+=1
     device = [
             i,
             item["family"],
             item["managementIpAddress"] 
            ]
     device_list.append( device )
table_header = ["Number", "Type", "IP"]
print( tabulate(device_list, table_header))
