class CustomReportGroups:
    """
    Provides methods for interacting with Adesk Custom Report Groups (API v2).
    Accessed via `client.v2.custom_report_groups`.
    """
    def __init__(self, client):
        """
        Initializes the CustomReportGroups resource.

        Args:
            client (AdeskClient): The AdeskClient instance to use for API calls.
        """
        self.client = client

    def list(self, name=None, api_name=None, color=None, report_section=None):
        """
        Retrieves a list of custom report groups.
        Corresponds to Adesk API v2 endpoint: `GET custom-report-groups`.

        Args:
            name (str, optional): Filter by group name.
            api_name (str, optional): Filter by group API name (camelCase: apiName).
            color (str, optional): Filter by group color.
            report_section (str, optional): Filter by report section (camelCase: reportSection).

        Returns:
            list[dict]: A list of custom report group objects.
                        Returns an empty list if none are found or in case of an error.
        """
        params = {}
        if name is not None:
            params["name"] = name
        if api_name is not None:
            params["apiName"] = api_name # API expects camelCase
        if color is not None:
            params["color"] = color
        if report_section is not None:
            params["reportSection"] = report_section # API expects camelCase
        
        response = self.client.get_v2("custom-report-groups", params=params)
        return response.get("data", []) if response else []

    def create(self, groups_data):
        """
        Creates new custom report groups.
        Corresponds to Adesk API v2 endpoint: `POST custom-report-groups/create`.

        Args:
            groups_data (list[dict]): A list of dictionaries, where each dictionary
                                      represents a group to be created.
                                      Example: `[{"name": "Group 1", "apiName": "group1", "reportSection": "sales"}]`
                                      API may expect keys in camelCase (e.g., `apiName`).

        Returns:
            list[dict]: A list of the created custom report group objects.
                        Returns an empty list if the operation was unsuccessful or the response is empty.
        """
        # groups_data is a list of dicts. Keys should be camelCase if API requires.
        # Example: [{"name": "Group 1", "apiName": "group1", "reportSection": "sales"}]
        # Assuming requests library sends dict keys as-is.
        response = self.client.post_v2("custom-report-groups/create", json_data=groups_data)
        return response.get("data", []) if response else []

    def update(self, groups_data):
        """
        Updates existing custom report groups.
        Corresponds to Adesk API v2 endpoint: `POST custom-report-groups/update`.

        Args:
            groups_data (list[dict]): A list of dictionaries, where each dictionary
                                      represents a group to be updated and must include its `id`.
                                      Example: `[{"id": 1, "name": "Updated Group 1"}]`

        Returns:
            list[dict]: A list of the updated custom report group objects.
                        Returns an empty list if the operation was unsuccessful or the response is empty.
        """
        # groups_data is a list of dicts, each must include 'id'.
        # Example: [{"id": 1, "name": "Updated Group 1"}]
        response = self.client.post_v2("custom-report-groups/update", json_data=groups_data)
        return response.get("data", []) if response else []

    def remove(self, group_ids):
        """
        Removes custom report groups by their IDs.
        Corresponds to Adesk API v2 endpoint: `POST custom-report-groups/remove`.

        Args:
            group_ids (list[int]): A list of IDs of the custom report groups to remove.
                                   Example: `[1, 2, 3]`

        Returns:
            list[dict]: Typically an empty list or a list of remaining items,
                        depending on API behavior. May also be an empty list on error.
        """
        # group_ids is a list of IDs.
        # Example: [1, 2, 3]
        response = self.client.post_v2("custom-report-groups/remove", json_data=group_ids)
        return response.get("data", []) if response else []


