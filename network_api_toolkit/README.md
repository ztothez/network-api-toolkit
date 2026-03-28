# Network API Toolkit
A collection of Python-based networking and API integration tools built to explore real-world API usage, network data retrieval, and simple network-related automation.

This repository combines smaller projects into a cleaner toolkit structure for portfolio use and practical learning.

## Features
This toolkit includes multiple Python clients and utilities for working with external APIs and network-related data.

### API Clients
- **Cisco APIC-EM Client**  
  Retrieves and displays network devices and hosts from the Cisco APIC-EM sandbox API.

- **ISS Tracker**  
  Uses the Open Notify API to:
  - show the current ISS location
  - list people currently in space
  - calculate upcoming ISS passes for a location
  - optionally display the ISS on a Turtle map

- **MapQuest API Client**  
  Uses the MapQuest API for location and routing-related requests.

- **Shodan Client**  
  Retrieves public IP information and host intelligence data from the Shodan API.

- **Sunrise/Sunset Client**  
  Fetches sunrise and sunset data for a selected location using a public API.

### Network Tools
- **Cisco Path Analysis**  
  Utility for working with Cisco path trace data.

### Utilities
- **API Helpers**  
  Shared helper functions for authentication and API requests.

## Repository Structure
```text
network-api-toolkit/
├── api-clients/
│   ├── cisco_apicem_client.py
│   ├── iss_tracker.py
│   ├── mapquest_api_client.py
│   ├── shodan_client.py
│   └── sunrise_sunset_client.py
├── data/
│   ├── iss.gif
│   ├── map.gif
│   └── path_trace_data.json
├── network-tools/
│   └── cisco_path_analysis.py
├── utils/
│   └── api_helpers.py
└── README.md
```

## Requirements
Recommended Python version:

```bash
Python 3.10+
```

Install dependencies:
```bash
pip install requests shodan tabulate pgeocode python-dotenv
```

Standard library modules used include:
* `os`
* `json`
* `time`
* `urllib`
* `turtle`

## Environment Variables
Some scripts require API keys or credentials. These must not be hardcoded in the source code.

### Required variables
```env
SHODAN_API_KEY=your_shodan_api_key
MAPQUEST_API_KEY=your_mapquest_api_key
PASSWORD=your_cisco_sandbox_password
```

### Using a `.env` file (recommended)
Create a `.env` file in the project root:

```env
SHODAN_API_KEY=your_shodan_api_key
MAPQUEST_API_KEY=your_mapquest_api_key
PASSWORD=your_cisco_sandbox_password
```

Install the dependency:

```bash
pip install python-dotenv
```

Load variables in your scripts:

```python
from dotenv import load_dotenv
load_dotenv()
```

### Notes
* Never commit your `.env` file to version control
* Add `.env` to `.gitignore`
* Rotate keys immediately if they are exposed

## Notes
### ISS Tracker Assets
The Turtle-based ISS visualization requires the following files in the `data/` directory:

* `iss.gif`
* `map.gif`

If your script loads them by filename only, either:

* run the script from the correct directory, or
* update the code to use proper relative paths.

### Cisco APIC-EM Scripts
Cisco sandbox examples may require:

* a valid sandbox account
* a working authentication helper
* access to the Cisco DevNet sandbox environment

## Example Use Cases
* Practice working with REST APIs in Python
* Learn environment variable handling for secrets
* Explore network-oriented public APIs
* Build reusable API clients
* Improve project structure for a technical portfolio

## Why This Repository Exists
This project started as a set of smaller networking and information security exercises and was reorganized into a cleaner toolkit structure to better reflect practical Python API work.

The goal is to demonstrate:

* API integration skills
* network-focused scripting
* clean project organization
* secure handling of secrets via environment variables

## Future Improvements
Possible next steps:

* add command-line arguments for each client
* improve error handling and logging
* standardize output formatting across scripts
* create shared request/session helpers
* add unit tests
* package the toolkit for reuse