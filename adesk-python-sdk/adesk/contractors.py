from adesk_python_sdk.adesk.models import Contractor, Commitment, Requisite

class Contractors:
    """
    Provides methods for interacting with Adesk contractors (API v1).
    Accessed via `client.contractors`.
    """
    def __init__(self, client):
        """
        Initializes the Contractors resource.

        Args:
            client (AdeskClient): The AdeskClient instance to use for API calls.
        """
        self.client = client

    def list_all(self, range_str=None, range_start=None, range_end=None, reduced=None, 
                 q=None, inn=None, checking_bank_account=None, with_balance=None):
        """
        Retrieves a list of contractors based on specified filters.
        Corresponds to Adesk API v1 endpoint: `GET contractors`.

        Args:
            range_str (str, optional): Predefined date range (e.g., "this_month").
            range_start (str, optional): Start date for custom range (YYYY-MM-DD).
            range_end (str, optional): End date for custom range (YYYY-MM-DD).
            reduced (bool, optional): If True, returns a reduced set of fields for each contractor.
            q (str, optional): Search query string (searches by name, INN, etc.).
            inn (str, optional): Filter by Taxpayer Identification Number (INN).
            checking_bank_account (str, optional): Filter by checking bank account number.
            with_balance (bool, optional): If True, includes balance information for contractors.

        Returns:
            list[Contractor]: A list of Contractor model instances.
                              Returns an empty list if no contractors are found or in case of an error.
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
            
        response_data = self.client.get("contractors", params=params)
        contractors_list_data = response_data.get("contractors", []) if response_data else []
        return Contractor.from_list(contractors_list_data)

    def get(self, contractor_id):
        """
        Retrieves a specific contractor by their ID.
        Corresponds to Adesk API v1 endpoint: `GET contractor/<contractor_id>`.

        Args:
            contractor_id (int): The ID of the contractor to retrieve. (Required)

        Returns:
            Contractor | None: The Contractor model instance, or None if not found.
        """
        if not contractor_id:
            raise ValueError("Required parameter missing: contractor_id.")
        response_data = self.client.get(f"contractor/{contractor_id}")
        contractor_data = response_data.get("contractor") if response_data else None
        return Contractor(contractor_data) if contractor_data else None

    def get_commitments(self, contractor_id):
        """
        Retrieves a list of commitments associated with a specific contractor.
        Corresponds to Adesk API v1 endpoint: `GET contractor/<contractor_id>/commitments`.

        Args:
            contractor_id (int): The ID of the contractor. (Required)

        Returns:
            list[Commitment]: A list of Commitment model instances for the contractor.
                              Returns an empty list if none are found or in case of an error.
        """
        if not contractor_id:
            raise ValueError("Required parameter missing: contractor_id.")
        response_data = self.client.get(f"contractor/{contractor_id}/commitments")
        commitments_data = response_data.get("commitments", []) if response_data else []
        return Commitment.from_list(commitments_data)

    def get_requisites(self, contractor_id):
        """
        Retrieves a list of requisites (bank details, etc.) for a specific contractor.
        Corresponds to Adesk API v1 endpoint: `GET contractor/<contractor_id>/requisites`.

        Args:
            contractor_id (int): The ID of the contractor. (Required)

        Returns:
            list[Requisite]: A list of Requisite model instances for the contractor.
                             Returns an empty list if none are found or in case of an error.
        """
        if not contractor_id:
            raise ValueError("Required parameter missing: contractor_id.")
        response_data = self.client.get(f"contractor/{contractor_id}/requisites")
        requisites_data = response_data.get("requisites", []) if response_data else []
        return Requisite.from_list(requisites_data)

    def create(self, name, contact_person=None, phone_number=None, email=None, description=None):
        """
        Creates a new contractor.
        Corresponds to Adesk API v1 endpoint: `POST contractor`.

        Args:
            name (str): The name of the contractor. (Required)
            contact_person (str, optional): Name of the contact person.
            phone_number (str, optional): Contact phone number.
            email (str, optional): Contact email address.
            description (str, optional): Description or notes about the contractor.

        Returns:
            Contractor | None: The created Contractor model instance, or None if creation failed.
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
            
        response_data = self.client.post("contractor", data=data)
        contractor_data = response_data.get("contractor") if response_data else None
        return Contractor(contractor_data) if contractor_data else None

    def update(self, contractor_id, name=None, contact_person=None, phone_number=None, email=None, description=None):
        """
        Updates an existing contractor.
        Corresponds to Adesk API v1 endpoint: `POST contractor/<contractor_id>`.

        Args:
            contractor_id (int): The ID of the contractor to update. (Required)
            name (str, optional): New name for the contractor.
            contact_person (str, optional): New contact person name.
            phone_number (str, optional): New phone number.
            email (str, optional): New email address.
            description (str, optional): New description.

        Returns:
            dict: The response from the API, typically confirming success (e.g., `{"success": true}`).
                  The Adesk API might also return the updated contractor object in some cases.
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
        Deletes a contractor.
        Corresponds to Adesk API v1 endpoint: `POST contractor/<contractor_id>/remove`.

        Args:
            contractor_id (int): The ID of the contractor to delete. (Required)

        Returns:
            dict: The response from the API, typically confirming success or failure.
        """
        if not contractor_id:
            raise ValueError("Required parameter missing: contractor_id.")
        return self.client.post(f"contractor/{contractor_id}/remove")

    def mass_delete(self, contractor_ids):
        """
        Deletes multiple contractors in a single request.
        Corresponds to Adesk API v1 endpoint: `POST contractors/remove`.

        Args:
            contractor_ids (str): Comma-separated string of contractor IDs to delete. (Required)

        Returns:
            dict: The response from the API, typically confirming success or failure.
        """
        if not contractor_ids: # Should be a comma-separated string of IDs
            raise ValueError("Required parameter missing: contractor_ids.")
        
        data = {"contractor_ids": contractor_ids}
        return self.client.post("contractors/remove", data=data)
