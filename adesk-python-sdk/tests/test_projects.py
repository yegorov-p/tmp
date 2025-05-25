import unittest
from unittest.mock import MagicMock, patch

# Assuming AdeskClient and Projects are in adesk_python_sdk.adesk package
# Adjust the import path if your structure is different
from adesk_python_sdk.adesk.client import AdeskClient 
from adesk_python_sdk.adesk.projects import Projects
from adesk_python_sdk.adesk.models import Project, ProjectCategory

class TestProjectsResource(unittest.TestCase):

    def setUp(self):
        # Create a MagicMock instance for AdeskClient for each test
        # This allows us to inspect calls to client.get and client.post
        self.mock_client = MagicMock(spec=AdeskClient)
        self.projects_resource = Projects(self.mock_client)

    def test_list_projects_success(self):
        mock_api_project_data = [{"id": 1, "name": "Test Project 1", "description": "Desc 1"}, {"id": 2, "name": "Test Project 2"}]
        mock_response_data = {"projects": mock_api_project_data}
        self.mock_client.get.return_value = mock_response_data

        result = self.projects_resource.list(status="active", managers=[101, 102])

        self.mock_client.get.assert_called_once_with(
            "projects", 
            params={"status": "active", "managers[]": [101, 102]}
        )
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(p, Project) for p in result))
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].name, "Test Project 1")
        self.assertEqual(result[0].description, "Desc 1")
        self.assertEqual(result[1].id, 2)
        self.assertEqual(result[1].name, "Test Project 2")


    def test_list_projects_empty_response(self):
        self.mock_client.get.return_value = {"projects": []} # API returns empty list
        result = self.projects_resource.list()
        self.mock_client.get.assert_called_once_with("projects", params={})
        self.assertEqual(result, [])
        self.assertIsInstance(result, list)


    def test_list_projects_no_projects_key(self):
        self.mock_client.get.return_value = {"message": "something else"} # No 'projects' key
        result = self.projects_resource.list()
        self.mock_client.get.assert_called_once_with("projects", params={})
        self.assertEqual(result, []) # Should return empty list if 'projects' key is missing or response is None

    def test_create_project_success(self):
        api_project_data = {"id": 3, "name": "New Project", "description": "Desc"}
        mock_response_data = {"project": api_project_data}
        self.mock_client.post.return_value = mock_response_data
        
        project_payload = {
            "name": "New Project",
            "description": "Desc",
            "category": 1,
            "manager": 5
        }
        result = self.projects_resource.create(**project_payload)

        self.mock_client.post.assert_called_once_with("project", data=project_payload)
        self.assertIsInstance(result, Project)
        self.assertEqual(result.id, api_project_data["id"])
        self.assertEqual(result.name, api_project_data["name"])
        self.assertEqual(result.description, api_project_data["description"])


    def test_create_project_missing_name(self):
        with self.assertRaises(ValueError) as context:
            self.projects_resource.create(description="A project without a name")
        self.assertTrue("Missing required parameter for creating a project: name" in str(context.exception))
        self.mock_client.post.assert_not_called()

    def test_update_project_success(self):
        project_id = 10
        update_payload = {"name": "Updated Name", "is_archived": True}
        api_project_data = {"id": project_id, **update_payload}
        mock_response_data = {"project": api_project_data}
        self.mock_client.post.return_value = mock_response_data

        result = self.projects_resource.update(project_id, name="Updated Name", is_archived=True)
        
        self.mock_client.post.assert_called_once_with(f"project/{project_id}", data=update_payload)
        self.assertIsInstance(result, Project)
        self.assertEqual(result.id, project_id)
        self.assertEqual(result.name, "Updated Name")
        self.assertTrue(result.is_archived)


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
        self.assertEqual(result, mock_response_data) # Delete still returns raw dict
    
    def test_delete_project_no_id(self):
        with self.assertRaises(ValueError):
            self.projects_resource.delete(project_id=None)
        self.mock_client.post.assert_not_called()

    def test_list_categories_success(self):
        mock_api_category_data = [{"id": 1, "name": "Category A"}, {"id": 2, "name": "Category B"}]
        mock_response_data = {"categories": mock_api_category_data}
        self.mock_client.get.return_value = mock_response_data

        result = self.projects_resource.list_categories()

        self.mock_client.get.assert_called_once_with("projects/categories")
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(c, ProjectCategory) for c in result))
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[0].name, "Category A")


    def test_list_categories_empty(self):
        self.mock_client.get.return_value = {"categories": []}
        result = self.projects_resource.list_categories()
        self.mock_client.get.assert_called_once_with("projects/categories")
        self.assertEqual(result, [])
        self.assertIsInstance(result, list)


if __name__ == '__main__':
    unittest.main()
