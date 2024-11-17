"""Test Bag's methods"""

import random as rd
from typing import Any, Optional

import pytest
from rdflib import Literal
from rdflib import URIRef as IRI

from rdflib_plus import Bag, SimpleGraph
from tests.parameters import (
    PARAMETERS_ELEMENT_LISTS,
    PARAMETERS_ELEMENTS,
    PARAMETERS_MODELS_COLLECTIONS,
)
from tests.tests_methods.utils import build_collection
from tests.utils import (
    SEED,
    cartesian_product,
    check_elements_unordered_collection,
    check_graph_bag,
)

# Set random seed
rd.seed(SEED)


@pytest.mark.parametrize("element, element_check", PARAMETERS_ELEMENTS)
def test_add_element(
    element: IRI | Literal | Any,
    element_check: IRI | Literal,
):
    """Test Bag's add_element() method."""

    # Initialize Bag
    bag, elements, elements_check = build_collection(Bag)

    # Add element
    bag.add_element(element)

    # Add new element to lists
    elements.append(element)
    elements_check.append(element_check)

    # Check that Bag contains exactly all the elements
    check_elements_unordered_collection(bag, elements)

    # Check that the graph is correct after calling the method
    check_graph_bag(bag, elements_check)


@pytest.mark.parametrize("elements, elements_check", PARAMETERS_ELEMENT_LISTS)
def test_any(
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
):
    """Test Bag's any() method."""

    # Create Bag
    bag = Bag(SimpleGraph(), elements=elements)

    # If no elements were specified, make sure that None is returned every time
    if not elements:
        for _ in range(10):
            assert bag.any() is None

    # Otherwise, make sure that elements from the list are returned every time
    else:
        for _ in range(3 * len(elements)):
            assert bag.any() in elements


@pytest.mark.parametrize(
    "elements_add, elements_add_check, model_elements_add",
    cartesian_product(
        PARAMETERS_ELEMENT_LISTS,
        [None, *PARAMETERS_MODELS_COLLECTIONS],
    ),
)
def test_extend(
    elements_add: list[IRI | Literal | Any],
    elements_add_check: list[IRI | Literal],
    model_elements_add: Optional[type],
) -> None:
    """Test Bag's extend() method."""

    # Create Bag
    bag, elements, elements_check = build_collection(Bag)

    # TODO: Find a better way, but otherwise too long
    if len(elements_add) > 20:
        elements_add_with_check = list(zip(elements_add, elements_add_check))
        elements_add_with_check = rd.sample(elements_add_with_check, 20)
        elements_add, elements_add_check = tuple(zip(*elements_add_with_check))
        elements_add = list(elements_add)
        elements_add_check = list(elements_add_check)

    # If a model is specified, create instance to initialize Bag
    # with
    if model_elements_add is not None:
        elements_add = model_elements_add(SimpleGraph(), elements=elements_add)

    # Extend Bag
    bag.extend(elements_add)

    # Extend lists with additional elements
    elements += elements_add
    elements_check += elements_add_check

    # Check that Bag contains exactly all the elements
    check_elements_unordered_collection(bag, elements)

    # Check that the graph is correct after calling the method
    check_graph_bag(bag, elements_check)
