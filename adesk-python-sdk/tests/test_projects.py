import unittest
from unittest.mock import MagicMock, patch

# Assuming AdeskClient and Projects are in adesk_python_sdk.adesk package
# Adjust the import path if your structure is different
from adesk_python_sdk.adesk.client import AdeskClient 
from adesk_python_sdk.adesk.projects import Projects

class TestProjectsResource(unittest.TestCase):

    def setUp(self):
        # Create a MagicMock instance for AdeskClient for each test
        # This allows us to inspect calls to client.get and client.post
        self.mock_client = MagicMock(spec=AdeskClient)
        self.projects_resource = Projects(self.mock_client)

    def test_list_projects_success(self):
        mock_response_data = {"projects": [{"id": 1, "name": "Test Project 1"}, {"id": 2, "name": "Test Project 2"}]}
        self.mock_client.get.return_value = mock_response_data

        result = self.projects_resource.list(status="active", managers=[101, 102])

        self.mock_client.get.assert_called_once_with(
            "projects", 
            params={"status": "active", "managers[]": [101, 102]}
        )
        self.assertEqual(result, mock_response_data["projects"])

    def test_list_projects_empty_response(self):
        self.mock_client.get.return_value = {"projects": []} # API returns empty list
        result = self.projects_resource.list()
        self.mock_client.get.assert_called_once_with("projects", params={})
        self.assertEqual(result, [])

    def test_list_projects_no_projects_key(self):
        self.mock_client.get.return_value = {"message": "something else"} # No 'projects' key
        result = self.projects_resource.list()
        self.mock_client.get.assert_called_once_with("projects", params={})
        self.assertIsNone(result) # Or [] depending on desired behavior in Projects.list

    def test_create_project_success(self):
        mock_response_data = {"project": {"id": 3, "name": "New Project", "description": "Desc"}}
        self.mock_client.post.return_value = mock_response_data
        
        project_data = {
            "name": "New Project",
            "description": "Desc",
            "category": 1,
            "manager": 5
        }
        result = self.projects_resource.create(**project_data)

        self.mock_client.post.assert_called_once_with("project", data=project_data)
        self.assertEqual(result, mock_response_data["project"])

    def test_create_project_missing_name(self):
        with self.assertRaises(ValueError) as context:
            self.projects_resource.create(description="A project without a name")
        self.assertTrue("Missing required parameter for creating a project: name" in str(context.exception))
        self.mock_client.post.assert_not_called()

    def test_update_project_success(self):
        project_id = 10
        update_payload = {"name": "Updated Name", "is_archived": True}
        mock_response_data = {"project": {"id": project_id, **update_payload}}
        self.mock_client.post.return_value = mock_response_data

        result = self.projects_resource.update(project_id, name="Updated Name", is_archived=True)
        
        self.mock_client.post.assert_called_once_with(f"project/{project_id}", data=update_payload)
        self.assertEqual(result, mock_response_data["project"])

    def test_update_project_no_id(self):
        with self.assertRaises(ValueError):
            self.projects_resource.update(project_id=None, name="New Name")
        self.mock_client.post.assert_not_called()

    def test_delete_project_success(self):
        project_id = 20
        mock_response_data = {"success": True} # Typical response for delete
        self.mock_client.post.return_value = mock_response_data

        result = self.projects_resource.delete(project_id)

        self.mock_client.post.assert_called_once_with(f"project/{project_id}/remove")
        self.assertEqual(result, mock_response_data)
    
    def test_delete_project_no_id(self):
        with self.assertRaises(ValueError):
            self.projects_resource.delete(project_id=None)
        self.mock_client.post.assert_not_called()

    def test_list_categories_success(self):
        mock_response_data = {"categories": [{"id": 1, "name": "Category A"}, {"id": 2, "name": "Category B"}]}
        self.mock_client.get.return_value = mock_response_data

        result = self.projects_resource.list_categories()

        self.mock_client.get.assert_called_once_with("projects/categories")
        self.assertEqual(result, mock_response_data["categories"])

    def test_list_categories_empty(self):
        self.mock_client.get.return_value = {"categories": []}
        result = self.projects_resource.list_categories()
        self.mock_client.get.assert_called_once_with("projects/categories")
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
