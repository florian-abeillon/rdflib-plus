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

# 0 - List of list of elements and as they should appear in the graph
#     (list[list[tuple[IRI | Literal | Any, IRI | Literal]]])
PARAMETERS_ELEMENT_LISTS: list[
    list[tuple[IRI | Literal | Any, IRI | Literal]]
] = [
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

# Turn each parameter from list of pairs to pair of lists
PARAMETERS_ELEMENT_LISTS: list[
    tuple[list[IRI | Literal | Any], list[IRI | Literal]]
] = [
    (
        [element for element, element_check in parameters_elements],
        [element_check for element, element_check in parameters_elements],
    )
    # tuple(
    #     list(parameter_element)
    #     for parameter_element in tuple(zip(*parameters_elements))
    # )
    for parameters_elements in PARAMETERS_ELEMENT_LISTS
]
