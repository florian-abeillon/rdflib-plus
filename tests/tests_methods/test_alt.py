"""Test Alt's methods"""

import copy
import random as rd
from typing import Any

import pytest
from rdflib import RDF, Literal
from rdflib import URIRef as IRI

from rdflib_plus import Alt
from tests.parameters import PARAMETERS_ELEMENT_LISTS, PARAMETERS_ELEMENTS
from tests.tests_methods.utils import (
    build_alt,
    build_collection,
    check_elements,
    get_default_alternatives,
)
from tests.utils import (
    SEED,
    cartesian_product,
    check_graph_diff_unordered_collection,
    parse_element_list_with_check,
)

# Set random seed
rd.seed(SEED)


# TODO: Adapt to Collection objects
@pytest.mark.parametrize(
    "element_list_with_check_before, element_list_with_check_after",
    cartesian_product(
        PARAMETERS_ELEMENT_LISTS,
        PARAMETERS_ELEMENT_LISTS,
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
    """Test Alt' elements setter."""

    # Parse lists of elements with check
    element_list_before, element_list_check_before = (
        parse_element_list_with_check(element_list_with_check_before)
    )
    element_list_after, element_list_check_after = (
        parse_element_list_with_check(element_list_with_check_after)
    )

    # Create Alt
    alt = build_collection(Alt, element_list=element_list_before)

    # Freeze the state of the graph before calling the method
    graph_before = copy.deepcopy(alt.graph)

    # Set elements property
    alt.elements = element_list_after

    # Check that collection appropriately contains all the elements of Alt
    check_elements(alt, element_list_after)

    if element_list_check_after:
        assert alt.default == element_list_after[0]

    default_before, alternatives_before = get_default_alternatives(
        element_list_with_check_before
    )
    default_after, alternatives_after = get_default_alternatives(
        element_list_with_check_after
    )

    triples_rem = (
        [(alt.iri, RDF["_1"], default_before)]
        if default_before is not None
        else []
    )
    triples_add = (
        [(alt.iri, RDF["_1"], default_after)]
        if default_after is not None
        else []
    )

    # Prepare the removed and additional predicates
    predicates_rem = [
        RDF[f"_{i + 1}"] for i in range(1, len(alternatives_before) + 1)
    ]
    predicates_add = [
        RDF[f"_{i + 1}"] for i in range(1, len(alternatives_after) + 1)
    ]

    # Check that the removed and additional predicates and objects are correct
    check_graph_diff_unordered_collection(
        graph_before,
        alt.graph,
        alt.iri,
        predicates_rem,
        predicates_add,
        alternatives_before,
        alternatives_after,
        triples_rem=triples_rem,
        triples_add=triples_add,
    )


# TODO: Check graph
@pytest.mark.parametrize(
    "new_default, new_default_check, element_list",
    cartesian_product(PARAMETERS_ELEMENTS, PARAMETERS_ELEMENT_LISTS),
)
def test_default(
    new_default: IRI | Literal | Any,
    new_default_check: IRI | Literal,
    element_list_with_check: list[tuple[IRI | Literal | Any, IRI | Literal]],
):
    """Test Alt's default setter."""

    # Parse list of elements with check
    element_list, element_list_check = parse_element_list_with_check(
        element_list_with_check
    )

    # Create Alt
    alt = build_alt(element_list=element_list)

    # Set default
    alt.default = new_default

    # Check that default and elements properties were updated correctly
    assert alt.default == new_default
    elements_after = [new_default] + [
        element for element in element_list if element != new_default
    ]
    assert alt.elements == elements_after


# TODO: Check graph
@pytest.mark.parametrize("element, element_check", PARAMETERS_ELEMENTS)
def test_add_alternative(
    element: IRI | Literal | Any, element_check: IRI | Literal
):
    """Test Alt's add_alternative() method."""

    # Arbitrarily select list of elements, and create Alt
    alt = build_alt()

    # Keep elements in memory
    element_set = copy.deepcopy(alt.elements)

    # Add alternative
    alt.add_alternative(element)

    # If element is not already in element_set, add it
    if element not in element_set:
        element_set.append(element)

    # Check that there are as many elements in Alt as in list
    assert len(alt.elements) == len(element_set)
    # Check that all elements in list also appear in Alt
    assert all(element in alt.elements for element in element_set)


@pytest.mark.parametrize("element_list", PARAMETERS_ELEMENT_LISTS)
def test_any_alternative(
    element_list_with_check: list[tuple[IRI | Literal | Any, IRI | Literal]],
):
    """Test Alt's any_alternative() method."""

    # Parse list of elements with check
    element_list, element_list_check = parse_element_list_with_check(
        element_list_with_check
    )

    # Create Alt
    alt = build_alt(element_list=element_list)

    # If no elements were specified
    if not element_list:
        # Make sure that None is returned every time
        for _ in range(10):
            assert alt.any_alternative() is None

    # Otherwise
    else:
        # Make sure that elements from the list are returned every time
        for _ in range(3 * len(element_list)):
            assert alt.any_alternative() in element_list
