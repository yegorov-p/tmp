import unittest
from unittest.mock import MagicMock, patch

from adesk_python_sdk.adesk.client import AdeskClient
from adesk_python_sdk.adesk.custom_reports import (
    CustomReportGroups, 
    CustomReportEntries, 
    CustomReportValues, 
    CustomReportDebtEntries
)
from adesk_python_sdk.adesk.models import (
    CustomReportGroup, 
    CustomReportEntry, 
    CustomReportValue, 
    CustomReportValueList,
    # CustomReportDebtEntry # Not strictly needed for these specific tests but good to have for consistency
)


class TestCustomReportGroupsResource(unittest.TestCase):

    def setUp(self):
        self.mock_client = MagicMock(spec=AdeskClient)
        self.custom_report_groups_resource = CustomReportGroups(self.mock_client)

    def test_list_custom_report_groups_success(self):
        mock_api_data = [{"id": 1, "name": "Group A", "apiName": "groupA"}]
        mock_response_data = {"data": mock_api_data, "success": True}
        self.mock_client.get_v2.return_value = mock_response_data

        result = self.custom_report_groups_resource.list(report_section="finance")

        self.mock_client.get_v2.assert_called_once_with(
            "custom-report-groups",
            params={"reportSection": "finance"}
        )
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(g, CustomReportGroup) for g in result))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].api_name, "groupA")


    def test_list_custom_report_groups_empty_data(self):
        self.mock_client.get_v2.return_value = {"data": [], "success": True}
        result = self.custom_report_groups_resource.list()
        self.mock_client.get_v2.assert_called_once_with("custom-report-groups", params={})
        self.assertEqual(result, [])
        self.assertIsInstance(result, list)
    
    def test_list_custom_report_groups_no_data_key(self):
        self.mock_client.get_v2.return_value = {"message": "error", "success": False} 
        result = self.custom_report_groups_resource.list()
        self.mock_client.get_v2.assert_called_once_with("custom-report-groups", params={})
        self.assertEqual(result, []) 

    def test_list_custom_report_groups_client_returns_none(self):
        self.mock_client.get_v2.return_value = None 
        result = self.custom_report_groups_resource.list()
        self.mock_client.get_v2.assert_called_once_with("custom-report-groups", params={})
        self.assertEqual(result, [])


    def test_create_custom_report_groups_success(self):
        groups_payload = [{
            "name": "New Group",
            "apiName": "newGroup",
            "reportSection": "sales",
            "color": "red"
        }]
        mock_api_data = [{"id": 10, **groups_payload[0]}]
        mock_response_data = {"data": mock_api_data, "success": True}
        self.mock_client.post_v2.return_value = mock_response_data

        result = self.custom_report_groups_resource.create(groups_payload)

        self.mock_client.post_v2.assert_called_once_with(
            "custom-report-groups/create",
            json_data=groups_payload
        )
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(g, CustomReportGroup) for g in result))
        self.assertEqual(result[0].id, 10)
        self.assertEqual(result[0].name, "New Group")


    def test_update_custom_report_groups_success(self):
        update_payload = [{"id": 1, "name": "Updated Group Name"}]
        mock_api_data = update_payload
        mock_response_data = {"data": mock_api_data, "success": True} 
        self.mock_client.post_v2.return_value = mock_response_data

        result = self.custom_report_groups_resource.update(update_payload)

        self.mock_client.post_v2.assert_called_once_with(
            "custom-report-groups/update",
            json_data=update_payload
        )
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(g, CustomReportGroup) for g in result))
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].name, "Updated Group Name")


    def test_remove_custom_report_groups_success(self):
        group_ids_to_remove = [1, 2]
        mock_response_data = {"success": True, "data": {"affected_ids": [1,2]}} 
        self.mock_client.post_v2.return_value = mock_response_data

        result = self.custom_report_groups_resource.remove(group_ids_to_remove)

        self.mock_client.post_v2.assert_called_once_with(
            "custom-report-groups/remove",
            json_data=group_ids_to_remove
        )
        self.assertEqual(result, mock_response_data) # Remove returns raw response


class TestCustomReportValuesResource(unittest.TestCase): # New Test Class

    def setUp(self):
        self.mock_client = MagicMock(spec=AdeskClient)
        self.custom_report_values_resource = CustomReportValues(self.mock_client)

    def test_list_values_success(self):
        mock_api_response = {
            "success": True,
            "itemsCount": 1,
            "totalItemsCount": 1,
            "values": [{"id": 100, "entryId": 1, "date": "2023-01-01", "amount": 123.45}],
            "entries": [{"id": 1, "name": "Revenue", "apiName": "revenue"}],
            "groups": [{"id": 5, "name": "Sales", "apiName": "sales"}],
            "projects": [{"id": 1, "name": "Project X"}], # Example raw data
            "businessUnits": [{"id": 1, "name": "BU Alpha"}] # Example raw data
        }
        self.mock_client.get_v2.return_value = mock_api_response

        result = self.custom_report_values_resource.list(entry_api_name="revenue")

        self.mock_client.get_v2.assert_called_once_with(
            "custom-report-values",
            params={"entryApiName": "revenue"}
        )
        self.assertIsInstance(result, CustomReportValueList)
        self.assertEqual(result.items_count, 1)
        self.assertIsInstance(result.values, list)
        self.assertTrue(all(isinstance(v, CustomReportValue) for v in result.values))
        self.assertEqual(result.values[0].id, 100)
        self.assertEqual(result.values[0].amount, 123.45)
        
        self.assertIsInstance(result.entries, list)
        self.assertTrue(all(isinstance(e, CustomReportEntry) for e in result.entries))
        self.assertEqual(result.entries[0].api_name, "revenue")

        self.assertIsInstance(result.groups, list)
        self.assertTrue(all(isinstance(g, CustomReportGroup) for g in result.groups))
        self.assertEqual(result.groups[0].api_name, "sales")
        
        # Check raw data for projects and business units as per current model
        self.assertEqual(result.projects_data[0]['name'], "Project X")
        self.assertEqual(result.business_units_data[0]['name'], "BU Alpha")


if __name__ == '__main__':
    unittest.main()
