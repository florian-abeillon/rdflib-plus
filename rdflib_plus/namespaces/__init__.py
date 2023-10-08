"""Import namespaces and useful functions"""

from rdflib_plus.namespaces.build import create_namespace
from rdflib_plus.namespaces.define import (
    DEFAULT_NAMESPACE,
    NAMESPACE_TO_PREFIX,
    PREFIX_TO_NAMESPACE,
    SHAPES_NAMESPACE,
)

__all__ = [
    "DEFAULT_NAMESPACE",
    "NAMESPACE_TO_PREFIX",
    "PREFIX_TO_NAMESPACE",
    "SHAPES_NAMESPACE",
    "create_namespace",
]
