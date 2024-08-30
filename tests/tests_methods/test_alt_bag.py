"""Test Alt and Bag's methods"""

import copy
from typing import Any

import pytest
from rdflib import RDF, Literal
from rdflib import URIRef as IRI

from rdflib_plus import Alt
from tests.parameters import (
    PARAMETERS_ALT,
    PARAMETERS_BAG,
    PARAMETERS_ELEMENT_LISTS_WITH_CHECK,
)
from tests.tests_methods.utils import (
    build_collection,
    check_elements,
    parse_element_list_with_check,
)
from tests.utils import cartesian_product


@pytest.mark.parametrize(
    "model, model_name, model_type, properties, "
    "element_list_with_check_before, element_list_with_check_after",
    cartesian_product(
        [PARAMETERS_ALT, PARAMETERS_BAG],
        PARAMETERS_ELEMENT_LISTS_WITH_CHECK,
        PARAMETERS_ELEMENT_LISTS_WITH_CHECK,
    ),
)
def test_elements(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    element_list_with_check_before: list[
        tuple[IRI | Literal | Any, IRI | Literal]
    ],
    element_list_with_check_after: list[
        tuple[IRI | Literal | Any, IRI | Literal]
    ],
):
    """Test Alt and Bag's elements setter."""

    # Parse lists of elements with check
    element_list_before, element_list_check_before = (
        parse_element_list_with_check(element_list_with_check_before)
    )
    element_list_after, element_list_check_after = (
        parse_element_list_with_check(element_list_with_check_after)
    )

    # Create Alt or Bag object
    alt_or_bag = build_collection(model, element_list=element_list_before)

    # Freeze the state of the graph before calling the method
    graph_before = copy.deepcopy(alt_or_bag.graph)
    graph_after = alt_or_bag.graph

    # Set elements property
    alt_or_bag.elements = element_list_after

    # Check that Alt or Bag appropriately contains all the elements of list
    check_elements(model, alt_or_bag.elements, element_list_after)

    # Get the graphs of removed and additional triples
    rem_graph = graph_before - graph_after
    add_graph = graph_after - graph_before

    # If alt_or_bag is an Alt, turn lists into sets (no duplicated values)
    if isinstance(alt_or_bag, Alt):
        element_list_check_before = set(element_list_check_before)
        element_list_check_after = set(element_list_check_after)

    # For every element of the first list
    predicates_rem = set()
    for element_check_before in element_list_check_before:
        # Get the predicate(s) associated with this element, and keep them in
        # memory
        predicates = list(
            rem_graph.predicates(alt_or_bag.iri, element_check_before)
        )
        predicates_rem.update(predicates)

    # Check that the triples removed are only elements from alt_or_bag
    assert len(predicates_rem) == len(rem_graph)

    # For every predicate possible
    predicates_kept = []
    for i in range(len(element_list_check_before)):
        predicate = RDF[f"_{i + 1}"]

        # If predicate was not removed
        if not predicate in predicates_rem:
            # Get its value in the graph before calling the setter
            object_ = graph_before.value(alt_or_bag.iri, predicate, any=False)

            # Check that this value is in both lists
            assert (
                object_ in element_list_check_before
                and object_ in element_list_check_after
            )
            # Check that the triples is still in the graph after calling the setter
            assert (alt_or_bag.iri, predicate, object_) in graph_after

            # Keep this predicate in memory
            predicates_kept.append(predicate)

    # For every element of the second list
    predicates_add = set()
    for element_check_after in element_list_check_after:
        # Get the predicate(s) associated with this element, and keep them in
        # memory
        predicates = list(
            add_graph.predicates(alt_or_bag.iri, element_check_after)
        )
        predicates_add.update(predicates)

    # Check that the triples added are only elements from alt_or_bag
    assert len(predicates_add) == len(add_graph)

    # Check that every predicate possible was either added, or was already in
    # graph before calling the setter
    assert all(
        (RDF[f"_{i + 1}"] in predicates_add)
        ^ (RDF[f"_{i + 1}"] in predicates_kept)
        for i in range(len(element_list_check_after))
    )
