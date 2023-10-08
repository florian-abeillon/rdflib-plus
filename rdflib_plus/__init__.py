"""Import everything"""

from rdflib_plus.definitions import (
    RDF_PROPERTIES,
    RDFS_CLASSES,
    parse_class_definition_file,
    parse_property_definition_file,
)
from rdflib_plus.models import (
    Alt,
    Bag,
    Class,
    FunctionalProperty,
    InverseFunctionalProperty,
    List,
    NaryProperty,
    Ontology,
    Property,
    PropertyWithAttributes,
    Resource,
    Seq,
    SymmetricProperty,
    TransitiveProperty,
)
from rdflib_plus.namespaces import (
    DEFAULT_NAMESPACE,
    NAMESPACE_TO_PREFIX,
    PREFIX_TO_NAMESPACE,
    SHAPES_NAMESPACE,
    create_namespace,
)

__all__ = [
    "create_namespace",
    "parse_class_definition_file",
    "parse_property_definition_file",
    "Alt",
    "Bag",
    "Class",
    "FunctionalProperty",
    "InverseFunctionalProperty",
    "List",
    "NaryProperty",
    "Ontology",
    "Property",
    "PropertyWithAttributes",
    "Resource",
    "Seq",
    "SymmetricProperty",
    "TransitiveProperty",
    "RDF_PROPERTIES",
    "RDFS_CLASSES",
    "DEFAULT_NAMESPACE",
    "NAMESPACE_TO_PREFIX",
    "PREFIX_TO_NAMESPACE",
    "SHAPES_NAMESPACE",
]
