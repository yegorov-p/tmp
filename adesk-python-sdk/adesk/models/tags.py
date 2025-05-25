# adesk/models/tags.py
from .base_model import BaseModel

class Tag(BaseModel):
    """Represents a tag from the Adesk API."""
    def __init__(self, data):
        """
        Initializes a Tag object from API response data.

        Args:
            data (dict | None): The dictionary of tag data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.name = data.get('name')
        self.color = data.get('color')
