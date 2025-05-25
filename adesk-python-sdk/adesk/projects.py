class Projects:
    """
    Provides methods for interacting with Adesk projects (API v1).
    Accessed via `client.projects`.
    """
    def __init__(self, client):
        """
        Initializes the Projects resource.

        Args:
            client (AdeskClient): The AdeskClient instance to use for API calls.
        """
        self.client = client

    def list(self, category=None, managers=None, status=None, start=None, length=None, q=None, reduced=None, sorting=None):
        """
        Retrieves a list of projects.
        Corresponds to Adesk API v1 endpoint: `GET projects`.

        Args:
            category (int, optional): Filter by project category ID.
            managers (list[int], optional): Filter by a list of manager IDs.
                                            The Adesk API expects this as 'managers[]'.
            status (str, optional): Filter by project status (e.g., "active", "archived", "all").
            start (int, optional): For pagination, the starting record number.
            length (int, optional): For pagination, the number of records to retrieve.
            q (str, optional): Search query string.
            reduced (bool, optional): If True, returns a reduced set of fields for each project.
            sorting (str, optional): Sorting criteria (e.g., "name_asc", "date_desc").

        Returns:
            list[dict]: A list of project objects.
                        Returns an empty list if no projects are found or in case of an error.
        """
        params = {}
        if category is not None:
            params["category"] = category
        if managers is not None: # Should be an array of numbers
            params["managers[]"] = managers 
        if status is not None:
            params["status"] = status
        if start is not None:
            params["start"] = start
        if length is not None:
            params["length"] = length
        if q is not None:
            params["q"] = q
        if reduced is not None:
            params["reduced"] = reduced
        if sorting is not None:
            params["sorting"] = sorting
        
        response = self.client.get("projects", params=params)
        return response.get("projects") if response else []

    def create(self, name, description=None, is_archived=None, plan_income=None, plan_outcome=None, 
               category=None, manager=None, deal_contractor=None, deal_legal_entity=None, is_deal=None):
        """
        Creates a new project.
        Corresponds to Adesk API v1 endpoint: `POST project`.

        Args:
            name (str): The name of the project. (Required)
            description (str, optional): Description of the project.
            is_archived (bool, optional): Whether the project is archived.
            plan_income (float, optional): Planned income for the project.
            plan_outcome (float, optional): Planned outcome (expenses) for the project.
            category (int, optional): Category ID for the project.
            manager (int, optional): Manager ID for the project.
            deal_contractor (int, optional): Contractor ID if the project is a deal.
            deal_legal_entity (int, optional): Legal entity ID if the project is a deal.
            is_deal (bool, optional): Whether the project is considered a deal.

        Returns:
            dict: The created project object.
                  Returns None if the operation was unsuccessful or the response is empty.
        """
        if not name:
            raise ValueError("Missing required parameter for creating a project: name.")

        data = {"name": name}
        if description is not None:
            data["description"] = description
        if is_archived is not None:
            data["is_archived"] = is_archived
        if plan_income is not None:
            data["plan_income"] = plan_income
        if plan_outcome is not None:
            data["plan_outcome"] = plan_outcome
        if category is not None:
            data["category"] = category
        if manager is not None:
            data["manager"] = manager
        if deal_contractor is not None:
            data["deal_contractor"] = deal_contractor
        if deal_legal_entity is not None:
            data["deal_legal_entity"] = deal_legal_entity
        if is_deal is not None:
            data["is_deal"] = is_deal
            
        response = self.client.post("project", data=data)
        return response.get("project") if response else None

    def update(self, project_id, name=None, description=None, is_archived=None, plan_income=None, 
               plan_outcome=None, category=None, manager=None, is_deal=None, 
               deal_contractor=None, deal_legal_entity=None):
        """
        Updates an existing project.
        Corresponds to Adesk API v1 endpoint: `POST project/<project_id>`.

        Args:
            project_id (int): The ID of the project to update. (Required)
            name (str, optional): New name for the project.
            description (str, optional): New description for the project.
            is_archived (bool, optional): Archive/unarchive the project.
            plan_income (float, optional): New planned income.
            plan_outcome (float, optional): New planned outcome.
            category (int, optional): New category ID.
            manager (int, optional): New manager ID.
            is_deal (bool, optional): Update if the project is a deal.
            deal_contractor (int, optional): New contractor ID for the deal.
            deal_legal_entity (int, optional): New legal entity ID for the deal.

        Returns:
            dict: The updated project object.
                  Returns None if the operation was unsuccessful or the response is empty.
        """
        if project_id is None:
            raise ValueError("Missing required parameter for updating a project: project_id.")

        data = {}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if is_archived is not None:
            data["is_archived"] = is_archived
        if plan_income is not None:
            data["plan_income"] = plan_income
        if plan_outcome is not None:
            data["plan_outcome"] = plan_outcome
        if category is not None:
            data["category"] = category
        if manager is not None:
            data["manager"] = manager
        if is_deal is not None:
            data["is_deal"] = is_deal
        if deal_contractor is not None:
            data["deal_contractor"] = deal_contractor
        if deal_legal_entity is not None:
            data["deal_legal_entity"] = deal_legal_entity
            
        response = self.client.post(f"project/{project_id}", data=data)
        return response.get("project") if response else None

    def delete(self, project_id):
        """
        Deletes a project.
        Corresponds to Adesk API v1 endpoint: `POST project/<project_id>/remove`.

        Args:
            project_id (int): The ID of the project to delete. (Required)

        Returns:
            dict: The response from the API, typically confirming success or failure.
                  A successful deletion might return `{"success": true}`.
        """
        if project_id is None:
            raise ValueError("Missing required parameter for deleting a project: project_id.")
            
        # Adesk API for delete project does not expect a body, only api_token, which client handles
        response = self.client.post(f"project/{project_id}/remove") 
        return response

    def list_categories(self):
        """
        Retrieves a list of project categories (directions).
        Corresponds to Adesk API v1 endpoint: `GET projects/categories`.

        Returns:
            list[dict]: A list of project category objects.
                        Returns an empty list if no categories are found or in case of an error.
        """
        response = self.client.get("projects/categories")
        return response.get("categories") if response else []
