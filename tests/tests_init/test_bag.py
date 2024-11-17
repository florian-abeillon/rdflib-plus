"""Test Bag constructor"""

from typing import Any

import pytest
from rdflib import Literal
from rdflib import URIRef as IRI

from tests.parameters import PARAMETERS_BAG, PARAMETERS_ELEMENT_LISTS
from tests.tests_init.utils import check_init_blank_node_object
from tests.utils import check_elements_unordered_collection, check_graph_bag


@pytest.mark.parametrize("elements, elements_check", PARAMETERS_ELEMENT_LISTS)
def test_init_with_elements(
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
):
    """Test Bag creation with element list."""

    # Set kwargs to be used by constructor
    kwargs = {"elements": elements}

    # Test constructor
    bag = check_init_blank_node_object(
        *PARAMETERS_BAG,
        kwargs=kwargs,
        check_triples=False,
    )

    # Check that Bag contains exactly all the elements
    check_elements_unordered_collection(bag, elements)

    # Check that the graph is correct after calling the method
    check_graph_bag(bag, elements_check)
