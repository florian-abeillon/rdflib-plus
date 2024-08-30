"""Define test parameters for object elements"""

from typing import Any

from rdflib import Literal
from rdflib import URIRef as IRI

from tests.parameters.elements import (
    PARAMETERS_ELEMENTS_BOOLEAN,
    PARAMETERS_ELEMENTS_DOUBLE,
    PARAMETERS_ELEMENTS_INTEGER,
    PARAMETERS_ELEMENTS_IRI,
    PARAMETERS_ELEMENTS_LITERAL_BOOLEAN,
    PARAMETERS_ELEMENTS_LITERAL_DOUBLE,
    PARAMETERS_ELEMENTS_LITERAL_INTEGER,
    PARAMETERS_ELEMENTS_LITERAL_LANGSTRING,
    PARAMETERS_ELEMENTS_LITERAL_STRING,
    PARAMETERS_ELEMENTS_STRING,
)

# 0 - List of elements and as they should appear in the graph
#     (list[IRI | Literal | Any])
PARAMETERS_ELEMENT_LISTS: list[list[IRI | Literal | Any]] = [
    # Empty list
    [],
    # Boolean only
    PARAMETERS_ELEMENTS_BOOLEAN,
    # Float only
    PARAMETERS_ELEMENTS_DOUBLE,
    # Integer only
    PARAMETERS_ELEMENTS_INTEGER,
    # IRI only
    PARAMETERS_ELEMENTS_IRI,
    # Literal boolean only
    PARAMETERS_ELEMENTS_LITERAL_BOOLEAN,
    # Literal float only
    PARAMETERS_ELEMENTS_LITERAL_DOUBLE,
    # Literal integer only
    PARAMETERS_ELEMENTS_LITERAL_INTEGER,
    # Literal string only
    PARAMETERS_ELEMENTS_LITERAL_STRING,
    # Literal string with lang only
    PARAMETERS_ELEMENTS_LITERAL_LANGSTRING,
    # Literal string only
    PARAMETERS_ELEMENTS_STRING,
]

# Add list of elements with mixed types
PARAMETERS_ELEMENT_LISTS.append(
    [
        element
        for parameter_elements in PARAMETERS_ELEMENT_LISTS
        for element in parameter_elements
    ]
)

# For each elements list, add list of elements with duplicates
PARAMETERS_ELEMENT_LISTS.extend(
    [
        parameter_elements + parameter_elements
        for parameter_elements in PARAMETERS_ELEMENT_LISTS
        if len(parameter_elements) > 0
    ]
)
