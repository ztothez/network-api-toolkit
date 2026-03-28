import requests
from tabulate import tabulate
from api_helpers import get_ticket


BASE_URL = "https://sandboxapicem.cisco.com/api/v1"


def get_data(endpoint: str, headers: dict):
    """Fetch data from a given APIC-EM endpoint."""
    url = f"{BASE_URL}/{endpoint}"

    resp = requests.get(url, headers=headers, verify=True)
    print(f"Status of /{endpoint} request: {resp.status_code}")

    if resp.status_code != 200:
        raise Exception(f"Request failed: {resp.text}")

    return resp.json().get("response", [])


def parse_devices(data):
    """Extract device information."""
    device_list = []
    for i, item in enumerate(data, start=1):
        device_list.append([
            i,
            item.get("family", "n/a"),
            item.get("managementIpAddress", "n/a")
        ])
    return device_list


def parse_hosts(data):
    """Extract host information."""
    host_list = []
    for i, item in enumerate(data, start=1):
        host_list.append([
            i,
            item.get("hostType", "n/a"),
            item.get("hostIp", "n/a")
        ])
    return host_list


def print_table(title: str, data: list):
    """Print formatted table."""
    print(f"\n=== {title} ===")
    headers = ["Number", "Type", "IP"]
    print(tabulate(data, headers=headers))


def main():
    ticket = get_ticket()

    headers = {
        "content-type": "application/json",
        "X-Auth-Token": ticket
    }

    # Fetch and display devices
    devices_raw = get_data("network-device", headers)
    devices = parse_devices(devices_raw)
    print_table("Network Devices", devices)

    # Fetch and display hosts
    hosts_raw = get_data("host", headers)
    hosts = parse_hosts(hosts_raw)
    print_table("Hosts", hosts)


if __name__ == "__main__":
    main()