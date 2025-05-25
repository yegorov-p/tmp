# Adesk Python SDK

A Python SDK for interacting with the Adesk API.

## Installation

```bash
pip install adesk-python-sdk
```

## Usage

```python
from adesk import AdeskClient

client = AdeskClient(api_token="YOUR_API_TOKEN")

# Example: Get list of projects
projects = client.projects.list()
print(projects)
```
