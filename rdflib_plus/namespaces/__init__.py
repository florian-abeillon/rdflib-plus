"""Import namespaces and useful functions"""

from rdflib_plus.namespaces.namespaces import (
    DEFAULT_NAMESPACE,
    NAMESPACE_TO_PREFIX,
    PREFIX_TO_NAMESPACE,
    SHAPES_NAMESPACE,
)
from rdflib_plus.namespaces.utils import create_namespace

__all__ = [
    "DEFAULT_NAMESPACE",
    "NAMESPACE_TO_PREFIX",
    "PREFIX_TO_NAMESPACE",
    "SHAPES_NAMESPACE",
    "create_namespace",
]
