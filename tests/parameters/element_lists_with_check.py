"""Define test parameters for object elements"""

from typing import Any

from rdflib import Literal
from rdflib import URIRef as IRI

from tests.parameters.elements_with_check import (
    PARAMETERS_ELEMENTS_BOOLEAN_WITH_CHECK,
    PARAMETERS_ELEMENTS_DOUBLE_WITH_CHECK,
    PARAMETERS_ELEMENTS_INTEGER_WITH_CHECK,
    PARAMETERS_ELEMENTS_IRI_WITH_CHECK,
    PARAMETERS_ELEMENTS_LITERAL_BOOLEAN_WITH_CHECK,
    PARAMETERS_ELEMENTS_LITERAL_DOUBLE_WITH_CHECK,
    PARAMETERS_ELEMENTS_LITERAL_INTEGER_WITH_CHECK,
    PARAMETERS_ELEMENTS_LITERAL_LANGSTRING_WITH_CHECK,
    PARAMETERS_ELEMENTS_LITERAL_STRING_WITH_CHECK,
    PARAMETERS_ELEMENTS_STRING_WITH_CHECK,
)

# 0 - List of elements and as they should appear in the graph
#     (list[IRI | Literal | Any])
PARAMETERS_ELEMENT_LISTS_WITH_CHECK: list[list[IRI | Literal | Any]] = [
    # Empty list
    [],
    # Boolean only
    PARAMETERS_ELEMENTS_BOOLEAN_WITH_CHECK,
    # Float only
    PARAMETERS_ELEMENTS_DOUBLE_WITH_CHECK,
    # Integer only
    PARAMETERS_ELEMENTS_INTEGER_WITH_CHECK,
    # IRI only
    PARAMETERS_ELEMENTS_IRI_WITH_CHECK,
    # Literal boolean only
    PARAMETERS_ELEMENTS_LITERAL_BOOLEAN_WITH_CHECK,
    # Literal float only
    PARAMETERS_ELEMENTS_LITERAL_DOUBLE_WITH_CHECK,
    # Literal integer only
    PARAMETERS_ELEMENTS_LITERAL_INTEGER_WITH_CHECK,
    # Literal string only
    PARAMETERS_ELEMENTS_LITERAL_STRING_WITH_CHECK,
    # Literal string with lang only
    PARAMETERS_ELEMENTS_LITERAL_LANGSTRING_WITH_CHECK,
    # Literal string only
    PARAMETERS_ELEMENTS_STRING_WITH_CHECK,
]

# Add list of elements with mixed types
PARAMETERS_ELEMENT_LISTS_WITH_CHECK.append(
    [
        element_with_check
        for parameter_elements_with_check in PARAMETERS_ELEMENT_LISTS_WITH_CHECK
        for element_with_check in parameter_elements_with_check
    ]
)

# For each elements list, add list of elements with duplicates
PARAMETERS_ELEMENT_LISTS_WITH_CHECK.extend(
    [
        parameter_elements_with_check + parameter_elements_with_check
        for parameter_elements_with_check in PARAMETERS_ELEMENT_LISTS_WITH_CHECK
        if len(parameter_elements_with_check) > 0
    ]
)
