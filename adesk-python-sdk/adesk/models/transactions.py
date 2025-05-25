# adesk/models/transactions.py
from .base_model import BaseModel

class TransactionCategory(BaseModel):
    """Represents a transaction category from the Adesk API."""
    def __init__(self, data):
        """
        Initializes a TransactionCategory object from API response data.

        Args:
            data (dict | None): The dictionary of transaction category data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.name = data.get('name')
        self.type = data.get('type') # 1: income, 2: expenses
        self.kind = data.get('kind') # 1: operational, 2: investment, 3: financial
        self.is_owner_transfer = data.get('isOwnerTransfer')
        self.is_system = data.get('isSystem')
        self.group = data.get('group') # This might be an object too, check API. For now, assume ID or simple value.
        self.is_archived = data.get('isArchived')
        # If 'group' can be a nested object (e.g., when full_group=true is used in API call),
        # it might be initialized like:
        # self.group_details = TransactionCategoryGroup(data.get('group')) if isinstance(data.get('group'), dict) else None
        # self.group_id = data.get('group') if isinstance(data.get('group'), int) else None
        # For now, keeping it simple as per the provided structure.
        # Attributes like 'type' and 'kind' store integer codes; consider adding properties
        # for string representations if useful (e.g., type_name(), kind_name()).
