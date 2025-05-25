class Transfers:
    def __init__(self, client):
        self.client = client

    def create(self, amount, from_bank_account, to_bank_account, transaction_id=None, amount_to=None, date=None, description=None, tags=None):
        """
        Add a transfer.
        Endpoint: transfer
        Method: POST
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
        return response.get("transfer")

    def split(self, transfers_ids):
        """
        Split a transfer.
        Endpoint: transfer/split
        Method: POST
        """
        if not transfers_ids:
            raise ValueError("Required parameter missing: transfers_ids.")

        data = {"transfers_ids": transfers_ids} # comma-separated string of IDs
        
        response = self.client.post("transfer/split", data=data)
        return response # Returns full response, often {"success": true} or similar
