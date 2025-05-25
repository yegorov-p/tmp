import unittest
from unittest.mock import MagicMock, patch

from adesk_python_sdk.adesk.client import AdeskClient
from adesk_python_sdk.adesk.custom_reports import CustomReportGroups

class TestCustomReportGroupsResource(unittest.TestCase):

    def setUp(self):
        self.mock_client = MagicMock(spec=AdeskClient)
        self.custom_report_groups_resource = CustomReportGroups(self.mock_client)

    def test_list_custom_report_groups_success(self):
        mock_response_data = {
            "data": [{"id": 1, "name": "Group A", "apiName": "groupA"}],
            "meta": {"pagination": {"total": 1, "count": 1, "per_page": 15, "current_page": 1}}
        }
        self.mock_client.get_v2.return_value = mock_response_data

        result = self.custom_report_groups_resource.list(report_section="finance")

        self.mock_client.get_v2.assert_called_once_with(
            "custom-report-groups",
            params={"reportSection": "finance"}
        )
        self.assertEqual(result, mock_response_data["data"])

    def test_list_custom_report_groups_empty_data(self):
        self.mock_client.get_v2.return_value = {"data": []}
        result = self.custom_report_groups_resource.list()
        self.mock_client.get_v2.assert_called_once_with("custom-report-groups", params={})
        self.assertEqual(result, [])
    
    def test_list_custom_report_groups_no_data_key(self):
        self.mock_client.get_v2.return_value = {"message": "error"} # No 'data' key
        result = self.custom_report_groups_resource.list()
        self.mock_client.get_v2.assert_called_once_with("custom-report-groups", params={})
        self.assertEqual(result, []) # Should return empty list if 'data' key is missing

    def test_list_custom_report_groups_client_returns_none(self):
        self.mock_client.get_v2.return_value = None # Client call failed or returned None
        result = self.custom_report_groups_resource.list()
        self.mock_client.get_v2.assert_called_once_with("custom-report-groups", params={})
        self.assertEqual(result, []) # Should return empty list if client returns None


    def test_create_custom_report_groups_success(self):
        groups_payload = [{
            "name": "New Group",
            "apiName": "newGroup",
            "reportSection": "sales",
            "color": "red"
        }]
        mock_response_data = {"data": [{"id": 10, **groups_payload[0]}]}
        self.mock_client.post_v2.return_value = mock_response_data

        result = self.custom_report_groups_resource.create(groups_payload)

        self.mock_client.post_v2.assert_called_once_with(
            "custom-report-groups/create",
            json_data=groups_payload
        )
        self.assertEqual(result, mock_response_data["data"])

    def test_update_custom_report_groups_success(self):
        update_payload = [{"id": 1, "name": "Updated Group Name"}]
        mock_response_data = {"data": update_payload} # Assuming API returns the updated data
        self.mock_client.post_v2.return_value = mock_response_data

        result = self.custom_report_groups_resource.update(update_payload)

        self.mock_client.post_v2.assert_called_once_with(
            "custom-report-groups/update",
            json_data=update_payload
        )
        self.assertEqual(result, mock_response_data["data"])

    def test_remove_custom_report_groups_success(self):
        group_ids_to_remove = [1, 2]
        # API might return empty data or some success indicator
        mock_response_data = {"data": [], "message": "Successfully removed"} 
        self.mock_client.post_v2.return_value = mock_response_data

        result = self.custom_report_groups_resource.remove(group_ids_to_remove)

        self.mock_client.post_v2.assert_called_once_with(
            "custom-report-groups/remove",
            json_data=group_ids_to_remove
        )
        self.assertEqual(result, mock_response_data["data"])


if __name__ == '__main__':
    unittest.main()
