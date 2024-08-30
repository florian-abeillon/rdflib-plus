"""Test Alt's methods"""

import copy
import random as rd
from typing import Any

import pytest
from rdflib import Literal
from rdflib import URIRef as IRI

from tests.parameters import PARAMETERS_ELEMENT_LISTS, PARAMETERS_ELEMENTS
from tests.tests_methods.utils import build_alt
from tests.utils import SEED, cartesian_product

# Set random seed
rd.seed(SEED)


# TODO: Check graph
@pytest.mark.parametrize(
    "new_default, element_list",
    cartesian_product(PARAMETERS_ELEMENTS, PARAMETERS_ELEMENT_LISTS),
)
def test_default(
    new_default: IRI | Literal | Any,
    element_list: list[IRI | Literal | Any],
):
    """Test Alt's default setter."""

    # Create Alt
    alt = build_alt(element_list=element_list)

    # Remove new_default from Alt's elements
    elements_before = copy.deepcopy(alt.elements)

    # Set default
    alt.default = new_default

    # Check that default and elements properties were updated correctly
    assert alt.default == new_default
    elements_after = [new_default] + [
        element for element in elements_before if element != new_default
    ]
    assert alt.elements == elements_after


# TODO: Check graph
@pytest.mark.parametrize("element", PARAMETERS_ELEMENTS)
def test_add_alternative(element: IRI | Literal | Any):
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
    element_list: list[IRI | Literal | Any],
):
    """Test Alt's any_alternative() method."""

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
