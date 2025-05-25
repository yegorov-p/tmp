class LegalEntities:
    def __init__(self, client):
        self.client = client

    def create(self, name, full_name=None, inn=None, kpp=None, address=None, phone_number=None, registration_number=None):
        if not name:
            raise ValueError("Required parameter missing: name.")
        
        data = {"name": name}
        if full_name is not None:
            data["full_name"] = full_name
        if inn is not None:
            data["inn"] = inn
        if kpp is not None:
            data["kpp"] = kpp
        if address is not None:
            data["address"] = address
        if phone_number is not None:
            data["phone_number"] = phone_number
        if registration_number is not None:
            data["registration_number"] = registration_number
            
        response = self.client.post("legal-entity", data=data)
        return response.get("legalEntity")

    def update(self, legal_entity_id, name=None, full_name=None, inn=None, kpp=None, 
               address=None, phone_number=None, registration_number=None, vat_rates=None):
        if not legal_entity_id:
            raise ValueError("Required parameter missing: legal_entity_id.")

        data = {}
        if name is not None:
            data["name"] = name
        if full_name is not None:
            data["full_name"] = full_name
        if inn is not None:
            data["inn"] = inn
        if kpp is not None:
            data["kpp"] = kpp
        if address is not None:
            data["address"] = address
        if phone_number is not None:
            data["phone_number"] = phone_number
        if registration_number is not None:
            data["registration_number"] = registration_number
        if vat_rates is not None: # Expects a list of dicts, e.g. [{"name": "VAT 20%", "value": 20.0}]
            data["vat_rates"] = vat_rates 
            
        response = self.client.post(f"legal-entity/{legal_entity_id}", data=data)
        return response.get("legalEntity")

    def delete(self, legal_entity_id):
        if not legal_entity_id:
            raise ValueError("Required parameter missing: legal_entity_id.")
        return self.client.post(f"legal-entity/{legal_entity_id}/remove")

    def get(self, legal_entity_id):
        if not legal_entity_id:
            raise ValueError("Required parameter missing: legal_entity_id.")
        response = self.client.get(f"legal-entity/{legal_entity_id}")
        return response.get("legalEntity")

    def list_all(self):
        response = self.client.get("legal-entities")
        return response.get("legalEntities")
