from .client import AdeskClient
from .exceptions import (
    AdeskAPIError,
    AdeskAuthError,
    AdeskBadRequestError,
    AdeskNotFoundError,
    AdeskPaymentRequiredError,
    AdeskRateLimitError,
    AdeskServerError
)
from .models import (
    Project, TransactionCategory, BankAccount, Commitment, LegalEntity,
    Transfer, Operation, Contractor, Requisite, Product, Unit, Tag, Webhook,
    CustomReportGroup, CustomReportEntry, CustomReportValue, CustomReportValueList,
    CustomReportDebtEntry
    # BaseModel and other nested/helper models are not typically exported at top level
    # unless specifically desired for direct use by the SDK user.
)

__version__ = '0.1.0'

__all__ = [
    'AdeskClient',
    # Exceptions
    'AdeskAPIError',
    'AdeskAuthError',
    'AdeskBadRequestError',
    'AdeskNotFoundError',
    'AdeskPaymentRequiredError',
    'AdeskRateLimitError',
    'AdeskServerError',
    # Version
    '__version__',
    # Exported Models
    'Project', 
    'TransactionCategory', 
    'BankAccount', 
    'Commitment', 
    'LegalEntity',
    'Transfer', 
    'Operation', 
    'Contractor', 
    'Requisite', 
    'Product', 
    'Unit', 
    'Tag', 
    'Webhook',
    'CustomReportGroup', 
    'CustomReportEntry', 
    'CustomReportValue', 
    'CustomReportValueList',
    'CustomReportDebtEntry',
]
