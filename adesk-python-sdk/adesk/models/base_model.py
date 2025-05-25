# adesk/models/base_model.py
class BaseModel:
    """
    Base class for all Adesk API data models.
    Provides common functionality for initializing from API response data
    and a basic representation.
    """
    def __init__(self, data):
        """
        Initializes a BaseModel instance.

        Subclasses are expected to call this and then populate their specific
        attributes from the `data` dictionary, typically using `data.get()`.

        Args:
            data (dict | None): The dictionary of data from the API response.
                                If None, an empty dictionary is used.
        """
        if data is None:
            data = {} # Ensure data is always a dict
        self._data = data # Store raw data if needed for unprocessed fields
        self._load_attributes(data)

    def _load_attributes(self, data):
        """
        Placeholder method for loading attributes from data.
        Subclasses should override this or directly assign attributes in their __init__.
        This specific implementation does nothing.

        Args:
            data (dict): The dictionary of data from the API response.
        """
        # This method will be overridden by subclasses
        # or a more generic mechanism can be implemented later if preferred.
        # For now, subclasses will explicitly set attributes in their __init__ after super().__init__
        pass

    def __repr__(self):
        """
        Provides a string representation of the model instance,
        showing its class name and public attributes.
        """
        attributes = ', '.join(f"{k}={v!r}" for k, v in self.__dict__.items() if not k.startswith('_'))
        return f"<{self.__class__.__name__}({attributes})>"

    @classmethod
    def from_list(cls, data_list):
        """
        Creates a list of model instances from a list of data dictionaries.

        Args:
            data_list (list[dict] | None): A list of dictionaries from the API response.

        Returns:
            list[BaseModel]: A list of model instances of the calling class.
                             Returns an empty list if `data_list` is None or empty.
        """
        if data_list is None:
            return []
        return [cls(item) for item in data_list]
