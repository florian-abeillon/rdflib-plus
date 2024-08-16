"""Define test parameters for models"""

from rdflib import OWL, RDF, RDFS
from rdflib import URIRef as IRI
from rdflib_plus import (
    Alt,
    Bag,
    Class,
    FunctionalProperty,
    InverseFunctionalProperty,
    List,
    Ontology,
    Property,
    Resource,
    Seq,
    SymmetricProperty,
    TransitiveProperty,
)
from tests.parameters.properties import (
    PARAMETERS_PROPERTIES_CLASS,
    PARAMETERS_PROPERTIES_CONTAINER,
    PARAMETERS_PROPERTIES_LIST,
    PARAMETERS_PROPERTIES_ONTOLOGY,
    PARAMETERS_PROPERTIES_PROPERTY,
    PARAMETERS_PROPERTIES_RESOURCE,
)

# 0 - Object constructor (type)
# 1 - Model name (str)
# 2 - Model IRI type (IRI)
# 3 - Model's valid properties (set[IRI])
PARAMETERS_ONTOLOGY: tuple[type, str, IRI, set[IRI], bool, bool] = (
    Ontology,
    "Ontology",
    OWL.Ontology,
    PARAMETERS_PROPERTIES_ONTOLOGY,
)
PARAMETERS_RESOURCE: tuple[type, str, IRI, set[IRI]] = (
    Resource,
    "Resource",
    RDFS.Resource,
    PARAMETERS_PROPERTIES_RESOURCE,
)

PARAMETERS_ALT: tuple[type, str, IRI, set[IRI]] = (
    Alt,
    "Alt",
    RDF.Alt,
    PARAMETERS_PROPERTIES_CONTAINER,
)
PARAMETERS_BAG: tuple[type, str, IRI, set[IRI]] = (
    Bag,
    "Bag",
    RDF.Bag,
    PARAMETERS_PROPERTIES_CONTAINER,
)
PARAMETERS_LIST: tuple[type, str, IRI, set[IRI]] = (
    List,
    "List",
    RDF.List,
    PARAMETERS_PROPERTIES_LIST,
)
PARAMETERS_SEQ: tuple[type, str, IRI, set[IRI]] = (
    Seq,
    "Seq",
    RDF.Seq,
    PARAMETERS_PROPERTIES_CONTAINER,
)

PARAMETERS_ORDERED_OBJECTS: list[tuple[type, str, IRI, set[IRI]]] = [
    PARAMETERS_ALT,
    PARAMETERS_BAG,
    PARAMETERS_LIST,
    PARAMETERS_SEQ,
]
PARAMETERS_BLANK_NODE_OBJECTS: list[tuple[type, str, IRI, set[IRI]]] = [
    PARAMETERS_RESOURCE,
    *PARAMETERS_ORDERED_OBJECTS,
]


# 0 - Object constructor (type)
# 1 - Model name (str)
# 2 - Model IRI type (IRI)
# 3 - Model's valid properties (set[IRI])
# 4 - Whether object label is in CamelCase (bool)
# 5 - Whether object label is in pascalCase (bool)
PARAMETERS_CLASS: tuple[type, str, IRI, set[IRI], bool, bool] = (
    Class,
    "Class",
    RDFS.Class,
    PARAMETERS_PROPERTIES_CLASS,
    True,
    False,
)
PARAMETERS_FUNCTIONAL_PROPERTY: tuple[type, str, IRI, set[IRI], bool, bool] = (
    FunctionalProperty,
    "FunctionalProperty",
    OWL.FunctionalProperty,
    PARAMETERS_PROPERTIES_PROPERTY,
    False,
    True,
)
PARAMETERS_INVERSE_FUNCTIONAL_PROPERTY: tuple[
    type, str, IRI, set[IRI], bool, bool
] = (
    InverseFunctionalProperty,
    "InverseFunctionalProperty",
    OWL.InverseFunctionalProperty,
    PARAMETERS_PROPERTIES_PROPERTY,
    False,
    True,
)
PARAMETERS_PROPERTY: tuple[type, str, IRI, set[IRI], bool, bool] = (
    Property,
    "Property",
    RDF.Property,
    PARAMETERS_PROPERTIES_PROPERTY,
    False,
    True,
)
PARAMETERS_SYMMETRIC_PROPERTY: tuple[type, str, IRI, set[IRI], bool, bool] = (
    SymmetricProperty,
    "SymmetricProperty",
    OWL.SymmetricProperty,
    PARAMETERS_PROPERTIES_PROPERTY,
    False,
    True,
)
PARAMETERS_TRANSITIVE_PROPERTY: tuple[type, str, IRI, set[IRI], bool, bool] = (
    TransitiveProperty,
    "TransitiveProperty",
    OWL.TransitiveProperty,
    PARAMETERS_PROPERTIES_PROPERTY,
    False,
    True,
)

PARAMETERS_LABELED_OBJECTS: list[
    tuple[type, str, IRI, set[IRI], bool, bool]
] = [
    (
        *PARAMETERS_RESOURCE,
        False,
        False,
    ),
    PARAMETERS_CLASS,
    PARAMETERS_FUNCTIONAL_PROPERTY,
    PARAMETERS_INVERSE_FUNCTIONAL_PROPERTY,
    PARAMETERS_PROPERTY,
    PARAMETERS_SYMMETRIC_PROPERTY,
    PARAMETERS_TRANSITIVE_PROPERTY,
]
