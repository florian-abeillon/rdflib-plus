"""Import namespaces and useful functions"""

from rdflib_plus.namespaces.build import create_namespace
from rdflib_plus.namespaces.define import (
    DEFAULT_NAMESPACE,
    NAMESPACE_TO_PREFIX,
    PREFIX_TO_NAMESPACE,
    SHAPES_NAMESPACE,
)
from rdflib_plus.namespaces.parse import parse_prefixed_iri, stringify_iri

__all__ = [
    "create_namespace",
    "parse_prefixed_iri",
    "stringify_iri",
    "DEFAULT_NAMESPACE",
    "NAMESPACE_TO_PREFIX",
    "PREFIX_TO_NAMESPACE",
    "SHAPES_NAMESPACE",
]
