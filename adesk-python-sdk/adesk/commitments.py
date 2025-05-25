from adesk_python_sdk.adesk.models import Commitment

class Commitments:
    """
    Provides methods for interacting with Adesk commitments (API v1).
    Accessed via `client.commitments`.
    """
    def __init__(self, client):
        """
        Initializes the Commitments resource.

        Args:
            client (AdeskClient): The AdeskClient instance to use for API calls.
        """
        self.client = client

    def _format_products_data(self, data, **kwargs):
        """
        Internal helper to format product-N-* parameters from kwargs.
        Example: `product_0_product_id=10, product_0_price=100, product_0_quantity=1`
        will be converted to:
        `data['product-0-product_id'] = 10`
        `data['product-0-price'] = 100`
        `data['product-0-quantity'] = 1`

        Args:
            data (dict): The dictionary to which formatted product data will be added.
            **kwargs: Arbitrary keyword arguments, potentially containing product details.
        """
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
        """
        Creates a new commitment.
        Corresponds to Adesk API v1 endpoint: `POST commitment`.

        Product details can be passed as keyword arguments, e.g.,
        `product_0_product_id=1, product_0_price=100.0, product_0_quantity=2, product_0_vat_percent=20`.
        Multiple products can be added by incrementing the index (e.g., `product_1_...`).

        Args:
            amount (float): The amount of the commitment. (Required)
            type (str): The type of commitment (e.g., "income", "outcome"). (Required)
            date (str): The date of the commitment (YYYY-MM-DD). (Required)
            contractor (int): The ID of the contractor. (Required)
            legal_entity (int): The ID of the legal entity. (Required)
            currency (str): The currency code (e.g., "RUB", "USD"). (Required)
            description (str, optional): Description of the commitment.
            project (int, optional): The ID of the associated project.
            vat_percent (float, optional): VAT percentage for the commitment.
            **kwargs: Used for product details (see description above).

        Returns:
            Commitment | None: The created Commitment model instance, or None if creation failed.
        """
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
            
        response_data = self.client.post("commitment", data=data)
        commitment_data = response_data.get("commitment") if response_data else None
        return Commitment(commitment_data) if commitment_data else None

    def update(self, commitment_id, legal_entity, amount=None, type=None, date=None, contractor=None, 
               currency=None, description=None, project=None, vat_percent=None, **kwargs):
        """
        Updates an existing commitment.
        Corresponds to Adesk API v1 endpoint: `POST commitment/<commitment_id>`.

        Product details can be passed as keyword arguments similar to the `create` method.

        Args:
            commitment_id (int): The ID of the commitment to update. (Required)
            legal_entity (int): The ID of the legal entity. (Required, even if not changing)
            amount (float, optional): New amount for the commitment.
            type (str, optional): New type for the commitment.
            date (str, optional): New date for the commitment (YYYY-MM-DD).
            contractor (int, optional): New contractor ID.
            currency (str, optional): New currency code.
            description (str, optional): New description.
            project (int, optional): New project ID.
            vat_percent (float, optional): New VAT percentage.
            **kwargs: Used for product details.

        Returns:
            Commitment | None: The updated Commitment model instance, or None if update failed.
        """
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

        response_data = self.client.post(f"commitment/{commitment_id}", data=data)
        commitment_data = response_data.get("commitment") if response_data else None
        return Commitment(commitment_data) if commitment_data else None

    def delete(self, commitment_id):
        """
        Deletes a commitment.
        Corresponds to Adesk API v1 endpoint: `POST commitment/<commitment_id>/remove`.

        Args:
            commitment_id (int): The ID of the commitment to delete. (Required)

        Returns:
            dict: The response from the API, typically confirming success or failure.
        """
        if not commitment_id:
            raise ValueError("Required parameter missing: commitment_id.")
        return self.client.post(f"commitment/{commitment_id}/remove")

    def list_commitments(self, range_str=None, range_start=None, range_end=None, contractors=None, projects=None):
        """
        Retrieves a list of commitments based on specified filters.
        Corresponds to Adesk API v1 endpoint: `POST commitments`. (Note: Uses POST)

        Args:
            range_str (str, optional): Predefined date range string (e.g., "this_month", "last_quarter").
            range_start (str, optional): Start date for a custom range (YYYY-MM-DD).
            range_end (str, optional): End date for a custom range (YYYY-MM-DD).
            contractors (list[int], optional): List of contractor IDs to filter by.
                                               The Adesk API expects this as 'contractors[]'.
            projects (list[int], optional): List of project IDs to filter by.
                                            The Adesk API expects this as 'projects[]'.

        Returns:
            list[Commitment]: A list of Commitment model instances.
                              Returns an empty list if no commitments are found or in case of an error.
        """
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
            
        response_data = self.client.post("commitments", data=data)
        commitments_list_data = response_data.get("commitments", []) if response_data else []
        return Commitment.from_list(commitments_list_data)
