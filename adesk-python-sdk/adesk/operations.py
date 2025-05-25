from adesk_python_sdk.adesk.models import Operation

class Operations:
    """
    Provides methods for interacting with Adesk operations (transactions) (API v1).
    Accessed via `client.operations`. Note that the API endpoint is 'transaction(s)'.
    """
    def __init__(self, client):
        """
        Initializes the Operations resource.

        Args:
            client (AdeskClient): The AdeskClient instance to use for API calls.
        """
        self.client = client

    def create(self, date, type, amount, bank_account, apply_import_rules=None, category=None, 
               project=None, business_unit=None, contractor=None, description=None, 
               related_date=None, is_periodic=None, period=None, repetition_end_date=None, 
               is_commitment=None, is_planned=None, is_splitted=None, parts=None, tags=None):
        """
        Creates a new operation (transaction).
        Corresponds to Adesk API v1 endpoint: `POST transaction`.

        Args:
            date (str): Date of the operation (YYYY-MM-DD). (Required)
            type (str): Type of operation ("income" or "outcome"). (Required)
            amount (float): Amount of the operation. (Required)
            bank_account (int): ID of the bank account. (Required)
            apply_import_rules (bool, optional): Whether to apply import rules.
            category (int, optional): Category ID for the operation.
            project (int, optional): Project ID associated with the operation.
            business_unit (int, optional): Business unit ID.
            contractor (int, optional): Contractor ID.
            description (str, optional): Description of the operation.
            related_date (str, optional): Related date (YYYY-MM-DD).
            is_periodic (bool, optional): If True, marks the operation as periodic.
            period (str, optional): Periodicity if `is_periodic` is True (e.g., "monthly").
            repetition_end_date (str, optional): End date for periodic repetition (YYYY-MM-DD).
            is_commitment (bool, optional): If True, links to a commitment.
            is_planned (bool, optional): If True, marks as a planned operation.
            is_splitted (bool, optional): If True, indicates the operation is split.
            parts (str, optional): JSON string representing parts if `is_splitted` is True.
            tags (str, optional): Comma-separated string of tag IDs.

        Returns:
            Operation | None: The created Operation model instance, or None if creation failed.
        """
        if not all([date, type, amount is not None, bank_account is not None]): # amount can be 0
            raise ValueError("Required parameters missing: date, type, amount, bank_account.")

        data = {
            "date": date, # YYYY-MM-DD
            "type": type, # 'income' or 'outcome'
            "amount": amount,
            "bank_account": bank_account, # ID
        }
        if apply_import_rules is not None:
            data["apply_import_rules"] = apply_import_rules
        if category is not None:
            data["category"] = category
        if project is not None:
            data["project"] = project
        if business_unit is not None:
            data["business_unit"] = business_unit
        if contractor is not None:
            data["contractor"] = contractor
        if description is not None:
            data["description"] = description
        if related_date is not None: # YYYY-MM-DD
            data["related_date"] = related_date
        if is_periodic is not None:
            data["is_periodic"] = is_periodic
        if period is not None:
            data["period"] = period
        if repetition_end_date is not None: # YYYY-MM-DD
            data["repetition_end_date"] = repetition_end_date
        if is_commitment is not None:
            data["is_commitment"] = is_commitment
        if is_planned is not None:
            data["is_planned"] = is_planned
        if is_splitted is not None:
            data["is_splitted"] = is_splitted
        if parts is not None: # JSON string
            data["parts"] = parts
        if tags is not None: # comma-separated string of IDs
            data["tags"] = tags
            
        response_data = self.client.post("transaction", data=data)
        op_data = response_data.get("transaction") if response_data else None
        return Operation(op_data) if op_data else None

    def update(self, transaction_id, date, bank_account, amount, category=None, project=None, 
               business_unit=None, contractor=None, description=None, related_date=None, 
               is_periodic=None, period=None, repetition_end_date=None, is_commitment=None, 
               is_planned=None, is_splitted=None, parts=None, periodic_edit_type=None, tags=None):
        """
        Updates an existing operation (transaction).
        Corresponds to Adesk API v1 endpoint: `POST transaction/<transaction_id>`.

        Args:
            transaction_id (int): ID of the transaction to update. (Required)
            date (str): New date for the operation (YYYY-MM-DD). (Required)
            bank_account (int): New bank account ID. (Required)
            amount (float): New amount for the operation. (Required)
            category (int, optional): New category ID.
            project (int, optional): New project ID.
            business_unit (int, optional): New business unit ID.
            contractor (int, optional): New contractor ID.
            description (str, optional): New description.
            related_date (str, optional): New related date (YYYY-MM-DD).
            is_periodic (bool, optional): Update periodic status.
            period (str, optional): New period if periodic.
            repetition_end_date (str, optional): New repetition end date if periodic (YYYY-MM-DD).
            is_commitment (bool, optional): Update commitment link status.
            is_planned (bool, optional): Update planned status.
            is_splitted (bool, optional): Update splitted status.
            parts (str, optional): New JSON string for parts if splitted.
            periodic_edit_type (str, optional): For periodic transactions, "this" or "this-and-following".
            tags (str, optional): New comma-separated string of tag IDs.

        Returns:
            Operation | None: The updated Operation model instance, or None if update failed.
        """
        if not all([transaction_id, date, bank_account is not None, amount is not None]): # bank_account/amount can be 0
            raise ValueError("Required parameters missing: transaction_id, date, bank_account, amount.")

        data = {
            "date": date, # YYYY-MM-DD
            "bank_account": bank_account, # ID
            "amount": amount,
        }
        if category is not None:
            data["category"] = category
        if project is not None:
            data["project"] = project
        if business_unit is not None:
            data["business_unit"] = business_unit
        if contractor is not None:
            data["contractor"] = contractor
        if description is not None:
            data["description"] = description
        if related_date is not None: # YYYY-MM-DD
            data["related_date"] = related_date
        if is_periodic is not None:
            data["is_periodic"] = is_periodic
        if period is not None:
            data["period"] = period
        if repetition_end_date is not None: # YYYY-MM-DD
            data["repetition_end_date"] = repetition_end_date
        if is_commitment is not None:
            data["is_commitment"] = is_commitment
        if is_planned is not None:
            data["is_planned"] = is_planned
        if is_splitted is not None:
            data["is_splitted"] = is_splitted
        if parts is not None: # JSON string
            data["parts"] = parts
        if periodic_edit_type is not None: # 'this' or 'this-and-following'
            data["periodic_edit_type"] = periodic_edit_type
        if tags is not None: # comma-separated string of IDs
            data["tags"] = tags
            
        response_data = self.client.post(f"transaction/{transaction_id}", data=data)
        op_data = response_data.get("transaction") if response_data else None
        return Operation(op_data) if op_data else None

    def delete(self, transaction_id, periodic_edit_type=None):
        """
        Deletes an operation (transaction).
        Corresponds to Adesk API v1 endpoint: `POST transaction/<transaction_id>/remove`.

        Args:
            transaction_id (int): ID of the transaction to delete. (Required)
            periodic_edit_type (str, optional): For periodic transactions, "this" or 
                                                "this-and-following".
                                                Note: This parameter is typically a query parameter
                                                in Adesk API, but client.post sends it in the body
                                                if provided. Behavior may vary based on API version/setup.

        Returns:
            dict: The response from the API, typically confirming success or failure.
        """
        if not transaction_id:
            raise ValueError("Required parameter missing: transaction_id.")
        
        data = {}
        # Based on the task description, periodic_edit_type is not part of the POST body for delete.
        # If it were a query parameter, client.post would need modification or a different approach.
        # For now, following the prompt's decision to omit it from the body.
        # However, if the API expects it in body for this specific call, it can be added here.
        # Example if it were a body parameter:
        # if periodic_edit_type is not None:
        #    data["periodic_edit_type"] = periodic_edit_type

        return self.client.post(f"transaction/{transaction_id}/remove", data=data)

    def complete(self, transaction_id):
        """
        Marks a planned operation (transaction) as completed.
        Corresponds to Adesk API v1 endpoint: `POST transaction/<transaction_id>/complete`.

        Args:
            transaction_id (int): ID of the planned transaction to complete. (Required)

        Returns:
            dict: The response from the API, typically confirming success or failure.
        """
        if not transaction_id:
            raise ValueError("Required parameter missing: transaction_id.")
        return self.client.post(f"transaction/{transaction_id}/complete")

    def get(self, transaction_id):
        """
        Retrieves a specific operation (transaction) by its ID.
        Corresponds to Adesk API v1 endpoint: `GET transaction/<transaction_id>`.

        Args:
            transaction_id (int): ID of the transaction to retrieve. (Required)

        Returns:
            Operation | None: The Operation model instance, or None if not found.
        """
        if not transaction_id:
            raise ValueError("Required parameter missing: transaction_id.")
        response_data = self.client.get(f"transaction/{transaction_id}")
        op_data = response_data.get("transaction") if response_data else None
        return Operation(op_data) if op_data else None

    def list_all(self, range_str=None, range_start=None, range_end=None, type=None, category=None, 
                 bank_account=None, legal_entity=None, contractor=None, contractor_inn=None, 
                 project=None, business_unit=None, status=None, owner_transfer=None, 
                 taxes=None, date_type=None, start=None, length=None):
        """
        Retrieves a list of operations (transactions) based on specified filters.
        Corresponds to Adesk API v1 endpoint: `GET transactions`.

        Args:
            range_str (str, optional): Predefined date range (e.g., "this_month").
            range_start (str, optional): Start date for custom range (YYYY-MM-DD).
            range_end (str, optional): End date for custom range (YYYY-MM-DD).
            type (str, optional): Filter by type ("income" or "outcome").
            category (int, optional): Filter by category ID.
            bank_account (int, optional): Filter by bank account ID.
            legal_entity (int, optional): Filter by legal entity ID.
            contractor (int, optional): Filter by contractor ID.
            contractor_inn (str, optional): Filter by contractor's INN.
            project (int, optional): Filter by project ID.
            business_unit (int, optional): Filter by business unit ID.
            status (str, optional): Filter by status (e.g., "planned", "completed").
            owner_transfer (bool, optional): Filter by owner transfer status.
            taxes (bool, optional): Filter by tax-related status.
            date_type (str, optional): Type of date to use for filtering ("operation" or "related").
            start (int, optional): For pagination, the starting record number.
            length (int, optional): For pagination, the number of records to retrieve.

        Returns:
            list[Operation]: A list of Operation model instances.
                             Returns an empty list if no operations are found or in case of an error.
        """
        params = {}
        if range_str is not None:
            params["range_str"] = range_str
        if range_start is not None: # YYYY-MM-DD
            params["range_start"] = range_start
        if range_end is not None: # YYYY-MM-DD
            params["range_end"] = range_end
        if type is not None:
            params["type"] = type
        if category is not None:
            params["category"] = category
        if bank_account is not None:
            params["bank_account"] = bank_account
        if legal_entity is not None:
            params["legal_entity"] = legal_entity
        if contractor is not None:
            params["contractor"] = contractor
        if contractor_inn is not None:
            params["contractor_inn"] = contractor_inn
        if project is not None:
            params["project"] = project
        if business_unit is not None:
            params["business_unit"] = business_unit
        if status is not None:
            params["status"] = status
        if owner_transfer is not None:
            params["owner_transfer"] = owner_transfer
        if taxes is not None:
            params["taxes"] = taxes
        if date_type is not None:
            params["date_type"] = date_type
        if start is not None:
            params["start"] = start
        if length is not None:
            params["length"] = length
            
        response_data = self.client.get("transactions", params=params)
        operations_data = response_data.get("transactions", []) if response_data else []
        return Operation.from_list(operations_data)
