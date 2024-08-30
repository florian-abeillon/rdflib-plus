"""Test Seq's methods"""

import copy
from typing import Any

import pytest
from rdflib import RDF, Literal
from rdflib import URIRef as IRI

from rdflib_plus import Seq
from tests.parameters import PARAMETERS_ELEMENT_LISTS_WITH_CHECK
from tests.tests_methods.utils import (
    build_collection,
    check_elements,
    parse_element_list_with_check,
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
    """Test Seq' elements setter."""

    # Parse lists of elements with check
    element_list_before, element_list_check_before = (
        parse_element_list_with_check(element_list_with_check_before)
    )
    element_list_after, element_list_check_after = (
        parse_element_list_with_check(element_list_with_check_after)
    )

    # Create Seq
    seq = build_collection(Seq, element_list=element_list_before)

    # Freeze the state of the graph before calling the method
    graph_before = copy.deepcopy(seq.graph)
    graph_after = seq.graph

    # Set elements property
    seq.elements = element_list_after

    # Check that collection appropriately contains all the elements of Seq
    check_elements(Seq, seq.elements, element_list_after)

    # Prepare the removed and additional triples
    rem_triples = [
        (seq.iri, RDF[f"_{i + 1}"], element_check_before)
        for i, element_check_before in enumerate(element_list_check_before)
    ]
    add_triples = [
        (seq.iri, RDF[f"_{i + 1}"], element_check_after)
        for i, element_check_after in enumerate(element_list_check_after)
    ]

    # Iterate on both lists
    idx_to_remove = []
    for i, (element_check_before, element_check_after) in enumerate(
        zip(element_list_check_before, element_list_check_after)
    ):
        # If one element is the same and at the same index
        if element_check_before == element_check_after:
            # Check that the related removed and additional triples are the same
            assert rem_triples[i] == add_triples[i]

            # Append related index to the list of indices to remove
            idx_to_remove.append(i)

    # Remove the indices from removed and additional triple lists
    rem_triples = [
        rem_triple
        for i, rem_triple in enumerate(rem_triples)
        if i not in idx_to_remove
    ]
    add_triples = [
        add_triple
        for i, add_triple in enumerate(add_triples)
        if i not in idx_to_remove
    ]

    # Check the correctness of the removed and additional triples
    check_graph_triples(graph_before - graph_after, rem_triples, exact=True)
    check_graph_triples(graph_after - graph_before, add_triples, exact=True)
