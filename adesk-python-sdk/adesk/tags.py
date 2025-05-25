class Tags:
    """
    Provides methods for interacting with Adesk tags (API v1).
    Accessed via `client.tags`.
    """
    def __init__(self, client):
        """
        Initializes the Tags resource.

        Args:
            client (AdeskClient): The AdeskClient instance to use for API calls.
        """
        self.client = client

    def list_all(self, search=None):
        """
        Retrieves a list of all tags.
        Corresponds to Adesk API v1 endpoint: `GET tags`.

        Args:
            search (str, optional): A search string to filter tags by name.

        Returns:
            list[dict]: A list of tag objects.
                        Returns an empty list if no tags are found or in case of an error.
        """
        params = {}
        if search is not None:
            params["search"] = search
            
        response = self.client.get("tags", params=params)
        return response.get("tags") if response else []

    def get(self, tag_id):
        """
        Retrieves a specific tag by its ID.
        Corresponds to Adesk API v1 endpoint: `GET tag/<tag_id>`.

        Args:
            tag_id (int): The ID of the tag to retrieve. (Required)

        Returns:
            dict: The tag object.
                  Returns None if not found or in case of an error.
        """
        if not tag_id:
            raise ValueError("Required parameter missing: tag_id.")
        response = self.client.get(f"tag/{tag_id}")
        return response.get("tag") if response else None

    def create(self, name, color):
        """
        Creates a new tag.
        Corresponds to Adesk API v1 endpoint: `POST tag`.

        Args:
            name (str): The name of the tag. (Required)
            color (str): The color of the tag (e.g., "orange", "blue"). (Required)

        Returns:
            dict: The created tag object or a success confirmation from the API.
                  The Adesk API might return the full tag object or just a success message.
        """
        if not name or not color:
            raise ValueError("Required parameters missing: name, color.")
        
        data = {
            "name": name,
            "color": color, # e.g., 'orange'
        }
        # API doc shows only success and errors, but let's see if it returns a tag object
        response = self.client.post("tag", data=data)
        return response # Or response.get("tag") if it exists and is desired

    def update(self, tag_id, name=None, color=None):
        """
        Updates an existing tag.
        Corresponds to Adesk API v1 endpoint: `POST tag/<tag_id>`.

        Args:
            tag_id (int): The ID of the tag to update. (Required)
            name (str, optional): New name for the tag.
            color (str, optional): New color for the tag.
                                   At least one of `name` or `color` must be provided.

        Returns:
            dict: The response from the API, typically confirming success or failure.
                  The Adesk API might return the updated tag object or just a success message.
        """
        if not tag_id:
            raise ValueError("Required parameter missing: tag_id.")
        if name is None and color is None:
            raise ValueError("Required parameters missing for update: name or color.")

        data = {}
        if name is not None:
            data["name"] = name
        if color is not None:
            data["color"] = color
            
        # API doc shows only success and errors
        return self.client.post(f"tag/{tag_id}", data=data)

    def delete(self, tag_id):
        """
        Deletes a tag.
        Corresponds to Adesk API v1 endpoint: `POST tag/<tag_id>/remove`.

        Args:
            tag_id (int): The ID of the tag to delete. (Required)

        Returns:
            dict: The response from the API, typically confirming success or failure.
        """
        if not tag_id:
            raise ValueError("Required parameter missing: tag_id.")
        
        # API doc shows only success and errors
        return self.client.post(f"tag/{tag_id}/remove")
