import os
import requests
import shodan


class ShodanClient:
    """Simple client for interacting with the Shodan API."""

    def __init__(self, api_key: str):
        self.api = shodan.Shodan(api_key)

    def get_host_info(self, ip: str):
        """Fetch host information for a given IP address."""
        try:
            host = self.api.host(ip)
            return {
                "ip": host.get("ip_str", "n/a"),
                "organization": host.get("org", "n/a"),
                "os": host.get("os", "n/a"),
                "banners": [
                    {
                        "port": item.get("port", "n/a"),
                        "data": item.get("data", "").strip(),
                    }
                    for item in host.get("data", [])
                ],
            }
        except shodan.APIError as e:
            print(f"Shodan API error: {e}")
            return None


class IPInfo:
    """Fetch the public IP address using Shodan's myip endpoint."""

    def __init__(self, api_key: str):
        self.url = f"https://api.shodan.io/tools/myip?key={api_key}"

    def get_public_ip(self):
        """Return the public IP as plain text."""
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            return response.text.strip()
        except requests.RequestException as e:
            print(f"Error fetching public IP: {e}")
            return None


def main():
    shodan_api_key = os.getenv("SHODAN_API_KEY")

    if not shodan_api_key:
        print("Shodan API key not found. Please set SHODAN_API_KEY in your environment variables.")
        return

    target_ip = "198.54.116.32"

    shodan_client = ShodanClient(shodan_api_key)
    ip_info = IPInfo(shodan_api_key)

    public_ip = ip_info.get_public_ip()
    if public_ip:
        print(f"My public IP is: {public_ip}\n")

    host_info = shodan_client.get_host_info(target_ip)
    if host_info:
        print(
            f"""IP: {host_info['ip']}
Organization: {host_info['organization']}
Operating System: {host_info['os']}
"""
        )

        for banner in host_info["banners"]:
            print(f"Port: {banner['port']}")
            print(f"Banner:\n{banner['data']}\n")


if __name__ == "__main__":
    main()