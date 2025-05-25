from adesk_python_sdk.adesk.models import Requisite

class Requisites:
    """
    Provides methods for interacting with Adesk contractor requisites (bank details, etc.) (API v1).
    Accessed via `client.requisites`.
    """
    def __init__(self, client):
        """
        Initializes the Requisites resource.

        Args:
            client (AdeskClient): The AdeskClient instance to use for API calls.
        """
        self.client = client

    def create(self, contractor_id, name, inn=None, kpp=None, bank_account_number=None, 
               bank_code=None, bank_name=None, address=None, correspondent_account=None):
        """
        Adds new requisites for a specified contractor.
        Corresponds to Adesk API v1 endpoint: `POST requisites`.

        Args:
            contractor_id (int): The ID of the contractor to whom these requisites belong. (Required)
            name (str): A name for these requisites (e.g., "Primary Bank Account"). (Required)
            inn (str, optional): Taxpayer Identification Number (INN).
            kpp (str, optional): Reason Code for Registration (KPP).
            bank_account_number (str, optional): The bank account number.
            bank_code (str, optional): Bank identification code (BIC).
            bank_name (str, optional): Name of the bank.
            address (str, optional): Address associated with these requisites.
            correspondent_account (str, optional): Correspondent account number.

        Returns:
            Requisite | None: The created Requisite model instance, or None if creation failed.
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
            
        response_data = self.client.post("requisites", data=data)
        requisite_data = response_data.get("requisites") if response_data else None # API returns "requisites" (plural)
        return Requisite(requisite_data) if requisite_data else None

    def update(self, requisites_id, contractor_id, name, inn=None, kpp=None, 
               bank_account_number=None, bank_code=None, bank_name=None, 
               address=None, correspondent_account=None):
        """
        Updates existing requisites.
        Corresponds to Adesk API v1 endpoint: `POST requisites/<requisites_id>`.

        Args:
            requisites_id (int): The ID of the requisites to update. (Required)
            contractor_id (int): The ID of the contractor (must be provided, even if not changing). (Required)
            name (str): New name for these requisites. (Required)
            inn (str, optional): New INN.
            kpp (str, optional): New KPP.
            bank_account_number (str, optional): New bank account number.
            bank_code (str, optional): New bank code (BIC).
            bank_name (str, optional): New bank name.
            address (str, optional): New address.
            correspondent_account (str, optional): New correspondent account number.

        Returns:
            Requisite | None: The updated Requisite model instance, or None if update failed.
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
            
        response_data = self.client.post(f"requisites/{requisites_id}", data=data)
        requisite_data = response_data.get("requisites") if response_data else None # API returns "requisites" (plural)
        return Requisite(requisite_data) if requisite_data else None

    def delete(self, requisites_id):
        """
        Deletes specified requisites.
        Corresponds to Adesk API v1 endpoint: `POST requisites/<requisites_id>/remove`.

        Args:
            requisites_id (int): The ID of the requisites to delete. (Required)

        Returns:
            dict: The response from the API, typically confirming success or failure
                  (e.g., `{"success": true}`).
        """
        if not requisites_id:
            raise ValueError("Required parameter missing: requisites_id.")
        
        # API returns full response, e.g. {"success": true}
        return self.client.post(f"requisites/{requisites_id}/remove")
