# adesk/models/operations.py
from .base_model import BaseModel
from .tags import Tag # Assuming Tag model is defined and available for import

# Forward declaration for nested types if needed, or define simple placeholder classes
class OperationBankAccount(BaseModel):
    """Represents bank account details as nested within an Operation object."""
    def __init__(self, data):
        """
        Initializes an OperationBankAccount object from API response data.

        Args:
            data (dict | None): The dictionary of bank account data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.name = data.get('name')
        self.currency = data.get('currency')
        # Add other fields as per API example for "bankAccount" in Operation
        self.number = data.get('number')
        self.type = data.get('type') # 'Bank' or 'Cash'

class OperationCategory(BaseModel):
    """Represents category details as nested within an Operation object."""
    def __init__(self, data):
        """
        Initializes an OperationCategory object from API response data.

        Args:
            data (dict | None): The dictionary of category data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.name = data.get('name')
        self.type = data.get('type') # 1: income, 2: expenses
        self.kind = data.get('kind')
        self.is_owner_transfer = data.get('isOwnerTransfer')
        self.group = data.get('group') # Could be an ID or a nested object

class OperationContractor(BaseModel):
    """Represents contractor details as nested within an Operation object."""
    def __init__(self, data):
        """
        Initializes an OperationContractor object from API response data.

        Args:
            data (dict | None): The dictionary of contractor data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.name = data.get('name')

class OperationProject(BaseModel):
    """Represents project details as nested within an Operation object."""
    def __init__(self, data):
        """
        Initializes an OperationProject object from API response data.

        Args:
            data (dict | None): The dictionary of project data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.name = data.get('name')
        
class OperationBusinessUnit(BaseModel):
    """Represents business unit details as nested within an Operation object."""
    def __init__(self, data):
        """
        Initializes an OperationBusinessUnit object from API response data.

        Args:
            data (dict | None): The dictionary of business unit data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.name = data.get('name')


class Operation(BaseModel):
    """Represents a financial operation (transaction) from the Adesk API."""
    def __init__(self, data):
        """
        Initializes an Operation object from API response data.

        Args:
            data (dict | None): The dictionary of operation data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.is_splitted = data.get('isSplitted')
        self.split_id = data.get('splitId')
        self.amount = data.get('amount')
        self.date = data.get('date') # Consider datetime conversion
        self.date_iso = data.get('dateIso') # Consider datetime conversion
        self.type = data.get('type') # 1: income, 2: expense
        self.description = data.get('description')
        self.date_formatted = data.get('dateFormatted')
        self.related_date = data.get('relatedDate') # Consider datetime conversion
        self.confirm_accrual = data.get('confirmAccrual')
        self.is_planned = data.get('isPlanned')
        self.is_ready_to_be_confirmed = data.get('isReadyToBeConfirmed')
        self.is_periodic = data.get('isPeriodic')
        self.periodic_chain = data.get('periodicChain') # ID of the chain
        self.period = data.get('period') # e.g. "month"
        self.is_commitment = data.get('isCommitment')
        self.is_transfer = data.get('isTransfer')
        self.bank_account_amount = data.get('bankAccountAmount')
        
        self.bank_account = OperationBankAccount(data.get('bankAccount')) if data.get('bankAccount') else None
        self.category = OperationCategory(data.get('category')) if data.get('category') else None
        self.contractor = OperationContractor(data.get('contractor')) if data.get('contractor') else None
        self.project = OperationProject(data.get('project')) if data.get('project') else None
        self.business_unit = OperationBusinessUnit(data.get('business_unit')) if data.get('business_unit') else None
        
        self.tags = Tag.from_list(data.get('tags')) if data.get('tags') else []

        if self.amount is not None:
            try: self.amount = float(self.amount)
            except (ValueError, TypeError): self.amount = None
        if self.bank_account_amount is not None:
            try: self.bank_account_amount = float(self.bank_account_amount)
            except (ValueError, TypeError): self.bank_account_amount = None
        # Note: Nested objects like bank_account, category, contractor, project, business_unit
        # are instances of their respective simplified model classes defined above.
        # 'tags' is a list of Tag model instances.
