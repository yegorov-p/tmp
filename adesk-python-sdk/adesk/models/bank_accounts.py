# adesk/models/bank_accounts.py
from .base_model import BaseModel

class BankAccount(BaseModel):
    """Represents a bank account or cash account from the Adesk API."""
    def __init__(self, data):
        """
        Initializes a BankAccount object from API response data.

        Args:
            data (dict | None): The dictionary of bank account data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.number = data.get('number')
        self.name = data.get('name')
        self.bank_name = data.get('bankName')
        self.created = data.get('created') # Consider datetime conversion later
        self.currency = data.get('currency') # This is likely a simple string code like "RUB"
        self.type = data.get('type') # API doc suggests 'Bank' or 'Cash', or 1 for cash, 2 for bank. Store as is.
        self.status = data.get('status') # 'open' or 'closed'
        self.initial_amount_date = data.get('initialAmountDate') # Consider datetime conversion
        self.initial_amount = data.get('initialAmount')
        self.amount = data.get('amount') # Current balance
        
        # Example for a nested legalEntity, if it's part of the response
        # self.legal_entity = LegalEntity(data.get('legalEntity')) if data.get('legalEntity') else None
        # For now, sticking to explicitly listed fields.
        
        # Other potential fields based on common bank account attributes:
        # self.bank_code = data.get('bankCode') # (BIC/SWIFT)
        # self.correspondent_account = data.get('correspondentAccount')
        # self.is_acquiring_enabled = data.get('isAcquiringEnabled')
        # self.commission_category_id = data.get('commissionCategoryId')
        # self.refund_category_id = data.get('refundCategoryId')
        # self.cash_category_id = data.get('cashCategoryId') # if type is 'Cash'
        # self.legal_entity_id = data.get('legalEntityId') # if legalEntity is not nested
        
        # Ensure numerical fields are correctly typed (e.g., float for amounts)
        if self.initial_amount is not None:
            try:
                self.initial_amount = float(self.initial_amount)
            except (ValueError, TypeError):
                # Handle or log error if conversion fails, or set to None
                self.initial_amount = None 
        
        if self.amount is not None:
            try:
                self.amount = float(self.amount)
            except (ValueError, TypeError):
                self.amount = None
        # Note: 'type' attribute stores the raw value from API (e.g., 'Bank', 'Cash', or int code).
        # Consider adding a property for a normalized type if needed.
