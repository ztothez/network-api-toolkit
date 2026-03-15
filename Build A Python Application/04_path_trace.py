import requests
import json
import time
from tabulate import *

def get_ticket():
    requests.packages.urllib3.disable_warnings()
    api_url = "https://SandBoxAPICEM.cisco.com/api/v1/ticket"
    headers = {
        "content-type": "application/json"
    }
    body_json = {
        "username": "devnetuser",
        "password": "Cisco123!"
    }
    # Earlier vulnerable part: resp = requests.post(api_url, json.dumps(body_json), headers=headers, verify=False)
    # VULNERABLE: TLS certificate verification disabled (CWE-295)
    # Fixed due to Snyk analysis
    resp = requests.post(api_url, json.dumps(body_json), headers=headers, verify=True)
    response_json = resp.json()                   
    print("\n","Ticket request status: ", resp.status_code)
    response_json = resp.json()
    serviceTicket = response_json["response"]["serviceTicket"] 
    print("\n","The service ticket number is: ", serviceTicket)
    return serviceTicket
get_ticket()

def response():
    requests.packages.urllib3.disable_warnings()
    api_url = "https://sandboxapicem.cisco.com/api/v1/flow-analysis"
    ticket = get_ticket()
    headers = {
     "content-type": "application/json",
     "X-Auth-Token": ticket
    }
    # Earlier vulnerable part: resp = requests.get(api_url, headers=headers, verify=False)
    # VULNERABLE: TLS certificate verification disabled (CWE-295)
    # Fixed due to Snyk analysis
    resp = requests.get(api_url, headers=headers, verify=True)
    print("Status of /host request: ", resp.status_code)
    if resp.status_code != 200:
        raise Exception("Status code does not equal 200. Response text: " + resp.text)
    response_json = resp.json()
    trace_list = []
    i = 0
    for item in response_json["response"]:
         i+=1
         trace = [
                 i,
                 item["sourceIP"],
                 item["destIP"],
                 item["status"]
                ]
         trace_list.append( trace )
    table_header = ["Number", "SourceIP", "DestIP","Status"]
    print( tabulate(trace_list, table_header))

response()


