class Projects:
    def __init__(self, client):
        self.client = client

    def list(self, category=None, managers=None, status=None, start=None, length=None, q=None, reduced=None, sorting=None):
        """
        Get list of projects.
        Endpoint: projects
        Method: GET
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
        return response.get("projects")

    def create(self, name, description=None, is_archived=None, plan_income=None, plan_outcome=None, 
               category=None, manager=None, deal_contractor=None, deal_legal_entity=None, is_deal=None):
        """
        Adding a project.
        Endpoint: project
        Method: POST
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
        return response.get("project")

    def update(self, project_id, name=None, description=None, is_archived=None, plan_income=None, 
               plan_outcome=None, category=None, manager=None, is_deal=None, 
               deal_contractor=None, deal_legal_entity=None):
        """
        Changing a project.
        Endpoint: project/<project_id>
        Method: POST
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
        return response.get("project")

    def delete(self, project_id):
        """
        Deleting a project.
        Endpoint: project/<project_id>/remove
        Method: POST
        """
        if project_id is None:
            raise ValueError("Missing required parameter for deleting a project: project_id.")
            
        # Adesk API for delete project does not expect a body, only api_token, which client handles
        response = self.client.post(f"project/{project_id}/remove") 
        return response

    def list_categories(self):
        """
        List of project directions.
        Endpoint: projects/categories
        Method: GET
        """
        response = self.client.get("projects/categories")
        return response.get("categories")
