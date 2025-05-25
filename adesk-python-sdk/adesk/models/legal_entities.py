# adesk/models/legal_entities.py
from .base_model import BaseModel

class VatRate(BaseModel):
    """Represents a VAT rate associated with a LegalEntity."""
    def __init__(self, data):
        """
        Initializes a VatRate object from API response data.

        Args:
            data (dict | None): The dictionary of VAT rate data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.active_since = data.get('activeSince') # Consider datetime
        self.active_until = data.get('activeUntil') # Consider datetime
        self.rate = data.get('rate')
        if self.rate is not None:
            try: self.rate = float(self.rate)
            except (ValueError, TypeError): self.rate = None

class LegalEntity(BaseModel):
    """Represents a legal entity from the Adesk API."""
    def __init__(self, data):
        """
        Initializes a LegalEntity object from API response data.

        Args:
            data (dict | None): The dictionary of legal entity data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.name = data.get('name')
        self.full_name = data.get('fullName')
        self.inn = data.get('inn')
        self.kpp = data.get('kpp')
        self.address = data.get('address')
        self.phone_number = data.get('phoneNumber')
        self.registration_number = data.get('registrationNumber')
        self.vat_rates = VatRate.from_list(data.get('vat_rates'))
        # Note: 'vat_rates' is a list of VatRate objects.
