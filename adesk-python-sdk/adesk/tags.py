from adesk_python_sdk.adesk.models import Tag

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
            list[Tag]: A list of Tag model instances.
                       Returns an empty list if no tags are found or in case of an error.
        """
        params = {}
        if search is not None:
            params["search"] = search
            
        response_data = self.client.get("tags", params=params)
        tags_list_data = response_data.get("tags", []) if response_data else []
        return Tag.from_list(tags_list_data)

    def get(self, tag_id):
        """
        Retrieves a specific tag by its ID.
        Corresponds to Adesk API v1 endpoint: `GET tag/<tag_id>`.

        Args:
            tag_id (int): The ID of the tag to retrieve. (Required)

        Returns:
            Tag | None: The Tag model instance, or None if not found.
        """
        if not tag_id:
            raise ValueError("Required parameter missing: tag_id.")
        response_data = self.client.get(f"tag/{tag_id}")
        tag_data = response_data.get("tag") if response_data else None
        return Tag(tag_data) if tag_data else None

    def create(self, name, color):
        """
        Creates a new tag.
        Corresponds to Adesk API v1 endpoint: `POST tag`.

        Args:
            name (str): The name of the tag. (Required)
            color (str): The color of the tag (e.g., "orange", "blue"). (Required)

        Returns:
            Tag | dict: The created Tag model instance if the API returns the tag object,
                        otherwise the raw API response (dict).
        """
        if not name or not color:
            raise ValueError("Required parameters missing: name, color.")
        
        data = {
            "name": name,
            "color": color, # e.g., 'orange'
        }
        response_data = self.client.post("tag", data=data)
        created_tag_data = response_data.get("tag") if response_data else None
        if created_tag_data:
            return Tag(created_tag_data)
        return response_data # Fallback for success messages or other structures

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
            Tag | dict: The updated Tag model instance if the API returns the tag object,
                        otherwise the raw API response (dict).
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
            
        response_data = self.client.post(f"tag/{tag_id}", data=data)
        updated_tag_data = response_data.get("tag") if response_data else None
        if updated_tag_data:
            return Tag(updated_tag_data)
        return response_data # Fallback for success messages

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
        
        return self.client.post(f"tag/{tag_id}/remove")
