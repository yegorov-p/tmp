class BankAccounts:
    def __init__(self, client):
        self.client = client

    def create(self, name, currency, legal_entity, number=None, bank_name=None, initial_amount=None, 
               initial_amount_date=None, type=None, bank_code=None, correspondent_account=None, 
               is_acquiring_enabled=None, commission_category=None, refund_category=None, category=None):
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
        return response.get("bankAccount")

    def update(self, bank_account_id, name, number=None, bank_name=None, bank_code=None, 
               initial_amount=None, initial_amount_date=None, legal_entity=None, type=None, 
               correspondent_account=None, is_acquiring_enabled=None, commission_category=None, 
               refund_category=None, category=None):
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
        if not bank_account_id:
            raise ValueError("Required parameter missing: bank_account_id.")
        return self.client.post(f"bank-account/{bank_account_id}/remove")

    def get(self, bank_account_id):
        if not bank_account_id:
            raise ValueError("Required parameter missing: bank_account_id.")
        response = self.client.get(f"bank-account/{bank_account_id}")
        return response.get("bankAccount")

    def list_all(self, start=None, length=None, reduced=None, with_sum_amount=None, 
                 bank_account_type=None, status=None):
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
        return response.get("bankAccounts")
