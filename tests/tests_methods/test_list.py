"""Test List's methods"""

import copy
from typing import Any

import pytest
from rdflib import Literal
from rdflib import URIRef as IRI

from rdflib_plus import List
from tests.parameters import PARAMETERS_ELEMENT_LISTS_WITH_CHECK
from tests.tests_methods.utils import (
    build_collection,
    check_elements,
    parse_element_list_with_check,
    prepare_list_triples_for_check,
)
from tests.utils import cartesian_product, check_graph_triples


@pytest.mark.parametrize(
    "element_list_with_check_before, element_list_with_check_after",
    cartesian_product(
        PARAMETERS_ELEMENT_LISTS_WITH_CHECK,
        PARAMETERS_ELEMENT_LISTS_WITH_CHECK,
    ),
)
def test_elements(
    element_list_with_check_before: list[
        tuple[IRI | Literal | Any, IRI | Literal]
    ],
    element_list_with_check_after: list[
        tuple[IRI | Literal | Any, IRI | Literal]
    ],
):
    """Test List' elements setter."""

    # Parse lists of elements with check
    element_list_before, element_list_check_before = (
        parse_element_list_with_check(element_list_with_check_before)
    )
    element_list_after, element_list_check_after = (
        parse_element_list_with_check(element_list_with_check_after)
    )

    # Create List
    list_ = build_collection(List, element_list=element_list_before)

    # Freeze the state of the graph before calling the method
    graph_before = copy.deepcopy(list_.graph)
    graph_after = list_.graph

    # Set elements property
    list_.elements = element_list_after

    # Check that collection appropriately contains all the elements of list
    check_elements(List, list_.elements, element_list_after)

    # Prepare the removed and additional triples
    rem_triples = prepare_list_triples_for_check(
        list_.iri, element_list_check_before, graph_before
    )
    add_triples = prepare_list_triples_for_check(
        list_.iri, element_list_check_after, graph_after
    )

    # If the first element is the same in both lists
    if (
        element_list_before
        and element_list_after
        and element_list_check_before[0] == element_list_check_after[0]
    ):
        # Check that the first removed and additional triples are the same
        assert rem_triples[0] == add_triples[0]

        # Remove this first triple from both lists
        rem_triples = rem_triples[1:]
        add_triples = add_triples[1:]

    # Check the correctness of the removed and additional triples
    check_graph_triples(graph_before - graph_after, rem_triples, exact=True)
    check_graph_triples(graph_after - graph_before, add_triples, exact=True)
