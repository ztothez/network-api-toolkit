import requests
import json
import os

def get_ticket():
    requests.packages.urllib3.disable_warnings()
    api_url = "https://SandBoxAPICEM.cisco.com/api/v1/ticket"
    headers = {
        "content-type": "application/json"
    }
    body_json = {
        "username": "devnetuser",
        "password": os.getenv("PASSWORD")
    }
    resp = requests.post(api_url, json.dumps(body_json),  headers=headers,  verify=False)
    print("Ticket request status: ", resp.status_code)
    response_json = resp.json()
    serviceTicket = response_json["response"]["serviceTicket"] 
    print("The service ticket number is: ", serviceTicket)
    return serviceTicket
get_ticket()
