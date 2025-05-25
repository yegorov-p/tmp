class Tags:
    def __init__(self, client):
        self.client = client

    def list_all(self, search=None):
        """
        Get list of tags.
        Endpoint: tags
        Method: GET
        """
        params = {}
        if search is not None:
            params["search"] = search
            
        response = self.client.get("tags", params=params)
        return response.get("tags")

    def get(self, tag_id):
        """
        Get a tag.
        Endpoint: tag/<tag_id>
        Method: GET
        """
        if not tag_id:
            raise ValueError("Required parameter missing: tag_id.")
        response = self.client.get(f"tag/{tag_id}")
        return response.get("tag")

    def create(self, name, color):
        """
        Add a tag.
        Endpoint: tag
        Method: POST
        """
        if not name or not color:
            raise ValueError("Required parameters missing: name, color.")
        
        data = {
            "name": name,
            "color": color, # e.g., 'orange'
        }
        # API doc shows only success and errors, but let's see if it returns a tag object
        response = self.client.post("tag", data=data)
        return response # Or response.get("tag") if it exists

    def update(self, tag_id, name=None, color=None):
        """
        Change a tag.
        Endpoint: tag/<tag_id>
        Method: POST
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
        Delete a tag.
        Endpoint: tag/<tag_id>/remove
        Method: POST
        """
        if not tag_id:
            raise ValueError("Required parameter missing: tag_id.")
        
        # API doc shows only success and errors
        return self.client.post(f"tag/{tag_id}/remove")
