class LegalEntities:
    """
    Provides methods for interacting with Adesk legal entities (API v1).
    Accessed via `client.legal_entities`.
    """
    def __init__(self, client):
        """
        Initializes the LegalEntities resource.

        Args:
            client (AdeskClient): The AdeskClient instance to use for API calls.
        """
        self.client = client

    def create(self, name, full_name=None, inn=None, kpp=None, address=None, phone_number=None, registration_number=None):
        """
        Creates a new legal entity.
        Corresponds to Adesk API v1 endpoint: `POST legal-entity`.

        Args:
            name (str): The short name of the legal entity. (Required)
            full_name (str, optional): The full name of the legal entity.
            inn (str, optional): Taxpayer Identification Number (INN).
            kpp (str, optional): Reason Code for Registration (KPP).
            address (str, optional): Legal address.
            phone_number (str, optional): Contact phone number.
            registration_number (str, optional): State registration number (e.g., OGRN).

        Returns:
            dict: The created legal entity object.
                  Returns None if the operation was unsuccessful or the response is empty.
        """
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
        return response.get("legalEntity") if response else None

    def update(self, legal_entity_id, name=None, full_name=None, inn=None, kpp=None, 
               address=None, phone_number=None, registration_number=None, vat_rates=None):
        """
        Updates an existing legal entity.
        Corresponds to Adesk API v1 endpoint: `POST legal-entity/<legal_entity_id>`.

        Args:
            legal_entity_id (int): The ID of the legal entity to update. (Required)
            name (str, optional): New short name for the legal entity.
            full_name (str, optional): New full name for the legal entity.
            inn (str, optional): New INN.
            kpp (str, optional): New KPP.
            address (str, optional): New legal address.
            phone_number (str, optional): New contact phone number.
            registration_number (str, optional): New state registration number.
            vat_rates (list[dict], optional): List of VAT rates.
                                              Example: `[{"name": "VAT 20%", "value": 20.0}]`.

        Returns:
            dict: The updated legal entity object.
                  Returns None if the operation was unsuccessful or the response is empty.
        """
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
        return response.get("legalEntity") if response else None

    def delete(self, legal_entity_id):
        """
        Deletes a legal entity.
        Corresponds to Adesk API v1 endpoint: `POST legal-entity/<legal_entity_id>/remove`.

        Args:
            legal_entity_id (int): The ID of the legal entity to delete. (Required)

        Returns:
            dict: The response from the API, typically confirming success or failure.
        """
        if not legal_entity_id:
            raise ValueError("Required parameter missing: legal_entity_id.")
        return self.client.post(f"legal-entity/{legal_entity_id}/remove")

    def get(self, legal_entity_id):
        """
        Retrieves a specific legal entity by its ID.
        Corresponds to Adesk API v1 endpoint: `GET legal-entity/<legal_entity_id>`.

        Args:
            legal_entity_id (int): The ID of the legal entity to retrieve. (Required)

        Returns:
            dict: The legal entity object.
                  Returns None if not found or in case of an error.
        """
        if not legal_entity_id:
            raise ValueError("Required parameter missing: legal_entity_id.")
        response = self.client.get(f"legal-entity/{legal_entity_id}")
        return response.get("legalEntity") if response else None

    def list_all(self):
        """
        Retrieves a list of all legal entities.
        Corresponds to Adesk API v1 endpoint: `GET legal-entities`.

        Returns:
            list[dict]: A list of legal entity objects.
                        Returns an empty list if no entities are found or in case of an error.
        """
        response = self.client.get("legal-entities")
        return response.get("legalEntities") if response else []
