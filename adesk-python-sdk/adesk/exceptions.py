class AdeskAPIError(Exception):
    """Base class for exceptions raised by the Adesk API client."""
    def __init__(self, message, status_code=None, response_data=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data

    def __str__(self):
        if self.status_code:
            return f"[{self.status_code}] {super().__str__()} - Response: {self.response_data}"
        return super().__str__()

class AdeskAuthError(AdeskAPIError):
    """Authentication failed (e.g., invalid API token). Status code 401."""
    pass

class AdeskRateLimitError(AdeskAPIError):
    """API rate limit exceeded. Status code 429."""
    pass

class AdeskPaymentRequiredError(AdeskAPIError):
    """Payment required for API access. Custom Adesk code 21, or HTTP 402/403."""
    pass

class AdeskBadRequestError(AdeskAPIError):
    """Invalid request (e.g., missing required parameters, validation error). Status code 400."""
    pass

class AdeskNotFoundError(AdeskAPIError):
    """Resource not found. Status code 404."""
    pass

class AdeskServerError(AdeskAPIError):
    """Adesk server-side error. Status codes 5xx."""
    pass
