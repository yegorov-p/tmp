# Adesk Python SDK

A Python SDK for interacting with the Adesk API (v1 and v2).

## Installation

```bash
pip install adesk-python-sdk 
# Note: This assumes the package will be named 'adesk-python-sdk' on PyPI.
# If it's intended to be installed directly from git or as a local package, 
# installation instructions might differ.
```
You will also need to install the `requests` library if it's not already present:
```bash
pip install requests
```

## Usage

Initialize the client with your API token:

```python
from adesk import AdeskClient

# Replace "YOUR_API_TOKEN" with your actual Adesk API token
client = AdeskClient(api_token="YOUR_API_TOKEN")

# You can also specify custom base URLs for API v1 and v2 if needed:
# client = AdeskClient(
#     api_token="YOUR_API_TOKEN",
#     base_url="https://your-custom-v1-url/api/v1/",
#     base_url_v2="https://your-custom-v2-url/api/v2/"
# )
```

### Example: Working with API v1 Resources (Projects)

```python
# List all projects
try:
    projects = client.projects.list()
    if projects:
        print("First project:", projects[0])
    else:
        print("No projects found.")

    # List projects with specific status and manager
    # Assuming manager ID 123 exists
    managed_projects = client.projects.list(status="active", managers=[123])
    print(f"Active projects for manager 123: {len(managed_projects)}")

    # Create a new project
    new_project_data = {
        "name": "New SDK Project",
        "description": "A project created via the Python SDK",
        "category": 1, # Example category ID
        "manager": 123 # Example manager ID
    }
    created_project = client.projects.create(**new_project_data)
    if created_project:
        print("Created project:", created_project)
        project_id = created_project.get("id")

        # Update the project
        if project_id:
            updated_project = client.projects.update(project_id, description="Updated description for SDK project")
            print("Updated project:", updated_project)
        
        # Delete the project (use with caution)
        # if project_id:
        #     delete_response = client.projects.delete(project_id)
        #     print("Delete response:", delete_response)

except Exception as e:
    print(f"An API error occurred: {e}")
```

### Example: Working with API v2 Resources (Custom Report Groups)

```python
try:
    # List custom report groups
    report_groups = client.v2.custom_report_groups.list(report_section="finance")
    if report_groups:
        print("First finance report group:", report_groups[0])
    else:
        print("No finance report groups found.")

    # Create a new custom report group
    # Note: API v2 typically expects camelCase keys in the JSON body.
    # The _request_v2 method sends Python dicts as JSON; the 'requests' library
    # by default does not convert snake_case to camelCase.
    # Ensure your API v2 is flexible or adjust keys in the dict if needed.
    new_group_data = [{
        "name": "SDK Test Group",
        "apiName": "sdkTestGroup", # camelCase as per API v2 docs
        "reportSection": "general", # camelCase
        "color": "blue"
    }]
    created_groups = client.v2.custom_report_groups.create(new_group_data)
    if created_groups:
        print("Created custom report group(s):", created_groups)
        group_id = created_groups[0].get("id")

        # Update the group
        if group_id:
            update_data = [{"id": group_id, "name": "SDK Test Group (Updated)"}]
            updated_groups = client.v2.custom_report_groups.update(update_data)
            print("Updated group(s):", updated_groups)

        # Remove the group (use with caution)
        # if group_id:
        #     remove_response = client.v2.custom_report_groups.remove([group_id])
        #     print("Remove response:", remove_response)
            
except Exception as e:
    print(f"An API v2 error occurred: {e}")
```

## Available Resources

The SDK provides access to various Adesk API resources, including:

**API v1 Resources (accessed via `client.<resource_name>`):**
*   `projects`: Manage projects and project categories.
*   `transaction_categories`: Manage categories for financial operations.
*   `commitments`: Handle financial commitments (planned income/outcome).
*   `legal_entities`: Manage your organization's legal entities.
*   `bank_accounts`: Manage bank accounts and cash accounts.
*   `operations`: Record financial operations (transactions).
*   `transfers`: Manage transfers between bank accounts.
*   `contractors`: Manage contractors (clients, suppliers, etc.).
*   `requisites`: Manage contractor requisites (bank details).
*   `warehouse`: Manage products, services, units, and commodity expenses.
*   `tags`: Manage tags for categorizing various items.
*   `webhooks`: Configure webhooks for event notifications.

**API v2 Resources (accessed via `client.v2.<resource_name>`):**
*   `custom_report_groups`: Manage groups for custom reports.
*   `custom_report_entries`: Manage entries (rows/metrics) within custom report groups.
*   `custom_report_values`: Manage the actual data values for custom report entries.
*   `custom_report_debt_entries`: Manage debt-related entries for custom reports.

Please refer to the docstrings within each module/class for detailed information on available methods and parameters.

## API Versions

This SDK supports both Adesk API v1 and API v2.

*   **API v1:**
    *   Resources are accessed directly as attributes of the `AdeskClient` instance (e.g., `client.projects`).
    *   The default base URL is `https://api.adesk.ru/v1/`.
    *   Authentication is typically done by passing the `api_token` in query parameters for GET requests or in the request body for POST requests (`application/x-www-form-urlencoded`).

*   **API v2:**
    *   Resources are accessed via the `client.v2` namespace (e.g., `client.v2.custom_report_groups`).
    *   The default base URL is `https://api.adesk.ru/v2/`.
    *   Authentication is done via an `X-API-Token` header.
    *   Request and response bodies are typically JSON (`application/json`).

The client handles these differences internally. You can override the default base URLs during client initialization if necessary.

## Error Handling

The SDK methods will raise an `Exception` if an API error occurs (e.g., HTTP status code 4xx or 5xx) or if there's a network issue. The exception message will typically include details from the API response when available. It's recommended to wrap API calls in `try...except` blocks to handle potential errors gracefully.

## Contributing

We welcome contributions to improve and expand this SDK. If you have new features, bug fixes, or improvements, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your changes.
3.  Make your changes, including clear comments, docstrings, and tests (if applicable).
4.  Submit a pull request for review.

## License

This SDK is released under the MIT License. See the `LICENSE` file (if available, typically added to a project) for details.
