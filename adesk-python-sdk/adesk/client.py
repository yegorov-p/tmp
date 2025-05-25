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
from .webhooks import Webhooks
from .exceptions import (
    AdeskAPIError,
    AdeskAuthError,
    AdeskRateLimitError,
    AdeskPaymentRequiredError,
    AdeskBadRequestError,
    AdeskNotFoundError,
    AdeskServerError
)


class ApiV2Namespace:
    """
    Provides a namespace for accessing Adesk API v2 resources.
    All v2 resources are accessed via an instance of this class, typically `client.v2`.
    """
    def __init__(self, client):
        """
        Initializes the ApiV2Namespace.

        Args:
            client (AdeskClient): The AdeskClient instance to use for API calls.
        """
        self.custom_report_groups = CustomReportGroups(client)
        self.custom_report_entries = CustomReportEntries(client)
        self.custom_report_values = CustomReportValues(client)
        self.custom_report_debt_entries = CustomReportDebtEntries(client)

class AdeskClient:
    """
    The main client for interacting with the Adesk API (both v1 and v2).

    Provides access to various API resources such as projects, transactions,
    commitments, etc. V1 resources are accessed directly as attributes of the client
    instance (e.g., `client.projects`), while V2 resources are accessed via the
    `v2` attribute (e.g., `client.v2.custom_report_groups`).
    """
    def __init__(self, api_token, base_url="https://api.adesk.ru/v1/", base_url_v2="https://api.adesk.ru/v2/"):
        """
        Initializes the AdeskClient.

        Args:
            api_token (str): Your Adesk API token.
            base_url (str, optional): The base URL for Adesk API v1.
                                      Defaults to "https://api.adesk.ru/v1/".
            base_url_v2 (str, optional): The base URL for Adesk API v2.
                                         Defaults to "https://api.adesk.ru/v2/".
        """
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
        self.webhooks = Webhooks(self)

    def _request(self, method, endpoint, params=None, data=None):
        """
        Internal method to make requests to Adesk API v1.

        Handles URL construction, authentication, and basic error handling for v1.
        V1 uses 'api_token' in query parameters for GET or in form data for POST.

        Args:
            method (str): HTTP method (e.g., "GET", "POST").
            endpoint (str): API endpoint path (e.g., "projects", "transaction/123").
            params (dict, optional): Query parameters for the request.
            data (dict, optional): Form data for POST requests.

        Returns:
            dict or None: The JSON response from the API, or None for 204 No Content.

        Raises:
            AdeskAuthError: If authentication fails (401).
            AdeskPaymentRequiredError: If payment is required (custom code 21 or HTTP 402/403).
            AdeskBadRequestError: For client-side errors like missing parameters (400).
            AdeskNotFoundError: If the resource is not found (404).
            AdeskServerError: For server-side errors (5xx).
            AdeskAPIError: For other API-related errors.
            requests.exceptions.RequestException: For network or request-related issues.
        """
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
            
            # Check for Adesk specific error code 21 even on HTTP 200
            if response.status_code == 200:
                try:
                    response_json = response.json()
                    if isinstance(response_json, dict) and response_json.get('code') == 21:
                        msg = response_json.get('message', "Payment required for API access.")
                        raise AdeskPaymentRequiredError(msg, status_code=200, response_data=response_json)
                    if response.text == "" and response.request.method != 'HEAD': # No content but not HEAD
                        return None # Or True, depending on desired behavior for empty success
                    return response_json # Return parsed JSON if no error code 21
                except requests.exceptions.JSONDecodeError:
                    # If response is not JSON, but status is 200 and not code 21, return text or handle as error
                    # For now, let's assume successful non-JSON 200 is rare for V1 and could be an issue.
                    # If response.text is empty, it's like a 204.
                    return response.text if response.text else None

            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx) if not 200
            
            if response.status_code == 204: # Should be caught by raise_for_status for non-2xx, but good to be explicit
                return None
            return response.json() # Should not be reached if raise_for_status() is effective for all non-200s

        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            try:
                response_data = err.response.json()
                message = response_data.get("message", str(err))
                if "errors" in response_data: # Often validation errors are in 'errors'
                    message += f" Details: {response_data['errors']}"
            except requests.exceptions.JSONDecodeError:
                response_data = err.response.text
                message = str(err)

            if status_code == 401:
                raise AdeskAuthError(message, status_code, response_data) from err
            elif status_code == 402 or status_code == 403: # Often used for payment/permission issues
                 # Check for Adesk's specific code 21 structure again, just in case
                if isinstance(response_data, dict) and response_data.get('code') == 21:
                    message = response_data.get('message', "Payment required for API access.")
                raise AdeskPaymentRequiredError(message, status_code, response_data) from err
            elif status_code == 429:
                raise AdeskRateLimitError(message, status_code, response_data) from err
            elif status_code == 400:
                raise AdeskBadRequestError(message, status_code, response_data) from err
            elif status_code == 404:
                raise AdeskNotFoundError(message, status_code, response_data) from err
            elif 500 <= status_code < 600:
                raise AdeskServerError(message, status_code, response_data) from err
            else:
                raise AdeskAPIError(message, status_code, response_data) from err
        except requests.exceptions.RequestException as e: # Catches network errors, etc.
            raise AdeskAPIError(f"Request failed: {e}") from e # Wrap in AdeskAPIError for consistency

    def _request_v2(self, method, endpoint, params=None, json_data=None):
        """
        Internal method to make requests to Adesk API v2.

        Handles URL construction, authentication (via X-API-Token header),
        JSON request bodies, and error handling for v2.

        Args:
            method (str): HTTP method (e.g., "GET", "POST", "PUT", "DELETE").
            endpoint (str): API endpoint path (e.g., "custom-report-groups").
            params (dict, optional): Query parameters for the request.
            json_data (dict, optional): JSON data for POST/PUT requests.

        Returns:
            dict or None: The JSON response from the API, or None for 204 No Content.

        Raises:
            AdeskAuthError: If authentication fails (401).
            AdeskRateLimitError: If rate limit is exceeded (429).
            AdeskBadRequestError: For client-side errors like missing parameters (400).
            AdeskNotFoundError: If the resource is not found (404).
            AdeskServerError: For server-side errors (5xx).
            AdeskAPIError: For other API-related errors.
            requests.exceptions.RequestException: For network or request-related issues.
        """
        url = f"{self.base_url_v2.rstrip('/')}/{endpoint.lstrip('/')}"
        
        headers = {
            "X-API-Token": self.api_token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            response = requests.request(method, url, params=params, json=json_data, headers=headers)
            response.raise_for_status() # Raises HTTPError for 4xx/5xx
            
            if response.status_code == 204: # No Content
                return None 
            return response.json()
            
        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            try:
                response_data = err.response.json()
                message = response_data.get("message", str(err))
                if "errors" in response_data: # V2 often uses 'errors' field
                    message += f" Details: {response_data['errors']}"
            except requests.exceptions.JSONDecodeError:
                response_data = err.response.text
                message = str(err)

            if status_code == 401:
                raise AdeskAuthError(message, status_code, response_data) from err
            elif status_code == 429:
                raise AdeskRateLimitError(message, status_code, response_data) from err
            elif status_code == 400:
                raise AdeskBadRequestError(message, status_code, response_data) from err
            elif status_code == 404:
                raise AdeskNotFoundError(message, status_code, response_data) from err
            elif status_code == 403: # V2 might use 403 for payment/permission
                raise AdeskPaymentRequiredError(message, status_code, response_data) from err
            elif 500 <= status_code < 600:
                raise AdeskServerError(message, status_code, response_data) from err
            else:
                raise AdeskAPIError(message, status_code, response_data) from err
        except requests.exceptions.RequestException as e: # Catches network errors
            raise AdeskAPIError(f"V2 Request failed: {e}") from e


    def get(self, endpoint, params=None):
        """
        Makes a GET request to a v1 API endpoint.

        Args:
            endpoint (str): API endpoint path.
            params (dict, optional): Query parameters.

        Returns:
            dict: The JSON response.
        """
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint, data=None, params=None):
        """
        Makes a POST request to a v1 API endpoint.

        Args:
            endpoint (str): API endpoint path.
            data (dict, optional): Form data for the request body.
            params (dict, optional): Query parameters.

        Returns:
            dict: The JSON response.
        """
        return self._request("POST", endpoint, params=params, data=data)

    # V2 public methods
    def get_v2(self, endpoint, params=None):
        """
        Makes a GET request to a v2 API endpoint.

        Args:
            endpoint (str): API endpoint path.
            params (dict, optional): Query parameters.

        Returns:
            dict or None: The JSON response, or None for 204 No Content.
        """
        return self._request_v2("GET", endpoint, params=params)

    def post_v2(self, endpoint, json_data=None, params=None):
        """
        Makes a POST request with a JSON body to a v2 API endpoint.

        Args:
            endpoint (str): API endpoint path.
            json_data (dict, optional): Data to be sent as JSON in the request body.
            params (dict, optional): Query parameters.

        Returns:
            dict or None: The JSON response, or None for 204 No Content.
        """
        return self._request_v2("POST", endpoint, params=params, json_data=json_data)

    def put_v2(self, endpoint, json_data=None, params=None):
        """
        Makes a PUT request with a JSON body to a v2 API endpoint.

        Args:
            endpoint (str): API endpoint path.
            json_data (dict, optional): Data to be sent as JSON in the request body.
            params (dict, optional): Query parameters.

        Returns:
            dict or None: The JSON response, or None for 204 No Content.
        """
        return self._request_v2("PUT", endpoint, params=params, json_data=json_data)

    def delete_v2(self, endpoint, params=None):
        """
        Makes a DELETE request to a v2 API endpoint.

        Args:
            endpoint (str): API endpoint path.
            params (dict, optional): Query parameters.

        Returns:
            dict or None: The JSON response, or None for 204 No Content.
        """
        return self._request_v2("DELETE", endpoint, params=params)
