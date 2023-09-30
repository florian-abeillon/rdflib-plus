"""Possible constraints of triple objects"""

from rdflib_plus.definitions.utils import parse_prefixed_iri

CONSTRAINTS_OBJECTS = {
    "class": parse_prefixed_iri,
    "datatype": parse_prefixed_iri,
    "minCount": None,
    "maxCount": None,
}
