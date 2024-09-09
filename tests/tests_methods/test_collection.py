"""Test Collection objects' methods"""

import random as rd
import re
from typing import Any

import pytest
from rdflib import Literal
from rdflib import URIRef as IRI

from rdflib_plus import Alt, Bag
from tests.parameters import PARAMETERS_COLLECTIONS, PARAMETERS_ELEMENT_LISTS
from tests.tests_methods.utils import (
    build_collection,
    check_elements,
    get_another_parameter,
)
from tests.utils import SEED, cartesian_product

# Set random seed
rd.seed(SEED)


@pytest.mark.parametrize(
    "model, model_name, model_type, properties, element_list",
    cartesian_product(PARAMETERS_COLLECTIONS, PARAMETERS_ELEMENT_LISTS),
)
def test_contains(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    element_list: list[IRI | Literal | Any],
):
    """Test Collection objects' __contains__ operator."""

    # Create Collection object
    collection = build_collection(model, element_list=element_list)

    # Get another list of elements, that has different elements
    # than element_list
    element_set = set(element_list)
    element_list_2 = get_another_parameter(
        PARAMETERS_ELEMENT_LISTS,
        key=lambda new_parameter: new_parameter
        and set(new_parameter) != element_set,
    )

    # For every element of the original and of the second lists
    for element in element_list + element_list_2:
        # If element appears in the original list
        if element in element_list:
            # Check that the element is indeed in object
            assert element in collection

        # Otherwise
        else:
            # Check that the element is not in object
            assert element not in collection


@pytest.mark.parametrize(
    "model, model_name, model_type, properties, element_list",
    cartesian_product(PARAMETERS_COLLECTIONS, PARAMETERS_ELEMENT_LISTS),
)
def test_iter(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    element_list: list[IRI | Literal | Any],
):
    """Test Collection's __iter__ operator."""

    # Create Collection object
    collection = build_collection(model, element_list=element_list)

    # Iterate over object
    i = 0
    for element in iter(collection):
        # If object is an Alt or a Bag
        if model in [Alt, Bag]:
            # Check that element is indeed part of object's elements
            assert element in element_list

        # Otherwise, if object is a List or a Seq
        else:
            # Check that element is the i-th element of object's elements
            assert element == element_list[i]

        # Increment i
        i += 1

    # Check that the number of iterations is equal to the number of elements
    if model == Alt:
        assert i == len(set(element_list))
    else:
        assert i == len(element_list)


@pytest.mark.parametrize(
    "model, model_name, model_type, properties, element_list",
    cartesian_product(PARAMETERS_COLLECTIONS, PARAMETERS_ELEMENT_LISTS),
)
def test_len(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    element_list: list[IRI | Literal | Any],
):
    """Test Collection's __len__ operator."""

    # Create Collection object
    collection = build_collection(model, element_list=element_list)

    # Check that the length of the object is correct
    if model == Alt:
        assert len(collection) == len(set(element_list))
    else:
        assert len(collection) == len(element_list)


@pytest.mark.parametrize(
    "model, model_name, model_type, properties, element_list",
    cartesian_product(PARAMETERS_COLLECTIONS, PARAMETERS_ELEMENT_LISTS),
)
def test_str(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    element_list: list[IRI | Literal | Any],
):
    """Test Collection objects' __str__ operator."""

    # Create Collection object
    collection = build_collection(model, element_list=element_list)

    # Check that the string representation of the collection has the
    # appropriate form
    str_collection = re.findall(
        rf"^{model_name}\(((.+?\,\s)*.+?)?\)$", str(collection)
    )[0][0]
    assert str_collection or not element_list

    # Check that the string representation contains all the elements
    elements_in_str_collection = (
        str_collection.split(", ") if str_collection else []
    )
    str_element_list = [str(element) for element in element_list]
    str_element_set = [str(element) for element in set(element_list)]
    # TODO: Broken
    check_elements(
        model,
        elements_in_str_collection,
        str_element_set,
        # str_element_list,
        # element_set=str_element_set,
    )


@pytest.mark.parametrize(
    "model, model_name, model_type, properties, element_list",
    cartesian_product(PARAMETERS_COLLECTIONS, PARAMETERS_ELEMENT_LISTS),
)
def test_count(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    element_list: list[IRI | Literal | Any],
):
    """Test Collection objects' __contains__() method."""

    # Create Collection object
    collection = build_collection(model, element_list=element_list)

    # Get another list of elements, that has different elements
    # than element_list
    element_set = set(element_list)
    element_list_2 = get_another_parameter(
        PARAMETERS_ELEMENT_LISTS,
        key=lambda new_parameter: new_parameter
        and set(new_parameter) != element_set,
    )

    # For every element of the original and of the second lists
    for element in element_list + element_list_2:
        # If element appears in the original list
        if element in element_list:

            # If object is an Alt
            if model == Alt:
                # Check that 1 is returned
                assert collection.count(element) == 1

            # Otherwise
            else:
                # Check that the number of time it appears in the original
                # list is returned
                assert collection.count(element) == element_list.count(element)

        # Otherwise
        else:
            # Check that 0 is returned
            assert collection.count(element) == 0
