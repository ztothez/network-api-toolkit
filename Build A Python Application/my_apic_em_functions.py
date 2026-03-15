import requests
import json
import os
from tabulate import *

def get_ticket():
    requests.packages.urllib3.disable_warnings()
    api_url = "https://SandBoxAPICEM.cisco.com/api/v1/ticket"
    headers = {
        "content-type": "application/json"
    }
    body_json = {
        "username": "devnetuser",
        "password": os.environ["PASSWORD"]
    }
    resp=requests.post(api_url, json.dumps(body_json),  headers=headers,  verify=True)
    response_json = resp.json()                   
    print("\n","Ticket request status: ", resp.status_code)
    response_json = resp.json()
    serviceTicket = response_json["response"]["serviceTicket"] 
    print("\n","The service ticket number is: ", serviceTicket)
    return serviceTicket
get_ticket()

def print_host():
    api_url = "https://sandboxapicem.cisco.com/api/v1/host"
    ticket = get_ticket()
    headers = {
     "content-type": "application/json",
     "X-Auth-Token": ticket
    }

    resp = requests.get(api_url, headers=headers, verify=True)
    response_json = resp.json()
    host_list = []
    i = 0
    for item in response_json["response"]:
         i+=1
         host = [
                 i,
                 item["hostType"],
                 item["hostIp"] 
                ]
         host_list.append( host )
    table_header = ["Number", "Type", "IP"]
    print("\n", tabulate(host_list, table_header))
print_host()


def print_device():
    api_url = "https://sandboxapicem.cisco.com/api/v1/network-device"
    ticket = get_ticket()
    headers = {
     "content-type": "application/json",
     "X-Auth-Token": ticket
    }

    resp = requests.get(api_url, headers=headers, verify=True)
    print("\n","Status of /host request: ", resp.status_code)
    if resp.status_code != 200:
        raise Exception("Status code does not equal 200. Response text: " + resp.text)
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
    print("\n", tabulate(device_list, table_header))
print_device()