class CustomReportEntries:
    """
    Provides methods for interacting with Adesk Custom Report Entries (API v2).
    Accessed via `client.v2.custom_report_entries`.
    """
    def __init__(self, client):
        """
        Initializes the CustomReportEntries resource.

        Args:
            client (AdeskClient): The AdeskClient instance to use for API calls.
        """
        self.client = client

    def list(self, name=None, api_name=None, value_type=None, group_id=None, report_section=None):
        """
        Retrieves a list of custom report entries.
        Corresponds to Adesk API v2 endpoint: `GET custom-report-entries`.

        Args:
            name (str, optional): Filter by entry name.
            api_name (str, optional): Filter by entry API name (camelCase: apiName).
            value_type (str, optional): Filter by value type (camelCase: valueType).
            group_id (int, optional): Filter by group ID (camelCase: groupId).
            report_section (str, optional): Filter by report section (camelCase: reportSection).

        Returns:
            list[dict]: A list of custom report entry objects.
                        Returns an empty list if none are found or in case of an error.
        """
        params = {}
        if name is not None:
            params["name"] = name
        if api_name is not None:
            params["apiName"] = api_name # API expects camelCase
        if value_type is not None:
            params["valueType"] = value_type # API expects camelCase
        if group_id is not None:
            params["groupId"] = group_id # API expects camelCase
        if report_section is not None:
            params["reportSection"] = report_section # API expects camelCase
            
        response = self.client.get_v2("custom-report-entries", params=params)
        return response.get("data", []) if response else []

    def create(self, entries_data):
        """
        Creates new custom report entries.
        Corresponds to Adesk API v2 endpoint: `POST custom-report-entries/create`.

        Args:
            entries_data (list[dict]): A list of dictionaries, where each dictionary
                                       represents an entry to be created.
                                       Example: `[{"name": "Entry 1", "apiName": "entry1", "groupId": 1}]`

        Returns:
            list[dict]: A list of the created custom report entry objects.
                        Returns an empty list if the operation was unsuccessful or the response is empty.
        """
        response = self.client.post_v2("custom-report-entries/create", json_data=entries_data)
        return response.get("data", []) if response else []

    def update(self, entries_data):
        """
        Updates existing custom report entries.
        Corresponds to Adesk API v2 endpoint: `POST custom-report-entries/update`.

        Args:
            entries_data (list[dict]): A list of dictionaries, where each dictionary
                                       represents an entry to be updated and must include its `id`.
                                       Example: `[{"id": 1, "name": "Updated Entry 1"}]`

        Returns:
            list[dict]: A list of the updated custom report entry objects.
                        Returns an empty list if the operation was unsuccessful or the response is empty.
        """
        response = self.client.post_v2("custom-report-entries/update", json_data=entries_data)
        return response.get("data", []) if response else []

    def remove(self, entry_ids):
        """
        Removes custom report entries by their IDs.
        Corresponds to Adesk API v2 endpoint: `POST custom-report-entries/remove`.

        Args:
            entry_ids (list[int]): A list of IDs of the custom report entries to remove.

        Returns:
            list[dict]: Typically an empty list or a list of remaining items.
                        May also be an empty list on error.
        """
        response = self.client.post_v2("custom-report-entries/remove", json_data=entry_ids)
        return response.get("data", []) if response else []


class CustomReportValues:
    """
    Provides methods for interacting with Adesk Custom Report Values (API v2).
    Accessed via `client.v2.custom_report_values`.
    """
    def __init__(self, client):
        """
        Initializes the CustomReportValues resource.

        Args:
            client (AdeskClient): The AdeskClient instance to use for API calls.
        """
        self.client = client

    def list(self, page=None, page_size=None, offset=None, entry_id=None, entry_api_name=None, 
               group_id=None, group_api_name=None, date_from=None, date_to=None, month=None, 
               type=None, project=None, business_unit=None, exact_business_unit=None):
        """
        Retrieves a list of custom report values with pagination and filtering.
        Corresponds to Adesk API v2 endpoint: `GET custom-report-values`.

        Args:
            page (int, optional): Page number for pagination.
            page_size (int, optional): Number of items per page (camelCase: pageSize).
            offset (int, optional): Offset for pagination.
            entry_id (int, optional): Filter by entry ID (camelCase: entryId).
            entry_api_name (str, optional): Filter by entry API name (camelCase: entryApiName).
            group_id (int, optional): Filter by group ID (camelCase: groupId).
            group_api_name (str, optional): Filter by group API name (camelCase: groupApiName).
            date_from (str, optional): Start date for filtering (YYYY-MM-DD) (camelCase: dateFrom).
            date_to (str, optional): End date for filtering (YYYY-MM-DD) (camelCase: dateTo).
            month (str, optional): Filter by month (YYYY-MM).
            type (str, optional): Filter by type.
            project (int, optional): Filter by project ID.
            business_unit (int, optional): Filter by business unit ID (camelCase: businessUnit).
            exact_business_unit (bool, optional): Exact match for business unit (camelCase: exactBusinessUnit).

        Returns:
            dict: The full response object from the API, which includes pagination details
                  and the list of custom report values under the "data" key.
                  Returns None if the request fails.
        """
        params = {}
        if page is not None: params["page"] = page
        if page_size is not None: params["pageSize"] = page_size # API expects camelCase
        if offset is not None: params["offset"] = offset
        if entry_id is not None: params["entryId"] = entry_id # API expects camelCase
        if entry_api_name is not None: params["entryApiName"] = entry_api_name # API expects camelCase
        if group_id is not None: params["groupId"] = group_id # API expects camelCase
        if group_api_name is not None: params["groupApiName"] = group_api_name # API expects camelCase
        if date_from is not None: params["dateFrom"] = date_from # API expects camelCase
        if date_to is not None: params["dateTo"] = date_to # API expects camelCase
        if month is not None: params["month"] = month
        if type is not None: params["type"] = type
        if project is not None: params["project"] = project
        if business_unit is not None: params["businessUnit"] = business_unit # API expects camelCase
        if exact_business_unit is not None: params["exactBusinessUnit"] = exact_business_unit # API expects camelCase
        
        # Returns the full response object
        return self.client.get_v2("custom-report-values", params=params)

    def create(self, values_data):
        """
        Creates new custom report values.
        Corresponds to Adesk API v2 endpoint: `POST custom-report-values/create`.

        Args:
            values_data (list[dict]): A list of dictionaries, where each dictionary
                                      represents a value to be created.
                                      Example: `[{"entryId": 1, "date": "2023-01-01", "value": 100.50}]`

        Returns:
            list[dict]: A list of the created custom report value objects.
                        Returns an empty list if the operation was unsuccessful or the response is empty.
        """
        response = self.client.post_v2("custom-report-values/create", json_data=values_data)
        return response.get("data", []) if response else [] # Assuming it also returns a 'data' field for consistency

    def update(self, values_data):
        """
        Updates existing custom report values.
        Corresponds to Adesk API v2 endpoint: `POST custom-report-values/update`.

        Args:
            values_data (list[dict]): A list of dictionaries, where each dictionary
                                      represents a value to be updated and must include its `id`.
                                      Example: `[{"id": 1, "value": 150.75}]`

        Returns:
            list[dict]: A list of the updated custom report value objects.
                        Returns an empty list if the operation was unsuccessful or the response is empty.
        """
        response = self.client.post_v2("custom-report-values/update", json_data=values_data)
        return response.get("data", []) if response else []

    def remove(self, value_ids):
        """
        Removes custom report values by their IDs.
        Corresponds to Adesk API v2 endpoint: `POST custom-report-values/remove`.

        Args:
            value_ids (list[int]): A list of IDs of the custom report values to remove.

        Returns:
            list[dict]: Typically an empty list or a list of remaining items.
                        May also be an empty list on error.
        """
        response = self.client.post_v2("custom-report-values/remove", json_data=value_ids)
        return response.get("data", []) if response else []


