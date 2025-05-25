# adesk/models/contractors.py
from .base_model import BaseModel

class Contractor(BaseModel):
    """Represents a contractor (client, supplier, etc.) from the Adesk API."""
    def __init__(self, data):
        """
        Initializes a Contractor object from API response data.

        Args:
            data (dict | None): The dictionary of contractor data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.name = data.get('name')
        self.contact_person = data.get('contactPerson')
        self.phone_number = data.get('phoneNumber')
        self.email = data.get('email')
        self.balance = data.get('balance') # Only in list view
        self.description = data.get('description') # Might be in detailed view

        if self.balance is not None:
            try:
                self.balance = float(self.balance)
            except (ValueError, TypeError):
                self.balance = None # Or handle error appropriately
        # Note: 'balance' attribute might only be present in list views from the API.
