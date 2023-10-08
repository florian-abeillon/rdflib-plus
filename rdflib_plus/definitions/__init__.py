"""Import RDF Property and RDFS Class definitions"""

from rdflib_plus.definitions.classes import (
    RDFS_CLASSES,
    parse_class_definition_file,
)
from rdflib_plus.definitions.properties import (
    RDF_PROPERTIES,
    parse_property_definition_file,
)

__all__ = [
    "RDF_PROPERTIES",
    "RDFS_CLASSES",
    "parse_class_definition_file",
    "parse_property_definition_file",
]
