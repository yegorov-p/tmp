# adesk/models/requisites.py
from .base_model import BaseModel

class Requisite(BaseModel):
    """Represents contractor requisites (bank details, etc.) from the Adesk API."""
    def __init__(self, data):
        """
        Initializes a Requisite object from API response data.

        Args:
            data (dict | None): The dictionary of requisite data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.name = data.get('name') # Name of legal entity of contractor
        self.inn = data.get('inn')
        self.kpp = data.get('kpp')
        self.correspondent_account = data.get('correspondentAccount')
        self.bank_name = data.get('bankName')
        self.bank_account_number = data.get('bankAccountNumber')
        self.bank_code = data.get('bankCode')
        self.address = data.get('address')
        self.phone_number = data.get('phoneNumber') # As per API docs for create/update
        self.email = data.get('email') # As per API docs for create/update
        self.website = data.get('website') # As per API docs for create/update
        # contractor_id is not typically part of the Requisite object itself,
        # as requisites are usually sub-resources of a contractor.
        # self.contractor_id = data.get('contractor_id')
        # Note: Some fields like phone_number, email, website might be part of the API response
        # when fetching requisites, or they might be more specific to the contractor itself.
        # The model reflects fields common in 'requisites' structures.
