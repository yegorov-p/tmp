from adesk_python_sdk.adesk.models import Product, Unit, CommodityCost, WarehouseShipmentModel

class Warehouse:
    """
    Provides methods for interacting with Adesk warehouse resources (products, services, units, etc.) (API v1).
    Accessed via `client.warehouse`.
    """
    def __init__(self, client):
        """
        Initializes the Warehouse resource.

        Args:
            client (AdeskClient): The AdeskClient instance to use for API calls.
        """
        self.client = client

    def list_products(self, search=None):
        """
        Retrieves a list of products and services from the warehouse.
        Corresponds to Adesk API v1 endpoint: `GET warehouse/products`.

        Args:
            search (str, optional): A search string to filter products/services by name or SKU.

        Returns:
            list[Product]: A list of Product model instances.
                           Returns an empty list if none are found or in case of an error.
        """
        params = {}
        if search is not None:
            params["search"] = search
        response_data = self.client.get("warehouse/products", params=params)
        products_data = response_data.get("products", []) if response_data else []
        return Product.from_list(products_data)

    def add_product_or_service(self, type, name, sku=None, description=None, unit_id=None, 
                               unit_name=None, unit_symbol=None, unit_code=None, 
                               with_initial_batch=None, initial_batch_date=None, 
                               initial_batch_quantity=None, initial_batch_price=None, 
                               initial_batch_currency=None, initial_batch_legal_entity=None):
        """
        Adds a new product or service to the warehouse.
        Corresponds to Adesk API v1 endpoint: `POST warehouse/product`.

        Args:
            type (int): Type of item (1 for product, 2 for service). (Required)
            name (str): Name of the product or service. (Required)
            sku (str, optional): Stock Keeping Unit (SKU) for the product.
            description (str, optional): Description of the product or service.
            unit_id (int, optional): ID of an existing unit of measurement.
                                     Required for product (type 1) if unit details not provided.
            unit_name (str, optional): Name of the unit (e.g., "piece", "hour").
                                       Used if `unit_id` is not provided.
            unit_symbol (str, optional): Symbol for the unit (e.g., "pc.", "hr.").
                                         Used if `unit_id` is not provided.
            unit_code (str, optional): Numeric code for the unit (e.g., OKEI code).
            with_initial_batch (bool, optional): If True, creates an initial batch for the product.
            initial_batch_date (str, optional): Date for the initial batch (YYYY-MM-DD).
                                                Required if `with_initial_batch` is True.
            initial_batch_quantity (float, optional): Quantity for the initial batch.
                                                     Required if `with_initial_batch` is True.
            initial_batch_price (float, optional): Price per unit for the initial batch.
                                                   Required if `with_initial_batch` is True.
            initial_batch_currency (str, optional): Currency for the initial batch (e.g., "RUB").
                                                    Required if `with_initial_batch` is True.
            initial_batch_legal_entity (int, optional): Legal entity ID for the initial batch.
                                                        Required if `with_initial_batch` is True.

        Returns:
            Product | None: The created Product model instance, or None if creation failed.
        """
        if type is None or not name:
            raise ValueError("Required parameters missing: type, name.")
        if type == 1 and not unit_id and not (unit_name and unit_symbol): # Product
            raise ValueError("For product (type 1), unit_id or (unit_name and unit_symbol) are required.")
        if with_initial_batch and not all([initial_batch_date, initial_batch_quantity is not None, 
                                           initial_batch_price is not None, initial_batch_currency, 
                                           initial_batch_legal_entity is not None]):
            raise ValueError("Missing required parameters for initial batch.")

        data = {"type": type, "name": name}
        if sku is not None: data["sku"] = sku
        if description is not None: data["description"] = description
        if unit_id is not None: data["unit_id"] = unit_id
        if unit_name is not None: data["unit_name"] = unit_name
        if unit_symbol is not None: data["unit_symbol"] = unit_symbol
        if unit_code is not None: data["unit_code"] = unit_code
        if with_initial_batch is not None: data["with_initial_batch"] = with_initial_batch
        if initial_batch_date is not None: data["initial_batch_date"] = initial_batch_date
        if initial_batch_quantity is not None: data["initial_batch_quantity"] = initial_batch_quantity
        if initial_batch_price is not None: data["initial_batch_price"] = initial_batch_price
        if initial_batch_currency is not None: data["initial_batch_currency"] = initial_batch_currency
        if initial_batch_legal_entity is not None: data["initial_batch_legal_entity"] = initial_batch_legal_entity
            
        response_data = self.client.post("warehouse/product", data=data)
        product_data = response_data.get("product") if response_data else None
        return Product(product_data) if product_data else None

    def update_product_or_service(self, product_id, name=None, sku=None, description=None, 
                                  unit_id=None, unit_name=None, unit_symbol=None, unit_code=None, 
                                  with_initial_batch=None, initial_batch_date=None, 
                                  initial_batch_quantity=None, initial_batch_price=None, 
                                  initial_batch_currency=None, initial_batch_legal_entity=None):
        """
        Updates an existing product or service.
        Corresponds to Adesk API v1 endpoint: `POST warehouse/product/<product_id>`.
        Note: Updating initial batch details via this method might not be supported by the API.

        Args:
            product_id (int): The ID of the product or service to update. (Required)
            name (str, optional): New name for the product/service.
            sku (str, optional): New SKU.
            description (str, optional): New description.
            unit_id (int, optional): New unit ID.
            unit_name (str, optional): New unit name (if not using `unit_id`).
            unit_symbol (str, optional): New unit symbol (if not using `unit_id`).
            unit_code (str, optional): New unit code.
            with_initial_batch (bool, optional): Flag for initial batch (effect on update is uncertain).
            initial_batch_date (str, optional): Date for initial batch (effect on update is uncertain).
            initial_batch_quantity (float, optional): Quantity for initial batch (effect on update is uncertain).
            initial_batch_price (float, optional): Price for initial batch (effect on update is uncertain).
            initial_batch_currency (str, optional): Currency for initial batch (effect on update is uncertain).
            initial_batch_legal_entity (int, optional): Legal entity for initial batch (effect on update is uncertain).

        Returns:
            Product | None: The updated Product model instance, or None if update failed.
        """
        if not product_id:
            raise ValueError("Required parameter missing: product_id.")

        data = {}
        if name is not None: data["name"] = name
        if sku is not None: data["sku"] = sku
        if description is not None: data["description"] = description
        if unit_id is not None: data["unit_id"] = unit_id
        if unit_name is not None: data["unit_name"] = unit_name
        if unit_symbol is not None: data["unit_symbol"] = unit_symbol
        if unit_code is not None: data["unit_code"] = unit_code
        # Note: API does not seem to support updating initial batch details this way.
        # The with_initial_batch and related params are typically for creation.
        # Keeping them here as per method signature but they might not have an effect on update.
        if with_initial_batch is not None: data["with_initial_batch"] = with_initial_batch
        if initial_batch_date is not None: data["initial_batch_date"] = initial_batch_date
        if initial_batch_quantity is not None: data["initial_batch_quantity"] = initial_batch_quantity
        if initial_batch_price is not None: data["initial_batch_price"] = initial_batch_price
        if initial_batch_currency is not None: data["initial_batch_currency"] = initial_batch_currency
        if initial_batch_legal_entity is not None: data["initial_batch_legal_entity"] = initial_batch_legal_entity

        response_data = self.client.post(f"warehouse/product/{product_id}", data=data)
        product_data = response_data.get("product") if response_data else None
        return Product(product_data) if product_data else None

    def delete_product_or_service(self, product_id):
        """
        Deletes a product or service from the warehouse.
        Corresponds to Adesk API v1 endpoint: `POST warehouse/product/<product_id>/remove`.

        Args:
            product_id (int): The ID of the product or service to delete. (Required)

        Returns:
            dict: The response from the API, typically confirming success or failure.
        """
        if not product_id:
            raise ValueError("Required parameter missing: product_id.")
        return self.client.post(f"warehouse/product/{product_id}/remove")

    def list_units(self):
        """
        Retrieves a list of all available units of measurement.
        Corresponds to Adesk API v1 endpoint: `GET warehouse/units`.

        Returns:
            list[Unit]: A list of Unit model instances.
                        Returns an empty list if none are found or in case of an error.
        """
        response_data = self.client.get("warehouse/units")
        units_data = response_data.get("units", []) if response_data else []
        return Unit.from_list(units_data)

    def list_commodity_costs(self, projects):
        """
        Retrieves commodity costs for specified projects.
        Corresponds to Adesk API v1 endpoint: `GET warehouse/commodity-costs`.

        Args:
            projects (list[int]): A list of project IDs for which to retrieve commodity costs. (Required)
                                  The Adesk API expects this as 'projects[]'.

        Returns:
            list[CommodityCost]: A list of CommodityCost model instances.
                                 Returns an empty list if none are found or in case of an error.
        """
        if not projects: # Expects a list of project IDs
            raise ValueError("Required parameter missing: projects.")
        params = {"projects[]": projects}
        response_data = self.client.get("warehouse/commodity-costs", params=params)
        # API returns 'commodity-costs' key, ensure model handling is consistent
        costs_data = response_data.get("commodity-costs", []) if response_data else []
        return CommodityCost.from_list(costs_data)

    def add_commodity_expense(self, date, legal_entity_id, project_id, products_json_string):
        """
        Adds a commodity expense (shipment/write-off).
        Corresponds to Adesk API v1 endpoint: `POST warehouse/expenses`.

        Args:
            date (str): Date of the expense (YYYY-MM-DD). (Required)
            legal_entity_id (int): ID of the legal entity associated with the expense. (Required)
            project_id (int): ID of the project associated with the expense. (Required)
            products_json_string (str): A JSON string representing the list of products,
                                        their quantities, and prices. Example:
                                        `'[{"product_id": 1, "quantity": 10, "price": 5.00}, ...]'`
                                        (Required)
        Returns:
            WarehouseShipmentModel | None: The created WarehouseShipmentModel instance, or None if creation failed.
        """
        if not all([date, legal_entity_id is not None, project_id is not None, products_json_string]):
            raise ValueError("Required parameters missing: date, legal_entity_id, project_id, products_json_string.")
        
        data = {
            "date": date, # YYYY-MM-DD
            "legal_entity_id": legal_entity_id,
            "project_id": project_id,
            "products": products_json_string, # API expects a JSON string for 'products'
        }
        response_data = self.client.post("warehouse/expenses", data=data)
        shipment_data = response_data.get("shipment") if response_data else None
        return WarehouseShipmentModel(shipment_data) if shipment_data else None

    def update_commodity_expense(self, shipment_id, date, legal_entity_id, project_id, products_json_string):
        """
        Updates an existing commodity expense (shipment/write-off).
        Corresponds to Adesk API v1 endpoint: `POST warehouse/expenses/<shipment_id>`.

        Args:
            shipment_id (int): The ID of the shipment/expense to update. (Required)
            date (str): New date for the expense (YYYY-MM-DD). (Required)
            legal_entity_id (int): New legal entity ID. (Required)
            project_id (int): New project ID. (Required)
            products_json_string (str): New JSON string for products. (Required)

        Returns:
            WarehouseShipmentModel | None: The updated WarehouseShipmentModel instance, or None if update failed.
        """
        if not all([shipment_id, date, legal_entity_id is not None, project_id is not None, products_json_string]):
            raise ValueError("Required parameters missing: shipment_id, date, legal_entity_id, project_id, products_json_string.")

        data = {
            "date": date, # YYYY-MM-DD
            "legal_entity_id": legal_entity_id,
            "project_id": project_id,
            "products": products_json_string, # API expects a JSON string for 'products'
        }
        response_data = self.client.post(f"warehouse/expenses/{shipment_id}", data=data)
        shipment_data = response_data.get("shipment") if response_data else None
        return WarehouseShipmentModel(shipment_data) if shipment_data else None

    def delete_commodity_expense(self, shipment_id):
        """
        Deletes a commodity expense (shipment/write-off).
        Corresponds to Adesk API v1 endpoint: `POST warehouse/expenses/<shipment_id>/remove`.

        Args:
            shipment_id (int): The ID of the shipment/expense to delete. (Required)

        Returns:
            dict: The response from the API, typically confirming success or failure.
        """
        if not shipment_id:
            raise ValueError("Required parameter missing: shipment_id.")
        return self.client.post(f"warehouse/expenses/{shipment_id}/remove")
