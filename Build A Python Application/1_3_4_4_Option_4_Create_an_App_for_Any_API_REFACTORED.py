import os
import shodan
import requests

# ShodanClient Class for Encapsulating Shodan API Interaction
class ShodanClient:
    def __init__(self, api_key):
        self.api = shodan.Shodan(api_key)
    
    def get_host_info(self, ip):
        try:
            host = self.api.host(ip)
            return {
                'ip': host['ip_str'],
                'organization': host.get('org', 'n/a'),
                'os': host.get('os', 'n/a'),
                'banners': [{'port': item['port'], 'data': item['data']} for item in host['data']]
            }
        except shodan.APIError as e:
            print(f"Shodan API Error: {e}")
            return None

# Class for Fetching Public IP
class IPInfo:
    def __init__(self, api_key):
        self.url = f"https://api.shodan.io/tools/myip?key={api_key}"
    
    def get_public_ip(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            json_data = response.json()
            return json_data.get('ip', 'No IP found')
        except requests.RequestException as e:
            print(f"Error fetching public IP: {e}")
            return None

# Main Program
def main():
    # Retrieve API Key from Environment Variables
    SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")
    
    if not SHODAN_API_KEY:
        print("Shodan API key not found. Please set it in your environment variables.")
        return

    # Create instances of the classes
    shodan_client = ShodanClient(SHODAN_API_KEY)
    ip_info = IPInfo(SHODAN_API_KEY)

    # Fetch and display public IP
    public_ip = ip_info.get_public_ip()
    if public_ip:
        print("Public IP retrieved successfully.")

    # Fetch and display host information for a specific IP
    host_info = shodan_client.get_host_info('198.54.116.32')
    if host_info:
        print(f"""
        IP: {host_info['ip']}
        Organization: {host_info['organization']}
        Operating System: {host_info['os']}
        """)
        for banner in host_info['banners']:
            print(f"Port: {banner['port']}\nBanner: {banner['data']}\n")

if __name__ == "__main__":
    main()
