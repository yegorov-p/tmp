from adesk_python_sdk.adesk.models import TransactionCategory

class TransactionCategories:
    """
    Provides methods for interacting with Adesk transaction categories (API v1).
    Accessed via `client.transaction_categories`.
    """
    def __init__(self, client):
        """
        Initializes the TransactionCategories resource.

        Args:
            client (AdeskClient): The AdeskClient instance to use for API calls.
        """
        self.client = client

    def list(self, type=None, full_group=None):
        """
        Retrieves a list of transaction categories.
        Corresponds to Adesk API v1 endpoint: `GET transactions/categories`.

        Args:
            type (str, optional): Filter by category type (e.g., "income", "outcome").
            full_group (bool, optional): Whether to return the full group structure.

        Returns:
            list[TransactionCategory]: A list of TransactionCategory model instances.
                                       Returns an empty list if no categories are found or in case of an error.
        """
        params = {}
        if type is not None:
            params["type"] = type
        if full_group is not None:
            params["full_group"] = full_group
        
        response = self.client.get("transactions/categories", params=params)
        categories_data = response.get("categories", []) if response else []
        return TransactionCategory.from_list(categories_data)

    def create_update_delete(self, id=None, name=None, type=None, kind=None, group=None, 
                             is_owner_transfer=None, is_deleted=None, is_archived=None):
        """
        Creates, updates, or deletes a transaction category.
        To create a new category, provide `name`, `type`, and `kind`.
        To update an existing category, provide its `id` and other parameters to change.
        To delete a category, provide its `id` and set `is_deleted=True`.
        Corresponds to Adesk API v1 endpoint: `POST transactions/category`.

        Args:
            id (int, optional): The ID of the category to update or delete.
                                Required for update/delete actions.
            name (str, optional): The name of the category. Required for creation.
            type (str, optional): The type of the category (e.g., "income", "outcome").
                                  Required for creation.
            kind (str, optional): The kind of the category (e.g., "operational", "investment").
                                  Required for creation.
            group (int, optional): The ID of the parent group for this category.
            is_owner_transfer (bool, optional): Whether this category represents an owner transfer.
            is_deleted (bool, optional): Set to `True` to delete the category.
                                         Requires `id` to be specified.
            is_archived (bool, optional): Set to `True` to archive the category.

        Returns:
            TransactionCategory | dict | None: The created or updated TransactionCategory model instance
                                               if the action was create or update and successful.
                                               If deleting, returns the raw API response (dict).
                                               Returns None if the create/update operation was unsuccessful
                                               or the response is empty.
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
        if id is None and (is_deleted is None or is_deleted is False): # If creating a new category
            if not name or type is None or kind is None:
                raise ValueError("Missing required parameters for creating a category: name, type, kind.")

        response_data = self.client.post("transactions/category", data=data)
        
        if is_deleted and response_data: # If delete action, return raw response
            return response_data

        category_data = response_data.get("category") if response_data else None
        return TransactionCategory(category_data) if category_data else None
