"""Custom Graph constructor"""

import importlib
from typing import Optional

from rdflib import Graph as RdflibGraph

# Import all the models defined in rdflib_plus.models
module = importlib.import_module("rdflib_plus.models")
MODELS = [getattr(module, model) for model in module.__dict__["__all__"]]


class Graph(RdflibGraph):
    """Custom Graph constructor"""

    def __init__(self, **kwargs) -> None:
        """Initialize Graph."""

        super().__init__(**kwargs)

        # Initialize Graph's models list
        self._models = []

        # Add model constructors to Graph
        self.add_models(MODELS)

    def add_model(self, model: type) -> None:
        """Add model constructor to Graph as attribute.

        Args:
            model (str):
                Model constructor.
        """

        def model_constructor(*args, **kwargs):
            """Create model object."""

            return model(self, *args, **kwargs)

        # Get model name
        model_name = model.__name__

        # Add it to Graph's models list
        self._models.append(model_name)

        # Define Graph's related method
        setattr(self, model_name, model_constructor)

    def add_models(self, models: list[type]) -> None:
        """Add multiple model constructors to Graph as attributes.

        Args:
            model (list[str]):
                List of model constructors.
        """

        # For every model
        for model in models:
            # Add its constructor to Graph
            self.add_model(model)

    def load(self, path: str) -> "Graph":
        """Load Graph data.

        Args:
            path (str):
                Location of the Graph data to load.

        Returns:
            Graph: Loaded Graph.
        """

        return super().parse(source=path)

    def save(
        self, path: str, fast: bool = False, encoding: Optional[str] = None
    ) -> None:
        """Save Graph locally.

        Args:
            path (str):
                Path where to save Graph to.
            fast (bool, optional):
                Whether to save Graph in a format that is faster to parse and
                serialize. Defaults to False.
            encoding (Optional[str], optional):
                Encoding to use when serializing Graph. Defaults to None.
        """

        # Set format
        format_ = "ntriples" if fast else "turtle"

        # Serialize Graph
        super().serialize(destination=path, format=format_, encoding=encoding)
