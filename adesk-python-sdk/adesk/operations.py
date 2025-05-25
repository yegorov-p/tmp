class Operations:
    def __init__(self, client):
        self.client = client

    def create(self, date, type, amount, bank_account, apply_import_rules=None, category=None, 
               project=None, business_unit=None, contractor=None, description=None, 
               related_date=None, is_periodic=None, period=None, repetition_end_date=None, 
               is_commitment=None, is_planned=None, is_splitted=None, parts=None, tags=None):
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
            
        response = self.client.post("transaction", data=data)
        return response.get("transaction")

    def update(self, transaction_id, date, bank_account, amount, category=None, project=None, 
               business_unit=None, contractor=None, description=None, related_date=None, 
               is_periodic=None, period=None, repetition_end_date=None, is_commitment=None, 
               is_planned=None, is_splitted=None, parts=None, periodic_edit_type=None, tags=None):
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
            
        response = self.client.post(f"transaction/{transaction_id}", data=data)
        return response.get("transaction")

    def delete(self, transaction_id, periodic_edit_type=None):
        if not transaction_id:
            raise ValueError("Required parameter missing: transaction_id.")
        
        data = {}
        # Based on the task description, periodic_edit_type is not part of the POST body for delete.
        # If it were a query parameter, client.post would need modification or a different approach.
        # For now, following the prompt's decision to omit it from the body.
        if periodic_edit_type is not None:
             # If it's a query param, it should be passed to client.post differently.
             # self.client.post(f"transaction/{transaction_id}/remove", params={"periodic_edit_type": periodic_edit_type})
             # However, the current client.post only supports 'data' for body and 'params' for GET.
             # For now, assuming it's not used or is handled by a different mechanism if it's a query param for POST.
             pass

        return self.client.post(f"transaction/{transaction_id}/remove", data=data)

    def complete(self, transaction_id):
        if not transaction_id:
            raise ValueError("Required parameter missing: transaction_id.")
        return self.client.post(f"transaction/{transaction_id}/complete")

    def get(self, transaction_id):
        if not transaction_id:
            raise ValueError("Required parameter missing: transaction_id.")
        response = self.client.get(f"transaction/{transaction_id}")
        return response.get("transaction")

    def list_all(self, range_str=None, range_start=None, range_end=None, type=None, category=None, 
                 bank_account=None, legal_entity=None, contractor=None, contractor_inn=None, 
                 project=None, business_unit=None, status=None, owner_transfer=None, 
                 taxes=None, date_type=None, start=None, length=None):
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
            
        response = self.client.get("transactions", params=params)
        return response.get("transactions")
