class CustomReportGroups:
    def __init__(self, client):
        self.client = client

    def list(self, name=None, api_name=None, color=None, report_section=None):
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
        # groups_data is a list of dicts. Keys should be camelCase if API requires.
        # Example: [{"name": "Group 1", "apiName": "group1", "reportSection": "sales"}]
        # Assuming requests library sends dict keys as-is.
        response = self.client.post_v2("custom-report-groups/create", json_data=groups_data)
        return response.get("data", []) if response else []

    def update(self, groups_data):
        # groups_data is a list of dicts, each must include 'id'.
        # Example: [{"id": 1, "name": "Updated Group 1"}]
        response = self.client.post_v2("custom-report-groups/update", json_data=groups_data)
        return response.get("data", []) if response else []

    def remove(self, group_ids):
        # group_ids is a list of IDs.
        # Example: [1, 2, 3]
        response = self.client.post_v2("custom-report-groups/remove", json_data=group_ids)
        return response.get("data", []) if response else []


class CustomReportEntries:
    def __init__(self, client):
        self.client = client

    def list(self, name=None, api_name=None, value_type=None, group_id=None, report_section=None):
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
        response = self.client.post_v2("custom-report-entries/create", json_data=entries_data)
        return response.get("data", []) if response else []

    def update(self, entries_data):
        response = self.client.post_v2("custom-report-entries/update", json_data=entries_data)
        return response.get("data", []) if response else []

    def remove(self, entry_ids):
        response = self.client.post_v2("custom-report-entries/remove", json_data=entry_ids)
        return response.get("data", []) if response else []


class CustomReportValues:
    def __init__(self, client):
        self.client = client

    def list(self, page=None, page_size=None, offset=None, entry_id=None, entry_api_name=None, 
               group_id=None, group_api_name=None, date_from=None, date_to=None, month=None, 
               type=None, project=None, business_unit=None, exact_business_unit=None):
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
        response = self.client.post_v2("custom-report-values/create", json_data=values_data)
        return response.get("data", []) if response else [] # Assuming it also returns a 'data' field for consistency

    def update(self, values_data):
        response = self.client.post_v2("custom-report-values/update", json_data=values_data)
        return response.get("data", []) if response else []

    def remove(self, value_ids):
        response = self.client.post_v2("custom-report-values/remove", json_data=value_ids)
        return response.get("data", []) if response else []


class CustomReportDebtEntries:
    def __init__(self, client):
        self.client = client

    def list(self):
        response = self.client.get_v2("custom-report-debt-entries")
        return response.get("data", []) if response else []

    def create(self, debt_entries_data):
        response = self.client.post_v2("custom-report-debt-entries/create", json_data=debt_entries_data)
        return response.get("data", []) if response else []

    def update(self, debt_entries_data):
        response = self.client.post_v2("custom-report-debt-entries/update", json_data=debt_entries_data)
        return response.get("data", []) if response else []

    def remove(self, debt_entry_ids):
        response = self.client.post_v2("custom-report-debt-entries/remove", json_data=debt_entry_ids)
        return response.get("data", []) if response else []
