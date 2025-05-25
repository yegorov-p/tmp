from adesk_python_sdk.adesk.models import BankAccount

class BankAccounts:
    """
    Provides methods for interacting with Adesk bank accounts (API v1).
    Accessed via `client.bank_accounts`.
    """
    def __init__(self, client):
        """
        Initializes the BankAccounts resource.

        Args:
            client (AdeskClient): The AdeskClient instance to use for API calls.
        """
        self.client = client

    def create(self, name, currency, legal_entity, number=None, bank_name=None, initial_amount=None, 
               initial_amount_date=None, type=None, bank_code=None, correspondent_account=None, 
               is_acquiring_enabled=None, commission_category=None, refund_category=None, category=None):
        """
        Creates a new bank account or cash account.
        Corresponds to Adesk API v1 endpoint: `POST bank-account`.

        Args:
            name (str): The name of the bank account. (Required)
            currency (str): Currency code (e.g., "RUB", "USD"). (Required)
            legal_entity (int): ID of the associated legal entity. (Required)
            number (str, optional): Account number.
            bank_name (str, optional): Name of the bank.
            initial_amount (float, optional): Initial balance of the account.
            initial_amount_date (str, optional): Date of the initial balance (YYYY-MM-DD).
            type (int, optional): Type of account (1 for cash, 2 for bank).
            bank_code (str, optional): Bank identification code (BIC).
            correspondent_account (str, optional): Correspondent account number.
            is_acquiring_enabled (bool, optional): Whether acquiring is enabled for this account.
            commission_category (int, optional): Category ID for acquiring commission.
            refund_category (int, optional): Category ID for acquiring refunds.
            category (int, optional): Category ID for cash accounts.

        Returns:
            BankAccount | None: The created BankAccount model instance, or None if creation failed.
        """
        if not all([name, currency, legal_entity is not None]): # legal_entity can be 0
            raise ValueError("Required parameters missing: name, currency, legal_entity.")
        
        data = {
            "name": name,
            "currency": currency,
            "legal_entity": legal_entity,
        }
        if number is not None:
            data["number"] = number
        if bank_name is not None:
            data["bank_name"] = bank_name
        if initial_amount is not None:
            data["initial_amount"] = initial_amount
        if initial_amount_date is not None:
            data["initial_amount_date"] = initial_amount_date # YYYY-MM-DD
        if type is not None:
            data["type"] = type # 1 for cash, 2 for bank
        if bank_code is not None:
            data["bank_code"] = bank_code
        if correspondent_account is not None:
            data["correspondent_account"] = correspondent_account
        if is_acquiring_enabled is not None:
            data["is_acquiring_enabled"] = is_acquiring_enabled
        if commission_category is not None:
            data["commission_category"] = commission_category
        if refund_category is not None:
            data["refund_category"] = refund_category
        if category is not None:
            data["category"] = category # For cash accounts
            
        response = self.client.post("bank-account", data=data)
        account_data = response.get("bankAccount") if response else None
        return BankAccount(account_data) if account_data else None

    def update(self, bank_account_id, name, number=None, bank_name=None, bank_code=None, 
               initial_amount=None, initial_amount_date=None, legal_entity=None, type=None, 
               correspondent_account=None, is_acquiring_enabled=None, commission_category=None, 
               refund_category=None, category=None):
        """
        Updates an existing bank account.
        Corresponds to Adesk API v1 endpoint: `POST bank-account/<bank_account_id>`.

        Args:
            bank_account_id (int): The ID of the bank account to update. (Required)
            name (str): New name for the bank account. (Required)
            number (str, optional): New account number.
            bank_name (str, optional): New bank name.
            bank_code (str, optional): New bank code (BIC).
            initial_amount (float, optional): New initial balance.
            initial_amount_date (str, optional): New date for initial balance (YYYY-MM-DD).
            legal_entity (int, optional): New legal entity ID.
            type (int, optional): New account type (1 for cash, 2 for bank).
            correspondent_account (str, optional): New correspondent account number.
            is_acquiring_enabled (bool, optional): Update acquiring status.
            commission_category (int, optional): New commission category ID.
            refund_category (int, optional): New refund category ID.
            category (int, optional): New category ID for cash accounts.

        Returns:
            dict: The response from the API, typically confirming success (e.g., `{"success": true}`).
        """
        if not bank_account_id or not name:
            raise ValueError("Required parameters missing: bank_account_id, name.")

        data = {"name": name}
        if number is not None:
            data["number"] = number
        if bank_name is not None:
            data["bank_name"] = bank_name
        if bank_code is not None:
            data["bank_code"] = bank_code
        if initial_amount is not None:
            data["initial_amount"] = initial_amount
        if initial_amount_date is not None:
            data["initial_amount_date"] = initial_amount_date # YYYY-MM-DD
        if legal_entity is not None:
            data["legal_entity"] = legal_entity
        if type is not None:
            data["type"] = type # 1 for cash, 2 for bank
        if correspondent_account is not None:
            data["correspondent_account"] = correspondent_account
        if is_acquiring_enabled is not None:
            data["is_acquiring_enabled"] = is_acquiring_enabled
        if commission_category is not None:
            data["commission_category"] = commission_category
        if refund_category is not None:
            data["refund_category"] = refund_category
        if category is not None:
            data["category"] = category # For cash accounts

        # API returns just {"success": true}
        return self.client.post(f"bank-account/{bank_account_id}", data=data)

    def delete(self, bank_account_id):
        """
        Deletes a bank account.
        Corresponds to Adesk API v1 endpoint: `POST bank-account/<bank_account_id>/remove`.

        Args:
            bank_account_id (int): The ID of the bank account to delete. (Required)

        Returns:
            dict: The response from the API, typically confirming success or failure.
        """
        if not bank_account_id:
            raise ValueError("Required parameter missing: bank_account_id.")
        return self.client.post(f"bank-account/{bank_account_id}/remove")

    def get(self, bank_account_id):
        """
        Retrieves a specific bank account by its ID.
        Corresponds to Adesk API v1 endpoint: `GET bank-account/<bank_account_id>`.

        Args:
            bank_account_id (int): The ID of the bank account to retrieve. (Required)

        Returns:
            BankAccount | None: The BankAccount model instance, or None if not found.
        """
        if not bank_account_id:
            raise ValueError("Required parameter missing: bank_account_id.")
        response = self.client.get(f"bank-account/{bank_account_id}")
        account_data = response.get("bankAccount") if response else None
        return BankAccount(account_data) if account_data else None

    def list_all(self, start=None, length=None, reduced=None, with_sum_amount=None, 
                 bank_account_type=None, status=None):
        """
        Retrieves a list of bank accounts.
        Corresponds to Adesk API v1 endpoint: `GET bank-accounts`.

        Args:
            start (int, optional): For pagination, the starting record number.
            length (int, optional): For pagination, the number of records to retrieve.
            reduced (bool, optional): If True, returns a reduced set of fields.
            with_sum_amount (bool, optional): If True, includes sum amounts in the response.
            bank_account_type (str, optional): Filter by account type ("Bank" or "Cash").
            status (str, optional): Filter by account status ("open" or "closed").

        Returns:
            list[BankAccount]: A list of BankAccount model instances.
                               Returns an empty list if no accounts are found or in case of an error.
        """
        params = {}
        if start is not None:
            params["start"] = start
        if length is not None:
            params["length"] = length
        if reduced is not None:
            params["reduced"] = reduced
        if with_sum_amount is not None:
            params["with_sum_amount"] = with_sum_amount
        if bank_account_type is not None: # 'Bank' or 'Cash'
            params["bank_account_type"] = bank_account_type
        if status is not None: # 'open' or 'closed'
            params["status"] = status
            
        response = self.client.get("bank-accounts", params=params)
        accounts_data = response.get("bankAccounts", []) if response else []
        return BankAccount.from_list(accounts_data)
