"""Test Bag constructor"""

from typing import Any

import pytest
from rdflib import Literal
from rdflib import URIRef as IRI

from tests.parameters import PARAMETERS_BAG, PARAMETERS_ELEMENT_LISTS
from tests.tests_init.utils import (
    check_container_predicates,
    check_elements,
    check_init_blank_node_object,
    format_elements,
)


@pytest.mark.parametrize("element_list", PARAMETERS_ELEMENT_LISTS)
def test_init_with_elements(
    element_list: list[IRI | Literal | Any],
):
    """Test Bag creation with element list."""

    # Set kwargs to be used by constructor
    kwargs = {"elements": element_list}

    # Set additional triples
    elements = format_elements(element_list)
    add_triples = [(None, element) for element in elements]

    # Test constructor
    resource = check_init_blank_node_object(
        *PARAMETERS_BAG,
        kwargs=kwargs,
        add_triples=add_triples,
    )

    # Check Bag's "elements" attribute
    check_elements(resource, element_list)

    # Check that elements are related to resource with appropriate properties
    check_container_predicates(elements, resource)
