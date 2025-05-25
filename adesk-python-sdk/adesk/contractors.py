class Contractors:
    def __init__(self, client):
        self.client = client

    def list_all(self, range_str=None, range_start=None, range_end=None, reduced=None, 
                 q=None, inn=None, checking_bank_account=None, with_balance=None):
        """
        Get list of contractors.
        Endpoint: contractors
        Method: GET
        """
        params = {}
        if range_str is not None:
            params["range_str"] = range_str
        if range_start is not None: # YYYY-MM-DD
            params["range_start"] = range_start
        if range_end is not None: # YYYY-MM-DD
            params["range_end"] = range_end
        if reduced is not None:
            params["reduced"] = reduced
        if q is not None:
            params["q"] = q
        if inn is not None:
            params["inn"] = inn
        if checking_bank_account is not None:
            params["checking_bank_account"] = checking_bank_account
        if with_balance is not None:
            params["with_balance"] = with_balance
            
        response = self.client.get("contractors", params=params)
        return response.get("contractors")

    def get(self, contractor_id):
        """
        Get a contractor.
        Endpoint: contractor/<contractor_id>
        Method: GET
        """
        if not contractor_id:
            raise ValueError("Required parameter missing: contractor_id.")
        response = self.client.get(f"contractor/{contractor_id}")
        return response.get("contractor")

    def get_commitments(self, contractor_id):
        """
        Get list of commitments for a contractor.
        Endpoint: contractor/<contractor_id>/commitments
        Method: GET
        """
        if not contractor_id:
            raise ValueError("Required parameter missing: contractor_id.")
        response = self.client.get(f"contractor/{contractor_id}/commitments")
        return response.get("commitments")

    def get_requisites(self, contractor_id):
        """
        Get list of requisites for a contractor.
        Endpoint: contractor/<contractor_id>/requisites
        Method: GET
        """
        if not contractor_id:
            raise ValueError("Required parameter missing: contractor_id.")
        response = self.client.get(f"contractor/{contractor_id}/requisites")
        return response.get("requisites")

    def create(self, name, contact_person=None, phone_number=None, email=None, description=None):
        """
        Add a contractor.
        Endpoint: contractor
        Method: POST
        """
        if not name:
            raise ValueError("Required parameter missing: name.")
        
        data = {"name": name}
        if contact_person is not None:
            data["contact_person"] = contact_person
        if phone_number is not None:
            data["phone_number"] = phone_number
        if email is not None:
            data["email"] = email
        if description is not None:
            data["description"] = description
            
        response = self.client.post("contractor", data=data)
        return response.get("contractor")

    def update(self, contractor_id, name=None, contact_person=None, phone_number=None, email=None, description=None):
        """
        Change a contractor.
        Endpoint: contractor/<contractor_id>
        Method: POST
        """
        if not contractor_id:
            raise ValueError("Required parameter missing: contractor_id.")

        data = {}
        if name is not None:
            data["name"] = name
        if contact_person is not None:
            data["contact_person"] = contact_person
        if phone_number is not None:
            data["phone_number"] = phone_number
        if email is not None:
            data["email"] = email
        if description is not None:
            data["description"] = description
            
        # API returns full response, e.g. {"success": true}
        return self.client.post(f"contractor/{contractor_id}", data=data)

    def delete(self, contractor_id):
        """
        Delete a contractor.
        Endpoint: contractor/<contractor_id>/remove
        Method: POST
        """
        if not contractor_id:
            raise ValueError("Required parameter missing: contractor_id.")
        return self.client.post(f"contractor/{contractor_id}/remove")

    def mass_delete(self, contractor_ids):
        """
        Mass delete contractors.
        Endpoint: contractors/remove
        Method: POST
        """
        if not contractor_ids: # Should be a comma-separated string of IDs
            raise ValueError("Required parameter missing: contractor_ids.")
        
        data = {"contractor_ids": contractor_ids}
        return self.client.post("contractors/remove", data=data)
