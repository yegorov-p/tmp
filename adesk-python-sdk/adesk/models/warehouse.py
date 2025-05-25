# adesk/models/warehouse.py
from .base_model import BaseModel
from .commitments import ShipmentProduct # Re-use if structure is identical

class Unit(BaseModel):
    """Represents a unit of measurement for products from the Adesk API."""
    def __init__(self, data):
        """
        Initializes a Unit object from API response data.

        Args:
            data (dict | None): The dictionary of unit data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.symbol = data.get('symbol')
        self.name = data.get('name')
        self.code = data.get('code')
        self.fractional = data.get('fractional') # boolean

class InitialBatch(BaseModel):
    """Represents an initial batch of a product, nested within a Product object."""
    def __init__(self, data):
        """
        Initializes an InitialBatch object from API response data.

        Args:
            data (dict | None): The dictionary of initial batch data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.date = data.get('date') # Consider datetime conversion
        self.quantity = data.get('quantity')
        self.price = data.get('price')
        self.currency = data.get('currency')
        # self.legal_entity data might be a dict or an ID.
        self.legal_entity_data = data.get('legalEntity') # Store raw for now

        if self.quantity is not None:
            try: self.quantity = float(self.quantity)
            except (ValueError, TypeError): self.quantity = None
        if self.price is not None:
            try: self.price = float(self.price)
            except (ValueError, TypeError): self.price = None

class Product(BaseModel):
    """Represents a product or service from the Adesk API warehouse."""
    def __init__(self, data):
        """
        Initializes a Product object from API response data.

        Args:
            data (dict | None): The dictionary of product/service data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.type = data.get('type') # 1: product, 2: service
        self.name = data.get('name')
        self.sku = data.get('sku')
        self.description = data.get('description')
        self.unit = Unit(data.get('unit')) if data.get('unit') is not None else None
        self.initial_batch = InitialBatch(data.get('initialBatch')) if data.get('initialBatch') is not None else None
        # Additional fields that might be present:
        self.balance = data.get('balance') # for products
        self.average_cost_price = data.get('averageCostPrice') # for products

        if self.balance is not None:
            try: self.balance = float(self.balance)
            except (ValueError, TypeError): self.balance = None
        if self.average_cost_price is not None:
            try: self.average_cost_price = float(self.average_cost_price)
            except (ValueError, TypeError): self.average_cost_price = None
        # Note: 'unit' is a Unit object, 'initial_batch' is an InitialBatch object.

class CommodityCost(BaseModel):
    """Represents commodity cost details for a product in a project."""
    def __init__(self, data):
        """
        Initializes a CommodityCost object from API response data.
        This typically comes from the 'warehouse/commodity-costs' endpoint.

        Args:
            data (dict | None): The dictionary of commodity cost data from the API.
        """
        super().__init__(data)
        data = data or {}
        # Based on API docs, this endpoint returns a list of products with cost price details.
        # Each item in the list looks like a Product with additional cost fields.
        self.product_id = data.get('product_id') # or just 'id'
        self.name = data.get('name') # product name
        self.sku = data.get('sku')
        self.unit_name = data.get('unit_name')
        self.unit_symbol = data.get('unit_symbol')
        self.project_id = data.get('project_id')
        self.quantity = data.get('quantity')
        self.cost_price = data.get('cost_price')
        self.total_cost = data.get('total_cost') # quantity * cost_price

        if self.quantity is not None:
            try: self.quantity = float(self.quantity)
            except (ValueError, TypeError): self.quantity = None
        if self.cost_price is not None:
            try: self.cost_price = float(self.cost_price)
            except (ValueError, TypeError): self.cost_price = None
        if self.total_cost is not None:
            try: self.total_cost = float(self.total_cost)
            except (ValueError, TypeError): self.total_cost = None


# For response of add/update commodity expense (warehouse/expenses)
# This structure is similar to Commitment.Shipment
class WarehouseShipmentModel(BaseModel):
    """Represents a commodity expense shipment record from the Adesk API."""
    def __init__(self, data):
        """
        Initializes a WarehouseShipmentModel object from API response data.
        This is typically the response from creating or updating a commodity expense.

        Args:
            data (dict | None): The dictionary of shipment data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id') # This is the shipment ID (расход/списание)
        # The API doc says "объект отгрузки", which is similar to commitment's shipment object.
        # It contains 'batches' which are products with quantity, price, etc.
        self.batches = ShipmentProduct.from_list(data.get('batches'))

        # It might also contain other top-level fields from the request like:
        self.date = data.get('date')
        self.legal_entity_id = data.get('legal_entity_id')
        self.project_id = data.get('project_id')
        # And potentially the 'products' JSON string if API echoes it, though unlikely.
        # self.products_raw_json = data.get('products')
        # Note: 'batches' is a list of ShipmentProduct model instances.
