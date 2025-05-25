# adesk/models/commitments.py
from .base_model import BaseModel
# For now, assume IDs or simple dicts for linked objects like LegalEntity, Contractor, Project, Transaction.
# Full model hydration for these can be added later if needed.

class ShipmentProduct(BaseModel):
    """Represents a product within a shipment, often nested in Commitments."""
    def __init__(self, data):
        """
        Initializes a ShipmentProduct object from API response data.

        Args:
            data (dict | None): The dictionary of shipment product data from the API.
        """
        super().__init__(data)
        data = data or {}
        # Assuming product_data is a dict like {'id': 1, 'name': '...'} or just an ID.
        self.product_data = data.get('product') 
        self.type = data.get('type')
        self.date = data.get('date') # Consider datetime conversion
        self.quantity = data.get('quantity')
        self.price = data.get('price')
        self.vat = data.get('vat')
        self.vat_percent = data.get('vatPercent')

        if self.quantity is not None:
            try: self.quantity = float(self.quantity)
            except (ValueError, TypeError): self.quantity = None
        if self.price is not None:
            try: self.price = float(self.price)
            except (ValueError, TypeError): self.price = None
        if self.vat is not None:
            try: self.vat = float(self.vat)
            except (ValueError, TypeError): self.vat = None
        if self.vat_percent is not None:
            try: self.vat_percent = float(self.vat_percent)
            except (ValueError, TypeError): self.vat_percent = None


class Shipment(BaseModel):
    """Represents a shipment, often nested within a Commitment object."""
    def __init__(self, data):
        """
        Initializes a Shipment object from API response data.

        Args:
            data (dict | None): The dictionary of shipment data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.batches = ShipmentProduct.from_list(data.get('batches'))


class Commitment(BaseModel):
    """Represents a financial commitment from the Adesk API."""
    def __init__(self, data):
        """
        Initializes a Commitment object from API response data.

        Args:
            data (dict | None): The dictionary of commitment data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.amount = data.get('amount')
        self.vat = data.get('vat')
        self.vat_percent = data.get('vatPercent')
        self.description = data.get('description')
        self.date = data.get('date') # Consider datetime conversion
        self.date_formatted = data.get('dateFormatted') 
        # Placeholders for now, assuming these are dicts or IDs from API
        self.legal_entity = data.get('legalEntity') 
        self.contractor = data.get('contractor')   
        self.project_id = data.get('project')      
        self.type = data.get('type') # 1: incoming, 2: outgoing
        self.currency = data.get('currency') # e.g. "RUB"
        self.transaction = data.get('transaction') # Placeholder
        self.is_shipment = data.get('isShipment')
        self.shipment = Shipment(data.get('shipment')) if data.get('shipment') else None

        if self.amount is not None:
            try: self.amount = float(self.amount)
            except (ValueError, TypeError): self.amount = None
        if self.vat is not None:
            try: self.vat = float(self.vat)
            except (ValueError, TypeError): self.vat = None
        if self.vat_percent is not None:
            try: self.vat_percent = float(self.vat_percent)
            except (ValueError, TypeError): self.vat_percent = None
        # Note: linked objects like legal_entity, contractor, transaction, project
        # are stored as raw data (IDs or dicts) as per current implementation.
        # Full model hydration for these could be added if their complete models are available
        # and the API consistently returns enough data for them.
