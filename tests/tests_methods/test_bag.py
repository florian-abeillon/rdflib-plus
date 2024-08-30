"""Test Bag's methods"""

import copy
from typing import Any

import pytest
from rdflib import Literal
from rdflib import URIRef as IRI

from rdflib_plus import Bag
from tests.parameters import PARAMETERS_ELEMENT_LISTS, PARAMETERS_ELEMENTS
from tests.tests_methods.utils import build_collection


# TODO: Check graph
@pytest.mark.parametrize("element", PARAMETERS_ELEMENTS)
def test_add_element(element: IRI | Literal | Any):
    """Test Bag's add_element() method."""

    # Arbitrarily select list of elements, and create Bag
    bag = build_collection(Bag)

    # Keep elements in memory
    bag_elements_before = copy.deepcopy(bag.elements)

    # Add element
    bag.add_element(element)

    # Check that there are as many elements in Collection object as in list
    assert len(bag.elements) == len(bag_elements_before) + 1
    # Check that all elements in list also appear in Collection
    assert all(
        element in bag.elements for element in bag_elements_before + [element]
    )


@pytest.mark.parametrize("element_list", PARAMETERS_ELEMENT_LISTS)
def test_any(
    element_list: list[IRI | Literal | Any],
):
    """Test Bag's any() method."""

    # Create Bag
    bag = build_collection(Bag, element_list=element_list)

    # If no elements were specified
    if not element_list:
        # Make sure that None is returned every time
        for _ in range(10):
            assert bag.any() is None

    # Otherwise
    else:
        # Make sure that elements from the list are returned every time
        for _ in range(3 * len(element_list)):
            assert bag.any() in element_list
