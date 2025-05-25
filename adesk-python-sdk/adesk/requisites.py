class Requisites:
    def __init__(self, client):
        self.client = client

    def create(self, contractor_id, name, inn=None, kpp=None, bank_account_number=None, 
               bank_code=None, bank_name=None, address=None, correspondent_account=None):
        """
        Add requisites for a contractor.
        Endpoint: requisites
        Method: POST
        """
        if not contractor_id or not name:
            raise ValueError("Required parameters missing: contractor_id, name.")

        data = {
            "contractor_id": contractor_id,
            "name": name,
        }
        if inn is not None:
            data["inn"] = inn
        if kpp is not None:
            data["kpp"] = kpp
        if bank_account_number is not None:
            data["bank_account_number"] = bank_account_number
        if bank_code is not None:
            data["bank_code"] = bank_code
        if bank_name is not None:
            data["bank_name"] = bank_name
        if address is not None:
            data["address"] = address
        if correspondent_account is not None:
            data["correspondent_account"] = correspondent_account
            
        response = self.client.post("requisites", data=data)
        return response.get("requisites")

    def update(self, requisites_id, contractor_id, name, inn=None, kpp=None, 
               bank_account_number=None, bank_code=None, bank_name=None, 
               address=None, correspondent_account=None):
        """
        Change requisites.
        Endpoint: requisites/<requisites_id>
        Method: POST
        """
        if not requisites_id or not contractor_id or not name:
            raise ValueError("Required parameters missing: requisites_id, contractor_id, name.")

        data = {
            "contractor_id": contractor_id,
            "name": name,
        }
        if inn is not None:
            data["inn"] = inn
        if kpp is not None:
            data["kpp"] = kpp
        if bank_account_number is not None:
            data["bank_account_number"] = bank_account_number
        if bank_code is not None:
            data["bank_code"] = bank_code
        if bank_name is not None:
            data["bank_name"] = bank_name
        if address is not None:
            data["address"] = address
        if correspondent_account is not None:
            data["correspondent_account"] = correspondent_account
            
        response = self.client.post(f"requisites/{requisites_id}", data=data)
        return response.get("requisites")

    def delete(self, requisites_id):
        """
        Delete requisites.
        Endpoint: requisites/<requisites_id>/remove
        Method: POST
        """
        if not requisites_id:
            raise ValueError("Required parameter missing: requisites_id.")
        
        # API returns full response, e.g. {"success": true}
        return self.client.post(f"requisites/{requisites_id}/remove")
