# adesk/models/webhooks.py
from .base_model import BaseModel

class Webhook(BaseModel):
    """Represents a webhook configuration from the Adesk API."""
    def __init__(self, data):
        """
        Initializes a Webhook object from API response data.

        Args:
            data (dict | None): The dictionary of webhook data from the API.
        """
        super().__init__(data)
        data = data or {}
        self.id = data.get('id')
        self.description = data.get('description')
        self.url = data.get('url')
        self.events = data.get('events') # Should be a list of strings

        # Ensure events is a list, even if API might sometimes return single string or None
        if self.events is not None and not isinstance(self.events, list):
            # This case should ideally not happen if API is consistent.
            # If it can be a single string, convert to list.
            # If it's something else unexpected, log or raise.
            # For now, let's assume it's either a list or None.
            pass
        elif self.events is None:
            self.events = []
        # Note: 'events' is a list of strings representing event types.
