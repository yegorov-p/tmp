# adesk/models/projects.py
from .base_model import BaseModel

class ProjectCategory(BaseModel):
    """Represents a project category as nested within a Project object."""
    def __init__(self, data):
        """
        Initializes a ProjectCategory object from API response data.

        Args:
            data (dict | None): The dictionary of project category data from the API.
        """
        super().__init__(data)
        data = data or {} # Ensure data is a dict even if None was passed initially
        self.id = data.get('id')
        self.name = data.get('name')

class ProjectManager(BaseModel):
    """Represents a project manager as nested within a Project object."""
    def __init__(self, data):
        """
        Initializes a ProjectManager object from API response data.

        Args:
            data (dict | None): The dictionary of project manager data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.name = data.get('name')
            
class DealContractor(BaseModel):
    """Represents a deal contractor as nested within a Project object."""
    def __init__(self, data):
        """
        Initializes a DealContractor object from API response data.

        Args:
            data (dict | None): The dictionary of deal contractor data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.name = data.get('name')

class DealLegalEntity(BaseModel):
    """Represents a deal legal entity as nested within a Project object."""
    def __init__(self, data):
        """
        Initializes a DealLegalEntity object from API response data.

        Args:
            data (dict | None): The dictionary of deal legal entity data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.name = data.get('name')

class Project(BaseModel):
    """Represents a project from the Adesk API."""
    def __init__(self, data):
        """
        Initializes a Project object from API response data.

        Args:
            data (dict | None): The dictionary of project data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.created = data.get('created') # Consider datetime conversion later
        self.income = data.get('income')
        self.outcome = data.get('outcome')
        self.gross_profit = data.get('grossProfit') # Note API uses grossProfit
        self.profitability = data.get('profitability')
        self.is_archived = data.get('isArchived')
        self.plan_income = data.get('planIncome')
        self.plan_outcome = data.get('planOutcome')
        self.is_deal = data.get('isDeal')
        self.category = ProjectCategory(data.get('category')) if data.get('category') is not None else None
        self.manager = ProjectManager(data.get('manager')) if data.get('manager') is not None else None
        self.deal_contractor = DealContractor(data.get('deal_contractor')) if data.get('deal_contractor') is not None else None
        self.deal_legal_entity = DealLegalEntity(data.get('deal_legal_entity')) if data.get('deal_legal_entity') is not None else None
        # Add other fields as per API response example
        # Example: self.status = data.get('status')
        # Example: self.tags = [Tag(tag_data) for tag_data in data.get('tags', [])] if data.get('tags') else []
        # For now, keeping it to the explicitly listed fields in the prompt.
