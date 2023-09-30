"""Import useful classes"""

from rdflib_plus.models.owl_ontology import Ontology
from rdflib_plus.models.owl_properties import (
    FunctionalProperty,
    InverseFunctionalProperty,
    SymmetricProperty,
    TransitiveProperty,
)
from rdflib_plus.models.rdf_property import Property
from rdflib_plus.models.rdfs_class import Class
from rdflib_plus.models.rdfs_resource import Resource

__all__ = [
    "Property",
    "Class",
    "Resource",
    "Ontology",
    "FunctionalProperty",
    "InverseFunctionalProperty",
    "SymmetricProperty",
    "TransitiveProperty",
]
