"""Test Alt's methods"""

import copy
import random as rd
from typing import Any, Optional

import pytest
from rdflib import Literal
from rdflib import URIRef as IRI

from rdflib_plus import Alt, SimpleGraph
from tests.parameters import (
    PARAMETERS_ELEMENT_LISTS,
    PARAMETERS_ELEMENTS,
    PARAMETERS_MODELS_COLLECTIONS,
    PARAMETERS_PROPERTIES_CONTAINER,
)
from tests.tests_methods.utils import build_collection, index_exact_match
from tests.utils import (
    SEED,
    cartesian_product,
    check_elements_unordered_collection,
    check_graph_alt,
    remove_duplicated_elements,
)

# Set random seed
rd.seed(SEED)


@pytest.mark.parametrize(
    "elements, elements_check, model",
    cartesian_product(
        PARAMETERS_ELEMENT_LISTS, [None, *PARAMETERS_MODELS_COLLECTIONS]
    ),
)
def test_elements(
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
    model: Optional[type],
):
    """Test Alt's elements setter."""

    # Initialize Alt
    alt, *_ = build_collection(Alt, allow_duplicates=False)

    # If a model is specified, create instance to initialize Alt with
    if model is not None:
        elements = model(SimpleGraph(), elements=elements)

    # Set elements property
    alt.elements = elements

    # Remove them from the list
    elements, elements_check = remove_duplicated_elements(
        elements, elements_check
    )

    # Check that Alt contains exactly all the elements
    check_elements_unordered_collection(alt, elements)

    # Check that the graph is correct after calling the method
    check_graph_alt(alt, elements_check)


@pytest.mark.parametrize(
    "alternatives, alternatives_check, model, allow_duplicates",
    cartesian_product(
        PARAMETERS_ELEMENT_LISTS,
        [None, *PARAMETERS_MODELS_COLLECTIONS],
        [True, False],
    ),
)
def test_alternatives(
    alternatives: list[IRI | Literal | Any],
    alternatives_check: list[IRI | Literal],
    allow_duplicates: bool,
    model: Optional[type],
):
    """Test Alt's alternatives setter."""

    # Initialize Alt
    alt, elements, elements_check = build_collection(
        Alt, allow_duplicates=allow_duplicates
    )

    # If a model is specified, create instance to initialize Alt with
    if model is not None:
        alternatives = model(SimpleGraph(), elements=alternatives)

    # Set elements property
    alt.alternatives = alternatives

    # Keep the first element (if any), and add the alternatives to make
    # the new element list
    if elements:
        elements = [elements[0]]
        elements_check = [elements_check[0]]
    elements += alternatives
    elements_check += alternatives_check

    # If duplicates are not allowed, remove any from the element list
    if not allow_duplicates:
        elements, elements_check = remove_duplicated_elements(
            elements, elements_check
        )

    # Check that Alt contains exactly all the elements
    check_elements_unordered_collection(alt, elements)

    # Check that the graph is correct after calling the method
    check_graph_alt(alt, elements_check)


@pytest.mark.parametrize(
    "default, default_check, allow_duplicates",
    cartesian_product(PARAMETERS_ELEMENTS, [True, False]),
)
def test_default(
    default: IRI | Literal | Any,
    default_check: IRI | Literal,
    allow_duplicates: bool,
):
    """Test Alt's default setter."""

    # Initialize Alt
    alt, elements, elements_check = build_collection(
        Alt, allow_duplicates=allow_duplicates
    )

    # Set default
    alt.default = default

    # If duplicates are not allowed
    if not allow_duplicates:

        # Remove any duplicate from the list
        elements, elements_check = remove_duplicated_elements(
            elements, elements_check
        )

        # Remove new default from the list (if it appears in it)
        index = index_exact_match(default_check, elements_check)
        if index is not None:
            del elements[index]
            del elements_check[index]

    # Check that the default and elements properties were updated correctly
    assert alt.default == default
    assert alt.elements[0] == default

    # Check that Alt contains exactly all the elements
    check_elements_unordered_collection(alt, [default] + elements)

    # Check that the graph is correct after calling the method
    check_graph_alt(alt, elements_check, default=default_check)


@pytest.mark.parametrize(
    "element, element_check, allow_duplicates",
    cartesian_product(PARAMETERS_ELEMENTS, [True, False]),
)
def test_add_alternative(
    element: IRI | Literal | Any,
    element_check: IRI | Literal,
    allow_duplicates: bool,
):
    """Test Alt's add_alternative() method."""

    # Initialize Alt
    alt, elements, elements_check = build_collection(
        Alt, allow_duplicates=allow_duplicates
    )

    # Add alternative
    alt.add_alternative(element)

    # If duplicates are not allowed, remove them from the list
    if not allow_duplicates:
        elements, elements_check = remove_duplicated_elements(
            elements, elements_check
        )

    # If duplicates are allowed, or new alternative does not appear in
    # original list
    if allow_duplicates or element_check not in elements_check:
        # Add new alternative to lists
        elements.append(element)
        elements_check.append(element_check)

    # Check that Alt contains exactly all the elements
    check_elements_unordered_collection(alt, elements)

    # Check that the graph is correct after calling the method
    check_graph_alt(alt, elements_check)


@pytest.mark.parametrize("elements, elements_check", PARAMETERS_ELEMENT_LISTS)
def test_any_alternative(
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
):
    """Test Alt's any_alternative() method."""

    # Initialize Alt
    alt = Alt(SimpleGraph(), elements=elements)

    # If no alternatives were specified, make sure that None is returned every
    # time
    if len(elements) < 2:
        for _ in range(10):
            assert alt.any_alternative() is None

    # Otherwise, make sure that elements from the list are returned every time
    else:
        for _ in range(3 * len(elements)):
            assert alt.any_alternative() in elements


@pytest.mark.parametrize("elements, elements_check", PARAMETERS_ELEMENT_LISTS)
def test_copy(
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
):
    """Test Alt's copy() method."""

    # Create Alt
    alt = Alt(SimpleGraph(), elements=elements)

    # Freeze the state of the graph before calling the method
    graph_before = copy.deepcopy(alt.graph)

    # Copy Alt
    alt_new = alt.copy()

    # Check that the copied Alt is of the correct type
    assert isinstance(alt_new, Alt)

    # Check that the copied Alt has the same elements, default and alternatives
    check_elements_unordered_collection(alt_new, elements)
    assert alt_new.default == alt.default
    assert alt_new.alternatives == alt.alternatives

    # Check that the copied Alt has the same properties
    for property_ in PARAMETERS_PROPERTIES_CONTAINER:
        if hasattr(alt, property_):
            assert getattr(alt, property_) == getattr(alt_new, property_)
        else:
            assert not hasattr(alt_new, property_)

    # Check that the graph is correct after calling the method
    check_graph_alt(alt_new, elements_check, graph_diff=graph_before)


# TODO: Write test for warning raised by count(), discard_element() and
#       remove_element()
