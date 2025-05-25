class Transfers:
    """
    Provides methods for interacting with Adesk transfers (API v1).
    Accessed via `client.transfers`.
    """
    def __init__(self, client):
        """
        Initializes the Transfers resource.

        Args:
            client (AdeskClient): The AdeskClient instance to use for API calls.
        """
        self.client = client

    def create(self, amount, from_bank_account, to_bank_account, transaction_id=None, amount_to=None, date=None, description=None, tags=None):
        """
        Creates a new transfer between bank accounts.
        Corresponds to Adesk API v1 endpoint: `POST transfer`.

        Args:
            amount (float): The amount of the transfer. (Required)
            from_bank_account (int): ID of the source bank account. (Required)
            to_bank_account (int): ID of the destination bank account. (Required)
            transaction_id (int, optional): ID of an existing transaction to link.
            amount_to (float, optional): The amount received in the destination account,
                                         if different due to currency conversion or fees.
            date (str, optional): Date of the transfer (YYYY-MM-DD). Defaults to current date if not set.
            description (str, optional): Description of the transfer.
            tags (str, optional): Comma-separated string of tag IDs to associate with the transfer.

        Returns:
            dict: The created transfer object.
                  Returns None if the operation was unsuccessful or the response is empty.
        """
        if amount is None or from_bank_account is None or to_bank_account is None:
            raise ValueError("Required parameters missing: amount, from_bank_account, to_bank_account.")

        data = {
            "amount": amount,
            "from_bank_account": from_bank_account,
            "to_bank_account": to_bank_account,
        }
        if transaction_id is not None:
            data["transaction_id"] = transaction_id
        if amount_to is not None:
            data["amount_to"] = amount_to
        if date is not None: # YYYY-MM-DD
            data["date"] = date
        if description is not None:
            data["description"] = description
        if tags is not None: # comma-separated string of IDs
            data["tags"] = tags
            
        response = self.client.post("transfer", data=data)
        return response.get("transfer") if response else None

    def split(self, transfers_ids):
        """
        Splits a transfer. This operation is typically used when a single bank
        statement entry corresponds to multiple logical transfers.
        Corresponds to Adesk API v1 endpoint: `POST transfer/split`.

        Args:
            transfers_ids (str): Comma-separated string of transfer IDs to split. (Required)

        Returns:
            dict: The response from the API, typically confirming success or failure.
                  A successful operation might return `{"success": true}`.
        """
        if not transfers_ids:
            raise ValueError("Required parameter missing: transfers_ids.")

        data = {"transfers_ids": transfers_ids} # comma-separated string of IDs
        
        response = self.client.post("transfer/split", data=data)
        return response # Returns full response, often {"success": true} or similar
