import requests
from typing import Optional, Dict, Any, List

class TeaScout:
    def __init__(self, url: str, key: Optional[str] = None):
        """
        Initialize the TeaScout client.
        
        Args:
            url (str): The base URL of the TeaScout server (e.g., "http://localhost:5000").
            key (str, optional): API Key if required by the server.
        """
        self.base_url = url.rstrip('/')
        self.api_key = key
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({'Authorization': f'Bearer {self.api_key}'})

    def list_models(self) -> Dict[str, str]:
        """
        List available models from the server.
        
        Returns:
            dict: A dictionary of model names and their descriptions.
        """
        try:
            response = self.session.get(f"{self.base_url}/models")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to fetch models: {e}")

    def model(self, model_name: str) -> 'ModelContext':
        """
        Select a model to work with.
        
        Args:
            model_name (str): The ID of the model to use.
            
        Returns:
            ModelContext: A context object for building the request.
        """
        return ModelContext(self, model_name)

class ModelContext:
    def __init__(self, client: TeaScout, model_name: str):
        self.client = client
        self.model_name = model_name
        self._text_content = None

    def text(self, content: str) -> 'ModelContext':
        """
        Set the text content for inference.
        
        Args:
            content (str): The text to analyze.
            
        Returns:
            ModelContext: Returns self for chaining.
        """
        self._text_content = content
        return self

    def inference(self) -> Dict[str, Any]:
        """
        Execute the inference request.
        
        Returns:
            dict: The inference result from the server.
            
        Raises:
            ValueError: If text content is not set.
            ConnectionError: If the request fails.
        """
        if self._text_content is None:
            raise ValueError("Text content must be set using .text() before calling .inference()")
        
        url = f"{self.client.base_url}/inference/{self.model_name}"
        payload = {"text": self._text_content}
        
        try:
            response = self.client.session.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"Inference request failed: {e}")
