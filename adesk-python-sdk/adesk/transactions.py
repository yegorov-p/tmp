class TransactionCategories:
    def __init__(self, client):
        self.client = client

    def list(self, type=None, full_group=None):
        """
        Get list of transaction categories.
        Endpoint: transactions/categories
        Method: GET
        """
        params = {}
        if type is not None:
            params["type"] = type
        if full_group is not None:
            params["full_group"] = full_group
        
        response = self.client.get("transactions/categories", params=params)
        return response.get("categories")

    def create_update_delete(self, id=None, name=None, type=None, kind=None, group=None, 
                             is_owner_transfer=None, is_deleted=None, is_archived=None):
        """
        Create, change, delete a transaction category.
        Endpoint: transactions/category
        Method: POST
        """
        data = {}
        if id is not None:
            data["id"] = id
        if name is not None:
            data["name"] = name
        if type is not None:
            data["type"] = type
        if kind is not None:
            data["kind"] = kind
        if group is not None:
            data["group"] = group
        if is_owner_transfer is not None:
            data["is_owner_transfer"] = is_owner_transfer
        if is_deleted is not None:
            data["is_deleted"] = is_deleted
        if is_archived is not None:
            data["is_archived"] = is_archived

        # Basic validation for creation
        if id is None and is_deleted is not True: # If creating a new category (not deleting)
            if not name or type is None or kind is None:
                raise ValueError("Missing required parameters for creating a category: name, type, kind.")

        response = self.client.post("transactions/category", data=data)
        return response.get("category")