class CustomReportDebtEntries:
    """
    Provides methods for interacting with Adesk Custom Report Debt Entries (API v2).
    Accessed via `client.v2.custom_report_debt_entries`.
    """
    def __init__(self, client):
        """
        Initializes the CustomReportDebtEntries resource.

        Args:
            client (AdeskClient): The AdeskClient instance to use for API calls.
        """
        self.client = client

    def list(self):
        """
        Retrieves a list of custom report debt entries.
        Corresponds to Adesk API v2 endpoint: `GET custom-report-debt-entries`.

        Returns:
            list[dict]: A list of custom report debt entry objects.
                        Returns an empty list if none are found or in case of an error.
        """
        response = self.client.get_v2("custom-report-debt-entries")
        return response.get("data", []) if response else []

    def create(self, debt_entries_data):
        """
        Creates new custom report debt entries.
        Corresponds to Adesk API v2 endpoint: `POST custom-report-debt-entries/create`.

        Args:
            debt_entries_data (list[dict]): A list of dictionaries, where each dictionary
                                            represents a debt entry to be created.
                                            Example: `[{"name": "Debt Entry 1", "value": 1000}]`

        Returns:
            list[dict]: A list of the created custom report debt entry objects.
                        Returns an empty list if the operation was unsuccessful or the response is empty.
        """
        response = self.client.post_v2("custom-report-debt-entries/create", json_data=debt_entries_data)
        return response.get("data", []) if response else []

    def update(self, debt_entries_data):
        """
        Updates existing custom report debt entries.
        Corresponds to Adesk API v2 endpoint: `POST custom-report-debt-entries/update`.

        Args:
            debt_entries_data (list[dict]): A list of dictionaries, where each dictionary
                                            represents a debt entry to be updated and must include its `id`.
                                            Example: `[{"id": 1, "value": 1200}]`

        Returns:
            list[dict]: A list of the updated custom report debt entry objects.
                        Returns an empty list if the operation was unsuccessful or the response is empty.
        """
        response = self.client.post_v2("custom-report-debt-entries/update", json_data=debt_entries_data)
        return response.get("data", []) if response else []

    def remove(self, debt_entry_ids):
        """
        Removes custom report debt entries by their IDs.
        Corresponds to Adesk API v2 endpoint: `POST custom-report-debt-entries/remove`.

        Args:
            debt_entry_ids (list[int]): A list of IDs of the custom report debt entries to remove.

        Returns:
            list[dict]: Typically an empty list or a list of remaining items.
                        May also be an empty list on error.
        """
        response = self.client.post_v2("custom-report-debt-entries/remove", json_data=debt_entry_ids)
        return response.get("data", []) if response else []
