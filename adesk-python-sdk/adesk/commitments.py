class Commitments:
    def __init__(self, client):
        self.client = client

    def _format_products_data(self, data, **kwargs):
        """Helper to format product-N-* parameters."""
        product_counter = 0
        # Assuming kwargs might contain lists of product details or individual product-N-key items
        # This simplified version expects kwargs like product_0_product_id, product_0_price etc.
        # A more robust version might expect a list of dicts e.g. products=[{'product_id':1, 'price':100}]
        
        products = {} # Intermediate dict to group product data
        for key, value in kwargs.items():
            if key.startswith("product_"):
                parts = key.split('_', 2) # e.g. product_0_product_id -> ['product', '0', 'product_id']
                if len(parts) == 3 and parts[0] == "product" and parts[1].isdigit():
                    index = int(parts[1])
                    product_key = parts[2]
                    if index not in products:
                        products[index] = {}
                    products[index][product_key] = value
        
        # Re-map to product-N-key format
        # Ensure products are numbered 0, 1, 2...
        sorted_indices = sorted(products.keys())
        
        for i, index in enumerate(sorted_indices):
            product_details = products[index]
            if "product_id" in product_details and "price" in product_details and "quantity" in product_details:
                 data[f'product-{i}-product_id'] = product_details['product_id']
                 data[f'product-{i}-price'] = product_details['price']
                 data[f'product-{i}-quantity'] = product_details['quantity']
                 if "vat_percent" in product_details:
                     data[f'product-{i}-vat_percent'] = product_details['vat_percent']
            else:
                # This indicates a potential issue if a product is partially defined.
                # Depending on strictness, could raise an error or log a warning.
                # For now, we'll assume valid product structures are passed via kwargs.
                pass # Or handle error for incomplete product data

    def create(self, amount, type, date, contractor, legal_entity, currency, description=None, project=None, vat_percent=None, **kwargs):
        if not all([amount, type, date, contractor, legal_entity, currency]):
            raise ValueError("Required parameters missing: amount, type, date, contractor, legal_entity, currency.")
        
        data = {
            "amount": amount,
            "type": type,
            "date": date,
            "contractor": contractor,
            "legal_entity": legal_entity,
            "currency": currency,
        }
        if description is not None:
            data["description"] = description
        if project is not None:
            data["project"] = project
        if vat_percent is not None:
            data["vat_percent"] = vat_percent
        
        self._format_products_data(data, **kwargs)
            
        response = self.client.post("commitment", data=data)
        return response.get("commitment")

    def update(self, commitment_id, legal_entity, amount=None, type=None, date=None, contractor=None, 
               currency=None, description=None, project=None, vat_percent=None, **kwargs):
        if not commitment_id or legal_entity is None: # legal_entity can be 0
            raise ValueError("Required parameters missing: commitment_id, legal_entity.")

        data = {"legal_entity": legal_entity} # legal_entity is required for update
        if amount is not None:
            data["amount"] = amount
        if type is not None:
            data["type"] = type
        if date is not None:
            data["date"] = date
        if contractor is not None:
            data["contractor"] = contractor
        if currency is not None:
            data["currency"] = currency
        if description is not None:
            data["description"] = description
        if project is not None:
            data["project"] = project
        if vat_percent is not None:
            data["vat_percent"] = vat_percent
            
        self._format_products_data(data, **kwargs)

        response = self.client.post(f"commitment/{commitment_id}", data=data)
        return response.get("commitment")

    def delete(self, commitment_id):
        if not commitment_id:
            raise ValueError("Required parameter missing: commitment_id.")
        return self.client.post(f"commitment/{commitment_id}/remove")

    def list_commitments(self, range_str=None, range_start=None, range_end=None, contractors=None, projects=None):
        data = {}
        if range_str is not None:
            data["range_str"] = range_str
        if range_start is not None:
            data["range_start"] = range_start
        if range_end is not None:
            data["range_end"] = range_end
        if contractors is not None: # Expects a list of IDs
            data["contractors[]"] = contractors
        if projects is not None: # Expects a list of IDs
            data["projects[]"] = projects
            
        response = self.client.post("commitments", data=data)
        return response.get("commitments")
