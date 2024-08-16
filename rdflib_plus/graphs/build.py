"""Custom Graph constructor"""

import importlib
from typing import Callable, Optional

from rdflib_plus.namespaces import DEFAULT_NAMESPACE

# Import all the models defined in rdflib_plus.models
module = importlib.import_module("rdflib_plus.models")
MODELS = [getattr(module, model) for model in module.__dict__["__all__"]]


def build_custom_graph(
    base: type,
    format_fast: str,
    format_readable: str,
    additional_methods: Optional[list[Callable]] = None,
) -> type:
    """Create a constructor for custom graphs.

    Args:
        base (type):
            Rdflib graph constructor to base custom constructor on.
        format_fast (str):
            File format to serialize graph in for faster saves/loads.
        format_readable (str):
            File format to serialize graph in a readable way.
        additional_methods (list[Callable] | None, optional):
            Additional methods to add to the custom graph constructor.
            Defaults to None.

    Returns:
        type: Custom graph constructor.
    """

    class Graph(base):
        """Custom Graph constructor"""

        # Initialize model names list
        _models: list[str] = []

        # Set formats to None (to be initialized in child classes)
        _format_fast: str = format_fast
        _format_readable: str = format_readable

        def __init__(
            self, identifier: str = DEFAULT_NAMESPACE, **kwargs
        ) -> None:
            """Initialize Graph object.

            Args:
                identifier (str, optional):
                    Graph identifier. Defaults to DEFAULT_NAMESPACE.
            """

            super().__init__(identifier=identifier, **kwargs)

        @classmethod
        def add_model(cls, model: type) -> None:
            """Add model constructor to Graph as attribute.

            Args:
                model (str):
                    Model constructor.
            """

            # Get model name
            model_name = model.__name__

            # Add it to Graph's models list
            cls._models.append(model_name)

            def model_constructor(self, *args, **kwargs):
                """Create model object."""

                return model(self, *args, **kwargs)

            # Define Graph's related method
            setattr(cls, model_name, model_constructor)

        @classmethod
        def add_models(cls, models: list[type]) -> None:
            """Add multiple model constructors to Graph as attributes.

            Args:
                model (list[str]):
                    List of model constructors.
            """

            # For every model
            for model in models:
                # Add its constructor to Graph
                cls.add_model(model)

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
                    Whether to save Graph in a format that is faster to parse
                    and serialize. Defaults to False.
                encoding (str | None, optional):
                    Encoding to use when serializing Graph. Defaults to None.
            """

            # Set format
            format_ = self._format_fast if fast else self._format_readable

            # Serialize Graph
            super().serialize(
                destination=path, format=format_, encoding=encoding
            )

    # Add all rdflib_plus models to the _Graph class
    Graph.add_models(MODELS)

    # If additional methods are specified
    if additional_methods is not None:
        # For every additional method
        for method in additional_methods:
            # Add it to the custom graph constructor
            setattr(Graph, method.__name__, method)

    return Graph
