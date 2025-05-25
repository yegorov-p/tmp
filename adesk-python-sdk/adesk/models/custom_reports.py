# adesk/models/custom_reports.py
from .base_model import BaseModel
# from .projects import Project # Import if/when projects_data is fully modeled

class CustomReportGroup(BaseModel):
    """Represents a group for custom reports from the Adesk API v2."""
    def __init__(self, data):
        """
        Initializes a CustomReportGroup object from API response data.

        Args:
            data (dict | None): The dictionary of custom report group data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.name = data.get('name')
        self.api_name = data.get('apiName') # Note: API uses apiName
        self.color = data.get('color')
        self.report_section = data.get('reportSection') # Note: API uses reportSection

class CashflowCategoryInfo(BaseModel):
    """Represents cashflow category information, often nested in CustomReportEntry."""
    def __init__(self, data):
        """
        Initializes a CashflowCategoryInfo object from API response data.

        Args:
            data (dict | None): The dictionary of cashflow category info from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.name = data.get('name')
        # self.type = data.get('type') # If applicable

class IntegrationInfo(BaseModel):
    """Represents integration information, often nested in CustomReportEntry."""
    def __init__(self, data):
        """
        Initializes an IntegrationInfo object from API response data.

        Args:
            data (dict | None): The dictionary of integration info from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.source = data.get('source')
            
class CustomReportEntry(BaseModel):
    """Represents an entry (row/metric) within a custom report from the Adesk API v2."""
    def __init__(self, data):
        """
        Initializes a CustomReportEntry object from API response data.

        Args:
            data (dict | None): The dictionary of custom report entry data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.name = data.get('name')
        self.api_name = data.get('apiName')
        self.type = data.get('type')
        self.value_type = data.get('valueType')
        self.total_aggregation_type = data.get('totalAggregationType')
        self.group_id = data.get('groupId')
        self.report_section = data.get('reportSection')
        self.order = data.get('order')
        self.is_editable = data.get('isEditable')
        self.is_persistent = data.get('isPersistent')
        self.system_report_entry = data.get('systemReportEntry')
        self.cashflow_categories = CashflowCategoryInfo.from_list(data.get('cashflowCategories'))
        self.integrations = IntegrationInfo.from_list(data.get('integrations'))
        # Note: 'cashflow_categories' is a list of CashflowCategoryInfo objects.
        # 'integrations' is a list of IntegrationInfo objects.

class CustomReportValue(BaseModel):
    """Represents a data value for a custom report entry from the Adesk API v2."""
    def __init__(self, data):
        """
        Initializes a CustomReportValue object from API response data.

        Args:
            data (dict | None): The dictionary of custom report value data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.entry_id = data.get('entryId')
        self.date = data.get('date') # Consider datetime conversion
        self.amount = data.get('amount')
        self.vat = data.get('vat')
        self.vat_percent = data.get('vatPercent')
        self.currency = data.get('currency')
        self.exchange_rate = data.get('exchangeRate')
        self.description = data.get('description')
        self.project_id = data.get('projectId')
        self.business_unit_id = data.get('businessUnitId')
        self.has_attachments = data.get('hasAttachments')

        # Type conversions for numeric fields
        for attr_name in ['amount', 'vat', 'vat_percent', 'exchange_rate']:
            val = getattr(self, attr_name)
            if val is not None:
                try:
                    setattr(self, attr_name, float(val))
                except (ValueError, TypeError):
                    setattr(self, attr_name, None) # Or log error

# For the list response of CustomReportValues, which includes related entities
class CustomReportValueList(BaseModel):
    """
    Represents the paginated response structure for a list of CustomReportValues,
    including related entities like entries, groups, projects, and business units.
    """
    def __init__(self, data):
        """
        Initializes a CustomReportValueList object from API response data.

        Args:
            data (dict | None): The dictionary from the API list response for custom report values.
        """
        super().__init__(data)
        data = data or {}
        self.items_count = data.get('itemsCount')
        self.total_items_count = data.get('totalItemsCount')
        self.values = CustomReportValue.from_list(data.get('values'))
        self.entries = CustomReportEntry.from_list(data.get('entries'))
        self.groups = CustomReportGroup.from_list(data.get('groups'))
        
        # Placeholder for projects and businessUnits if their models are imported later
        # from .projects import Project # Would be needed
        # self.projects = Project.from_list(data.get('projects'))
        self.projects_data = data.get('projects') # Raw data for now
        
        # from .business_units import BusinessUnit # Would be needed (model not defined yet)
        self.business_units_data = data.get('businessUnits') # Raw data for now
        # Note: 'values', 'entries', 'groups' are lists of their respective model instances.
        # 'projects_data' and 'business_units_data' store raw data for now.

class CustomReportDebtEntryDetail(BaseModel):
    """Represents detailed entry or category information within a CustomReportDebtEntry."""
    def __init__(self, data):
        """
        Initializes a CustomReportDebtEntryDetail object from API response data.

        Args:
            data (dict | None): The dictionary of debt entry detail data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.name = data.get('name')
        self.type = data.get('type') 

class CustomReportDebtEntry(BaseModel):
    """Represents a custom report debt entry from the Adesk API v2."""
    def __init__(self, data):
        """
        Initializes a CustomReportDebtEntry object from API response data.

        Args:
            data (dict | None): The dictionary of custom report debt entry data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.name = data.get('name')
        self.entries = CustomReportDebtEntryDetail.from_list(data.get('entries'))
        self.cashflow_categories = CustomReportDebtEntryDetail.from_list(data.get('cashflowCategories'))
        # Note: 'entries' and 'cashflow_categories' are lists of CustomReportDebtEntryDetail objects.
