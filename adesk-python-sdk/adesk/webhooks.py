from adesk_python_sdk.adesk.models import Webhook

class Webhooks:
    """
    Provides methods for interacting with Adesk webhooks (API v1).
    Accessed via `client.webhooks`.
    """
    def __init__(self, client):
        """
        Initializes the Webhooks resource.

        Args:
            client (AdeskClient): The AdeskClient instance to use for API calls.
        """
        self.client = client

    def list_all(self):
        """
        Retrieves a list of all configured webhooks.
        Corresponds to Adesk API v1 endpoint: `GET webhooks`.

        Returns:
            list[Webhook]: A list of Webhook model instances.
                           Returns an empty list if no webhooks are found or in case of an error.
        """
        response_data = self.client.get("webhooks")
        webhooks_list_data = response_data.get("webhooks", []) if response_data else []
        return Webhook.from_list(webhooks_list_data)

    def create(self, url, events, description=None):
        """
        Creates a new webhook.
        Corresponds to Adesk API v1 endpoint: `POST webhook`.

        Args:
            url (str): The URL to which webhook notifications will be sent. (Required)
            events (list[str]): A list of event types for which to trigger the webhook
                                (e.g., ["transaction_created", "project_updated"]). (Required)
                                The Adesk API expects this as 'events[]'.
            description (str, optional): A description for the webhook.

        Returns:
            Webhook | None: The created Webhook model instance, or None if creation failed.
        """
        if not url or not events:
            raise ValueError("Required parameters missing: url, events.")

        data = {
            "url": url,
            "events": events,  # Pass list directly, requests lib should handle events[]=...
        }
        if description is not None:
            data["description"] = description
            
        response_data = self.client.post("webhook", data=data)
        webhook_data = response_data.get("webhook") if response_data else None
        return Webhook(webhook_data) if webhook_data else None

    def update(self, webhook_id, url, events, description=None):
        """
        Updates an existing webhook.
        Corresponds to Adesk API v1 endpoint: `POST webhook/<webhook_id>`.

        Args:
            webhook_id (int): The ID of the webhook to update. (Required)
            url (str): The new URL for the webhook. (Required)
            events (list[str]): The new list of event types. (Required)
            description (str, optional): The new description for the webhook.

        Returns:
            Webhook | None: The updated Webhook model instance, or None if update failed.
        """
        if not webhook_id or not url or not events:
            raise ValueError("Required parameters missing: webhook_id, url, events.")

        data = {
            "url": url,
            "events": events,  # Pass list directly
        }
        if description is not None:
            data["description"] = description
            
        response_data = self.client.post(f"webhook/{webhook_id}", data=data)
        webhook_data = response_data.get("webhook") if response_data else None
        return Webhook(webhook_data) if webhook_data else None

    def delete(self, webhook_id):
        """
        Deletes a webhook.
        Corresponds to Adesk API v1 endpoint: `POST webhook/<webhook_id>/remove`.

        Args:
            webhook_id (int): The ID of the webhook to delete. (Required)

        Returns:
            dict: The response from the API, typically confirming success or failure.
        """
        if not webhook_id:
            raise ValueError("Required parameter missing: webhook_id.")
        
        # This endpoint typically doesn't require a body, token is handled by client.post
        return self.client.post(f"webhook/{webhook_id}/remove")
