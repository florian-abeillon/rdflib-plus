"""Import useful classes"""

from rdflib_plus.models.custom import NaryProperty, PropertyWithAttributes
from rdflib_plus.models.owl import (
    FunctionalProperty,
    InverseFunctionalProperty,
    Ontology,
    SymmetricProperty,
    TransitiveProperty,
)
from rdflib_plus.models.rdf import (
    Alt,
    Bag,
    Class,
    List,
    Property,
    Resource,
    Seq,
)

__all__ = [
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
]
