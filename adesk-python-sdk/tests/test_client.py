import unittest
from unittest.mock import patch, MagicMock
import requests # Will be mocked

from adesk_python_sdk.adesk.client import AdeskClient, ApiV2Namespace
from adesk_python_sdk.adesk.exceptions import (
    AdeskAPIError,
    AdeskAuthError,
    AdeskRateLimitError,
    AdeskPaymentRequiredError,
    AdeskBadRequestError,
    AdeskNotFoundError,
    AdeskServerError
)
# Import resource classes to check for their initialization
from adesk_python_sdk.adesk.projects import Projects
from adesk_python_sdk.adesk.custom_reports import CustomReportGroups

class TestAdeskClient(unittest.TestCase):

    def test_init_client(self):
        token = "test_token"
        client = AdeskClient(api_token=token)
        self.assertEqual(client.api_token, token)
        self.assertEqual(client.base_url, "https://api.adesk.ru/v1/")
        self.assertEqual(client.base_url_v2, "https://api.adesk.ru/v2/")

        # Check if V1 resources are initialized (spot check a few)
        self.assertIsInstance(client.projects, Projects)
        self.assertIsInstance(client.webhooks, object) # Using object as Webhooks is not imported here directly

        # Check if V2 namespace and its resources are initialized
        self.assertIsInstance(client.v2, ApiV2Namespace)
        self.assertIsInstance(client.v2.custom_report_groups, CustomReportGroups)

        custom_v1_url = "http://localhost/api/v1"
        custom_v2_url = "http://localhost/api/v2"
        client_custom_url = AdeskClient(api_token=token, base_url=custom_v1_url, base_url_v2=custom_v2_url)
        self.assertEqual(client_custom_url.base_url, custom_v1_url)
        self.assertEqual(client_custom_url.base_url_v2, custom_v2_url)

    @patch('requests.request')
    def test_request_v1_get_success(self, mock_request):
        client = AdeskClient(api_token="test_token")
        mock_response = MagicMock()
        mock_response.status_code = 200
        expected_json = {"data": "success"}
        mock_response.json.return_value = expected_json
        mock_request.return_value = mock_response

        endpoint = "test_endpoint"
        params = {"param1": "value1"}
        response_json = client._request("GET", endpoint, params=params)

        mock_request.assert_called_once_with(
            "GET",
            f"{client.base_url}{endpoint}",
            params={"param1": "value1", "api_token": client.api_token},
            data=None,
            headers={}
        )
        self.assertEqual(response_json, expected_json)

    @patch('requests.request')
    def test_request_v1_post_success(self, mock_request):
        client = AdeskClient(api_token="test_token")
        mock_response = MagicMock()
        mock_response.status_code = 200
        expected_json = {"data": "created"}
        mock_response.json.return_value = expected_json
        mock_request.return_value = mock_response

        endpoint = "create_endpoint"
        data = {"key": "value"}
        response_json = client._request("POST", endpoint, data=data)

        mock_request.assert_called_once_with(
            "POST",
            f"{client.base_url}{endpoint}",
            params=None,
            data={"key": "value", "api_token": client.api_token},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        self.assertEqual(response_json, expected_json)
    
    @patch('requests.request')
    def test_request_v1_204_no_content(self, mock_request):
        client = AdeskClient(api_token="test_token")
        mock_response = MagicMock()
        mock_response.status_code = 200 # V1 client handles 204 like empty 200
        mock_response.text = ""
        mock_response.json.side_effect = requests.exceptions.JSONDecodeError("","",0) # mock no json
        mock_request.return_value = mock_response

        response = client._request("GET", "empty_endpoint")
        self.assertIsNone(response)

    @patch('requests.request')
    def test_request_v1_error_handling(self, mock_request):
        client = AdeskClient(api_token="test_token")
        error_map = {
            400: (AdeskBadRequestError, {"message": "Bad request"}),
            401: (AdeskAuthError, {"message": "Unauthorized"}),
            404: (AdeskNotFoundError, {"message": "Not found"}),
            429: (AdeskRateLimitError, {"message": "Rate limit"}),
            500: (AdeskServerError, {"message": "Server error"}),
        }

        for status_code, (exc_class, resp_json) in error_map.items():
            with self.subTest(status_code=status_code):
                mock_response = MagicMock()
                mock_response.status_code = status_code
                mock_response.json.return_value = resp_json
                mock_response.text = str(resp_json) # for non-json fallback
                mock_request.return_value = mock_response
                mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)

                with self.assertRaises(exc_class) as cm:
                    client._request("GET", "error_endpoint")
                self.assertEqual(cm.exception.status_code, status_code)
                self.assertIn(resp_json["message"], str(cm.exception))

    @patch('requests.request')
    def test_request_v1_payment_required_code_21(self, mock_request):
        client = AdeskClient(api_token="test_token")
        mock_response = MagicMock()
        mock_response.status_code = 200 # Code 21 comes with HTTP 200
        resp_json = {"code": 21, "message": "Payment required"}
        mock_response.json.return_value = resp_json
        mock_request.return_value = mock_response

        with self.assertRaises(AdeskPaymentRequiredError) as cm:
            client._request("GET", "payment_endpoint")
        self.assertEqual(cm.exception.status_code, 200) # Original status code
        self.assertIn(resp_json["message"], str(cm.exception))

    @patch('requests.request')
    def test_request_v1_non_json_error(self, mock_request):
        client = AdeskClient(api_token="test_token")
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Simple text error"
        mock_response.json.side_effect = requests.exceptions.JSONDecodeError("","",0)
        mock_request.return_value = mock_response
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)

        with self.assertRaises(AdeskBadRequestError) as cm:
            client._request("GET", "text_error_endpoint")
        self.assertEqual(cm.exception.status_code, 400)
        self.assertIn("Simple text error", str(cm.exception.response_data))


    @patch('requests.request')
    def test_request_v2_get_success(self, mock_request):
        client = AdeskClient(api_token="test_token_v2")
        mock_response = MagicMock()
        mock_response.status_code = 200
        expected_json = {"data": "v2_success"}
        mock_response.json.return_value = expected_json
        mock_request.return_value = mock_response

        endpoint = "v2_endpoint"
        params = {"p1": "v1"}
        response_json = client._request_v2("GET", endpoint, params=params)

        mock_request.assert_called_once_with(
            "GET",
            f"{client.base_url_v2}{endpoint}",
            params=params,
            json=None,
            headers={
                "X-API-Token": client.api_token,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )
        self.assertEqual(response_json, expected_json)

    @patch('requests.request')
    def test_request_v2_post_success(self, mock_request):
        client = AdeskClient(api_token="test_token_v2")
        mock_response = MagicMock()
        mock_response.status_code = 200
        expected_json = {"data": "v2_created"}
        mock_response.json.return_value = expected_json
        mock_request.return_value = mock_response

        endpoint = "v2_create"
        json_data = {"name": "test"}
        response_json = client._request_v2("POST", endpoint, json_data=json_data)

        mock_request.assert_called_once_with(
            "POST",
            f"{client.base_url_v2}{endpoint}",
            params=None,
            json=json_data,
            headers={
                "X-API-Token": client.api_token,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )
        self.assertEqual(response_json, expected_json)

    @patch('requests.request')
    def test_request_v2_204_no_content(self, mock_request):
        client = AdeskClient(api_token="test_token_v2")
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_request.return_value = mock_response

        response = client._request_v2("DELETE", "v2_delete_endpoint")
        self.assertIsNone(response)
        mock_response.json.assert_not_called() # No attempt to parse JSON for 204

    @patch('requests.request')
    def test_request_v2_error_handling(self, mock_request):
        client = AdeskClient(api_token="test_token")
        error_map = {
            400: (AdeskBadRequestError, {"message": "V2 Bad request", "errors": {"field": "is wrong"}}),
            401: (AdeskAuthError, {"message": "V2 Unauthorized"}),
            403: (AdeskPaymentRequiredError, {"message": "V2 Payment Required"}),
            404: (AdeskNotFoundError, {"message": "V2 Not found"}),
            429: (AdeskRateLimitError, {"message": "V2 Rate limit"}),
            500: (AdeskServerError, {"message": "V2 Server error"}),
        }

        for status_code, (exc_class, resp_json) in error_map.items():
            with self.subTest(status_code=status_code):
                mock_response = MagicMock()
                mock_response.status_code = status_code
                mock_response.json.return_value = resp_json
                mock_request.return_value = mock_response
                mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
                
                with self.assertRaises(exc_class) as cm:
                    client._request_v2("GET", "v2_error_endpoint")
                self.assertEqual(cm.exception.status_code, status_code)
                self.assertIn(resp_json["message"], str(cm.exception))
                if "errors" in resp_json:
                     self.assertIn(str(resp_json["errors"]), str(cm.exception))


    @patch.object(AdeskClient, '_request')
    def test_public_get_v1(self, mock_internal_request):
        client = AdeskClient(api_token="token")
        client.get("endpoint", params={"p": "v"})
        mock_internal_request.assert_called_once_with("GET", "endpoint", params={"p": "v"})

    @patch.object(AdeskClient, '_request')
    def test_public_post_v1(self, mock_internal_request):
        client = AdeskClient(api_token="token")
        client.post("endpoint", data={"d": "v"}, params={"p": "v"})
        mock_internal_request.assert_called_once_with("POST", "endpoint", params={"p": "v"}, data={"d": "v"})

    @patch.object(AdeskClient, '_request_v2')
    def test_public_get_v2(self, mock_internal_request_v2):
        client = AdeskClient(api_token="token")
        client.get_v2("endpoint", params={"p": "v"})
        mock_internal_request_v2.assert_called_once_with("GET", "endpoint", params={"p": "v"})

    @patch.object(AdeskClient, '_request_v2')
    def test_public_post_v2(self, mock_internal_request_v2):
        client = AdeskClient(api_token="token")
        client.post_v2("endpoint", json_data={"d": "v"}, params={"p": "v"})
        mock_internal_request_v2.assert_called_once_with("POST", "endpoint", params={"p": "v"}, json_data={"d": "v"})

    @patch.object(AdeskClient, '_request_v2')
    def test_public_put_v2(self, mock_internal_request_v2):
        client = AdeskClient(api_token="token")
        client.put_v2("endpoint", json_data={"d": "v"}, params={"p": "v"})
        mock_internal_request_v2.assert_called_once_with("PUT", "endpoint", params={"p": "v"}, json_data={"d": "v"})

    @patch.object(AdeskClient, '_request_v2')
    def test_public_delete_v2(self, mock_internal_request_v2):
        client = AdeskClient(api_token="token")
        client.delete_v2("endpoint", params={"p": "v"})
        mock_internal_request_v2.assert_called_once_with("DELETE", "endpoint", params={"p": "v"})


if __name__ == '__main__':
    unittest.main()
