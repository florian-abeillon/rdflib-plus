"""Import OWL classes"""

from rdflib_plus.models.owl.owl_ontology import Ontology
from rdflib_plus.models.owl.owl_properties import (
    FunctionalProperty,
    InverseFunctionalProperty,
    SymmetricProperty,
    TransitiveProperty,
)

__all__ = [
    "FunctionalProperty",
    "InverseFunctionalProperty",
    "Ontology",
    "SymmetricProperty",
    "TransitiveProperty",
]
