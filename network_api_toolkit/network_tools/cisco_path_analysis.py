import json
import os
import sys
import time
from typing import Any

import requests
from tabulate import tabulate

BASE_URL = "https://sandboxapicem.cisco.com/api/v1"
USERNAME = "devnetuser"
PASSWORD_ENV = "PASSWORD"
POLL_INTERVAL = 1
POLL_TIMEOUT = 20


def get_ticket() -> str:
    password = os.environ.get(PASSWORD_ENV)
    if not password:
        raise RuntimeError(f"Environment variable {PASSWORD_ENV} is not set")

    url = f"{BASE_URL}/ticket"
    headers = {"content-type": "application/json"}
    body = {"username": USERNAME, "password": password}

    resp = requests.post(url, json=body, headers=headers, verify=True, timeout=30)
    resp.raise_for_status()

    response_json = resp.json()
    service_ticket = response_json["response"]["serviceTicket"]
    print(f"Ticket request status: {resp.status_code}")
    return service_ticket


def api_get(endpoint: str, token: str) -> requests.Response:
    url = f"{BASE_URL}/{endpoint}"
    headers = {
        "content-type": "application/json",
        "X-Auth-Token": token,
    }
    return requests.get(url, headers=headers, verify=True, timeout=30)


def api_post(endpoint: str, token: str, data: dict[str, Any]) -> requests.Response:
    url = f"{BASE_URL}/{endpoint}"
    headers = {
        "content-type": "application/json",
        "X-Auth-Token": token,
    }
    return requests.post(url, json=data, headers=headers, verify=True, timeout=30)


def get_hosts(token: str) -> list[list[str]]:
    resp = api_get("host", token)
    resp.raise_for_status()
    response_json = resp.json()

    hosts: list[list[str]] = []
    for item in response_json.get("response", []):
        hosts.append(["host", item.get("hostIp", "UNKNOWN")])
    return hosts


def get_devices(token: str) -> list[list[str]]:
    resp = api_get("network-device", token)
    resp.raise_for_status()
    response_json = resp.json()

    devices: list[list[str]] = []
    for item in response_json.get("response", []):
        devices.append(["network device", item.get("managementIpAddress", "UNKNOWN")])
    return devices


def get_host_and_device(token: str) -> list[list[str]]:
    combined: list[list[str]] = []
    idx = 1

    for item_type, ip in get_hosts(token):
        combined.append([idx, item_type, ip])
        idx += 1

    for item_type, ip in get_devices(token):
        combined.append([idx, item_type, ip])
        idx += 1

    return combined


def select_ip(prompt: str, ip_list: list[list[Any]], ip_index: int) -> str:
    while True:
        user_input = input(prompt).strip()

        if user_input.lower() == "exit":
            sys.exit(0)

        if not user_input.isdigit():
            print("Oops! input is not a digit, please try again or enter 'exit'")
            continue

        choice = int(user_input)
        if 1 <= choice <= len(ip_list):
            return str(ip_list[choice - 1][ip_index])

        print("Oops! number is out of range, please try again or enter 'exit'")


def start_flow_analysis(token: str, source_ip: str, dest_ip: str) -> str:
    path_data = {"sourceIP": source_ip, "destIP": dest_ip}
    resp = api_post("flow-analysis", token, path_data)
    resp.raise_for_status()

    response_json = resp.json()
    print("Response from POST /flow-analysis:")
    print(json.dumps(response_json, indent=4))

    flow_analysis_id = response_json["response"]["flowAnalysisId"]
    return flow_analysis_id


def poll_flow_analysis(token: str, flow_analysis_id: str) -> dict[str, Any]:
    start_time = time.time()

    while True:
        resp = api_get(f"flow-analysis/{flow_analysis_id}", token)
        resp.raise_for_status()
        response_json = resp.json()

        status = response_json["response"]["request"]["status"]
        print(f"\n**** Check status here: {status} ****\n")

        if status == "COMPLETED":
            return response_json

        if status == "FAILED":
            raise RuntimeError(
                "Unable to find full path. No traceroute or netflow information found."
            )

        if time.time() - start_time > POLL_TIMEOUT:
            raise TimeoutError(
                "Script timed out, no routing path was found. Please try different source/destination."
            )

        time.sleep(POLL_INTERVAL)


def print_flow_summary(flow_response: dict[str, Any]) -> None:
    request = flow_response["response"]["request"]
    print("Flow Analysis Summary")
    print(
        tabulate(
            [[
                request.get("sourceIP", "UNKNOWN"),
                request.get("destIP", "UNKNOWN"),
                request.get("status", "UNKNOWN"),
                request.get("id", "UNKNOWN"),
            ]],
            headers=["Source IP", "Destination IP", "Status", "FlowAnalysisId"],
            tablefmt="rst",
        )
    )


def print_path_details(flow_response: dict[str, Any]) -> None:
    elements = flow_response["response"].get("networkElementsInfo", [])
    rows = []

    for i, item in enumerate(elements, start=1):
        rows.append([
            i,
            item.get("name", "UNKNOWN"),
            item.get("type", "UNKNOWN"),
            item.get("ip", "UNKNOWN"),
            item.get("role", "UNKNOWN"),
            item.get("linkInformationSource", "UNKNOWN"),
        ])

    print("\nPath Details")
    print(
        tabulate(
            rows,
            headers=["#", "Name", "Type", "IP", "Role", "Link Source"],
            tablefmt="rst",
        )
    )


def main() -> None:
    try:
        token = get_ticket()
        nd_list = get_host_and_device(token)

        if len(nd_list) < 2:
            print("We need at least 2 hosts or network devices to perform path trace.")
            sys.exit(1)

        print(tabulate(nd_list, headers=["number", "type", "ip"], tablefmt="rst"))
        print("*** Note: not all source/destination IP pairs will return a valid path. ***\n")

        ip_idx = 2
        source_ip = select_ip(
            "=> Select a number for the source IP from above list: ",
            nd_list,
            ip_idx,
        )
        dest_ip = select_ip(
            "=> Select a number for the destination IP from above list: ",
            nd_list,
            ip_idx,
        )

        flow_analysis_id = start_flow_analysis(token, source_ip, dest_ip)
        flow_response = poll_flow_analysis(token, flow_analysis_id)

        print("\nResponse from GET /flow-analysis/{flowAnalysisId}:")
        print(json.dumps(flow_response, indent=4))

        print_flow_summary(flow_response)
        print_path_details(flow_response)

        print("\n------ End of path trace ! ------")

    except Exception as exc:
        print(f"\nError: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()