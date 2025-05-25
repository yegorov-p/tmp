class Warehouse:
    def __init__(self, client):
        self.client = client

    def list_products(self, search=None):
        """List products and services."""
        params = {}
        if search is not None:
            params["search"] = search
        response = self.client.get("warehouse/products", params=params)
        return response.get("products")

    def add_product_or_service(self, type, name, sku=None, description=None, unit_id=None, 
                               unit_name=None, unit_symbol=None, unit_code=None, 
                               with_initial_batch=None, initial_batch_date=None, 
                               initial_batch_quantity=None, initial_batch_price=None, 
                               initial_batch_currency=None, initial_batch_legal_entity=None):
        """Add a product or service."""
        if type is None or not name:
            raise ValueError("Required parameters missing: type, name.")
        if type == 1 and not unit_id and not (unit_name and unit_symbol):
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
            
        response = self.client.post("warehouse/product", data=data)
        return response.get("product")

    def update_product_or_service(self, product_id, name=None, sku=None, description=None, 
                                  unit_id=None, unit_name=None, unit_symbol=None, unit_code=None, 
                                  with_initial_batch=None, initial_batch_date=None, 
                                  initial_batch_quantity=None, initial_batch_price=None, 
                                  initial_batch_currency=None, initial_batch_legal_entity=None):
        """Update a product or service."""
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

        response = self.client.post(f"warehouse/product/{product_id}", data=data)
        return response.get("product")

    def delete_product_or_service(self, product_id):
        """Delete a product or service."""
        if not product_id:
            raise ValueError("Required parameter missing: product_id.")
        return self.client.post(f"warehouse/product/{product_id}/remove")

    def list_units(self):
        """List units of measurement."""
        response = self.client.get("warehouse/units")
        return response.get("units")

    def list_commodity_costs(self, projects):
        """List commodity costs."""
        if not projects: # Expects a list of project IDs
            raise ValueError("Required parameter missing: projects.")
        params = {"projects[]": projects}
        response = self.client.get("warehouse/commodity-costs", params=params)
        return response.get("commodity-costs") # API returns 'commodity-costs'

    def add_commodity_expense(self, date, legal_entity_id, project_id, products_json_string):
        """Add a commodity expense."""
        if not all([date, legal_entity_id is not None, project_id is not None, products_json_string]):
            raise ValueError("Required parameters missing: date, legal_entity_id, project_id, products_json_string.")
        
        data = {
            "date": date, # YYYY-MM-DD
            "legal_entity_id": legal_entity_id,
            "project_id": project_id,
            "products": products_json_string, # API expects a JSON string for 'products'
        }
        response = self.client.post("warehouse/expenses", data=data)
        return response.get("shipment")

    def update_commodity_expense(self, shipment_id, date, legal_entity_id, project_id, products_json_string):
        """Update a commodity expense."""
        if not all([shipment_id, date, legal_entity_id is not None, project_id is not None, products_json_string]):
            raise ValueError("Required parameters missing: shipment_id, date, legal_entity_id, project_id, products_json_string.")

        data = {
            "date": date, # YYYY-MM-DD
            "legal_entity_id": legal_entity_id,
            "project_id": project_id,
            "products": products_json_string, # API expects a JSON string for 'products'
        }
        response = self.client.post(f"warehouse/expenses/{shipment_id}", data=data)
        return response.get("shipment")

    def delete_commodity_expense(self, shipment_id):
        """Delete a commodity expense."""
        if not shipment_id:
            raise ValueError("Required parameter missing: shipment_id.")
        return self.client.post(f"warehouse/expenses/{shipment_id}/remove")
