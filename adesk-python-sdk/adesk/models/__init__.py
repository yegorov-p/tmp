# adesk/models/__init__.py
from .base_model import BaseModel
from .projects import Project, ProjectCategory, ProjectManager, DealContractor, DealLegalEntity
from .transactions import TransactionCategory
from .bank_accounts import BankAccount
from .commitments import Commitment, Shipment, ShipmentProduct
from .legal_entities import LegalEntity, VatRate
from .transfers import Transfer, TransferAccountInfo
from .operations import (
    Operation, OperationBankAccount, OperationCategory, 
    OperationContractor, OperationProject, OperationBusinessUnit
)
from .contractors import Contractor
from .requisites import Requisite
from .warehouse import (
    Product, Unit, InitialBatch, CommodityCost, 
    WarehouseShipmentModel # Renamed from ShipmentModel to avoid potential future conflicts
)
from .tags import Tag
from .webhooks import Webhook
from .custom_reports import (
    CustomReportGroup, CustomReportEntry, CustomReportValue, CustomReportValueList,
    CustomReportDebtEntry, CashflowCategoryInfo, IntegrationInfo, CustomReportDebtEntryDetail
)

__all__ = [
    'BaseModel',
    # Project models
    'Project', 'ProjectCategory', 'ProjectManager', 'DealContractor', 'DealLegalEntity',
    # Transaction models (currently only TransactionCategory)
    'TransactionCategory',
    # BankAccount models
    'BankAccount',
    # Commitment models
    'Commitment', 'Shipment', 'ShipmentProduct',
    # LegalEntity models
    'LegalEntity', 'VatRate',
    # Transfer models
    'Transfer', 'TransferAccountInfo',
    # Operation models
    'Operation', 'OperationBankAccount', 'OperationCategory', 'OperationContractor', 
    'OperationProject', 'OperationBusinessUnit',
    # Contractor models
    'Contractor',
    # Requisite models
    'Requisite',
    # Warehouse models
    'Product', 'Unit', 'InitialBatch', 'CommodityCost', 'WarehouseShipmentModel',
    # Tag models
    'Tag',
    # Webhook models
    'Webhook',
    # Custom Report (V2) models
    'CustomReportGroup', 'CustomReportEntry', 'CustomReportValue', 'CustomReportValueList',
    'CustomReportDebtEntry', 'CashflowCategoryInfo', 'IntegrationInfo', 'CustomReportDebtEntryDetail',
]
