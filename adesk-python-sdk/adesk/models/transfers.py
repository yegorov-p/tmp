# adesk/models/transfers.py
from .base_model import BaseModel
from .tags import Tag # Assuming Tag model is defined and available for import

class TransferAccountInfo(BaseModel):
    """Represents summary information about a bank account involved in a transfer."""
    def __init__(self, data):
        """
        Initializes a TransferAccountInfo object from API response data.

        Args:
            data (dict | None): The dictionary of account info data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.currency = data.get('currency')
        self.bank_name = data.get('bankName')
        self.id = data.get('id')
        self.number = data.get('number')

class Transfer(BaseModel):
    """Represents a financial transfer between accounts from the Adesk API."""
    def __init__(self, data):
        """
        Initializes a Transfer object from API response data.

        Args:
            data (dict | None): The dictionary of transfer data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.from_account = TransferAccountInfo(data.get('from')) if data.get('from') else None
        self.to_account = TransferAccountInfo(data.get('to')) if data.get('to') else None
        self.amount = data.get('amount')
        self.tags = Tag.from_list(data.get('tags')) if data.get('tags') else []

        if self.amount is not None:
            try:
                self.amount = float(self.amount)
            except (ValueError, TypeError):
                self.amount = None
        # Note: 'from_account' and 'to_account' are instances of TransferAccountInfo.
        # 'tags' is a list of Tag model instances.
