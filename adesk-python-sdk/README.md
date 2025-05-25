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

    # Example of accessing model attributes
    if projects: # Assuming 'projects' is a list of Project model instances
        first_project = projects[0]
        print(f"First project ID: {first_project.id}, Name: {first_project.name}")
        if first_project.category: # Accessing a nested model attribute
            print(f"Category: {first_project.category.name}")
    
    if created_project: # Assuming 'created_project' is a Project model instance
         project_id_from_model = created_project.id # Access attribute
         print(f"Created project ID from model: {project_id_from_model}")


except Exception as e:
    print(f"An API error occurred: {e}")
```

### Example: Working with API v2 Resources (Custom Report Groups)

```python
try:
    # List custom report groups
    report_groups = client.v2.custom_report_groups.list(report_section="finance")
    if report_groups: # report_groups is a list of CustomReportGroup model instances
        first_group = report_groups[0]
        print(f"First finance report group ID: {first_group.id}, Name: {first_group.name}, API Name: {first_group.api_name}")
    else:
        print("No finance report groups found.")

    # Create a new custom report group
    # Note: API v2 typically expects camelCase keys in the JSON body for requests.
    # The client methods send Python dicts as JSON.
    # The models initialize from API responses which might use camelCase or snake_case.
    new_group_payload = [{
        "name": "SDK Test Group",
        "apiName": "sdkTestGroup", 
        "reportSection": "general", 
        "color": "blue"
    }]
    created_groups = client.v2.custom_report_groups.create(new_group_payload)
    if created_groups: # created_groups is a list of CustomReportGroup model instances
        created_group = created_groups[0]
        print(f"Created custom report group ID: {created_group.id}, Name: {created_group.name}")
        group_id = created_group.id # Use the ID from the model instance

        # Update the group
        if group_id:
            update_data = [{"id": group_id, "name": "SDK Test Group (Updated)"}]
            updated_groups = client.v2.custom_report_groups.update(update_data)
            if updated_groups:
                print(f"Updated group name: {updated_groups[0].name}")

        # Remove the group (use with caution)
        # if group_id:
        #     remove_response = client.v2.custom_report_groups.remove([group_id])
        #     # remove methods usually return a raw dict response (e.g., {"success": True})
        #     print("Remove response:", remove_response) 
            
except Exception as e:
    print(f"An API v2 error occurred: {e}")
```

## Data Models

The SDK maps API responses to dedicated Python classes (data models) for easier use. 
Instead of dictionaries, methods that fetch data will typically return instances of these models, 
allowing attribute-style access (e.g., `my_project.name`). This provides benefits like 
easier attribute access and better integration with type hinting.

Primary models include:
*   `Project`, `ProjectCategory`
*   `TransactionCategory`
*   `BankAccount`
*   `Commitment`, `LegalEntity`, `Transfer`, `Operation`
*   `Contractor`, `Requisite`
*   `Product`, `Unit`, `Tag`, `Webhook`
*   And V2 models like `CustomReportGroup`, `CustomReportEntry`, `CustomReportValue`, `CustomReportValueList`, `CustomReportDebtEntry`.

These models are defined in the `adesk.models` module and can also be imported directly 
from `adesk` (e.g., `from adesk import Project`). Refer to the docstrings within each model 
class in `adesk/models/` for details on their attributes.

## Available Resources

The SDK provides access to various Adesk API resources, including:

**API v1 Resources (accessed via `client.<resource_name>`):**
*   `projects`: Manage projects and project categories. (Returns `Project`, `ProjectCategory` models)
*   `transaction_categories`: Manage categories for financial operations. (Returns `TransactionCategory` models)
*   `commitments`: Handle financial commitments. (Returns `Commitment` models)
*   `legal_entities`: Manage your organization's legal entities. (Returns `LegalEntity` models)
*   `bank_accounts`: Manage bank accounts and cash accounts. (Returns `BankAccount` models)
*   `operations`: Record financial operations (transactions). (Returns `Operation` models)
*   `transfers`: Manage transfers between bank accounts. (Returns `Transfer` models)
*   `contractors`: Manage contractors. (Returns `Contractor`, `Commitment`, `Requisite` models)
*   `requisites`: Manage contractor requisites. (Returns `Requisite` models)
*   `warehouse`: Manage products, services, units, and commodity expenses. (Returns `Product`, `Unit`, `CommodityCost`, `WarehouseShipmentModel` models)
*   `tags`: Manage tags. (Returns `Tag` models)
*   `webhooks`: Configure webhooks. (Returns `Webhook` models)

**API v2 Resources (accessed via `client.v2.<resource_name>`):**
*   `custom_report_groups`: Manage groups for custom reports. (Returns `CustomReportGroup` models)
*   `custom_report_entries`: Manage entries (rows/metrics) within custom report groups. (Returns `CustomReportEntry` models)
*   `custom_report_values`: Manage the actual data values for custom report entries. (Returns `CustomReportValueList` or lists of `CustomReportValue` models)
*   `custom_report_debt_entries`: Manage debt-related entries for custom reports. (Returns `CustomReportDebtEntry` models)

Please refer to the docstrings within each resource module and model class for detailed information on available methods, parameters, and model attributes.

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
