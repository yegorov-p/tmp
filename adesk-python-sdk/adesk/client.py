import requests
from .transactions import TransactionCategories
from .projects import Projects
from .commitments import Commitments
from .legal_entities import LegalEntities
from .bank_accounts import BankAccounts
from .transfers import Transfers
from .operations import Operations
from .contractors import Contractors
from .requisites import Requisites
from .warehouse import Warehouse
from .tags import Tags
from .custom_reports import (
    CustomReportGroups,
    CustomReportEntries,
    CustomReportValues,
    CustomReportDebtEntries
)

class ApiV2Namespace:
    def __init__(self, client):
        self.custom_report_groups = CustomReportGroups(client)
        self.custom_report_entries = CustomReportEntries(client)
        self.custom_report_values = CustomReportValues(client)
        self.custom_report_debt_entries = CustomReportDebtEntries(client)

class AdeskClient:
    def __init__(self, api_token, base_url="https://api.adesk.ru/v1/", base_url_v2="https://api.adesk.ru/v2/"):
        self.api_token = api_token
        self.base_url = base_url
        self.base_url_v2 = base_url_v2
        self.transaction_categories = TransactionCategories(self)
        self.projects = Projects(self)
        self.commitments = Commitments(self)
        self.legal_entities = LegalEntities(self)
        self.bank_accounts = BankAccounts(self)
        self.transfers = Transfers(self)
        self.operations = Operations(self)
        self.contractors = Contractors(self)
        self.requisites = Requisites(self)
        self.warehouse = Warehouse(self)
        self.tags = Tags(self)
        self.v2 = ApiV2Namespace(self)

    def _request(self, method, endpoint, params=None, data=None):
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        headers = {}
        
        # Add api_token to params for GET or data for POST (V1 specific)
        if method.upper() == "GET":
            if params is None:
                params = {}
            params["api_token"] = self.api_token
        elif method.upper() == "POST": # V1 POST uses x-www-form-urlencoded
            if data is None:
                data = {}
            data["api_token"] = self.api_token
            headers["Content-Type"] = "application/x-www-form-urlencoded"

        try:
            response = requests.request(method, url, params=params, data=data, headers=headers)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.HTTPError as err:
            error_message = f"V1 HTTP error occurred: {err.response.status_code} {err.response.reason}\n"
            error_message += f"URL: {err.request.url}\n"
            try:
                error_message += f"Response content: {err.response.json()}"
            except ValueError: 
                error_message += f"Response content: {err.response.text}"
            raise Exception(error_message) from err
        except requests.exceptions.RequestException as e:
            raise Exception(f"V1 Request failed: {e}") from e

    def _request_v2(self, method, endpoint, params=None, json_data=None):
        url = f"{self.base_url_v2.rstrip('/')}/{endpoint.lstrip('/')}"
        
        headers = {
            "X-API-Token": self.api_token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            response = requests.request(method, url, params=params, json=json_data, headers=headers)
            response.raise_for_status()
            # Handle cases where response might be empty but successful (e.g., 204 No Content for DELETE)
            if response.status_code == 204:
                return None 
            return response.json()
        except requests.exceptions.HTTPError as err:
            error_message = f"V2 HTTP error occurred: {err.response.status_code} {err.response.reason}\n"
            error_message += f"URL: {err.request.url}\n"
            try:
                json_response = err.response.json()
                if "errors" in json_response:
                    error_message += f"Errors: {json_response['errors']}\n"
                if "message" in json_response:
                    error_message += f"Message: {json_response['message']}\n"
                error_message += f"Full Response: {json_response}"
            except ValueError:
                error_message += f"Response content: {err.response.text}"
            raise Exception(error_message) from err
        except requests.exceptions.RequestException as e:
            raise Exception(f"V2 Request failed: {e}") from e

    def get(self, endpoint, params=None):
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint, data=None, params=None):
        return self._request("POST", endpoint, params=params, data=data)

    # V2 public methods
    def get_v2(self, endpoint, params=None):
        return self._request_v2("GET", endpoint, params=params)

    def post_v2(self, endpoint, json_data=None, params=None):
        return self._request_v2("POST", endpoint, params=params, json_data=json_data)

    def put_v2(self, endpoint, json_data=None, params=None):
        return self._request_v2("PUT", endpoint, params=params, json_data=json_data)

    def delete_v2(self, endpoint, params=None):
        return self._request_v2("DELETE", endpoint, params=params)
