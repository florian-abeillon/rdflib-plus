"""Test Collection objects' methods"""

import copy
import random as rd
import re
from typing import Any, Optional

import pytest
from rdflib import Literal
from rdflib import URIRef as IRI

from rdflib_plus import Alt, Bag, SimpleGraph
from tests.parameters import (
    PARAMETERS_COLLECTIONS,
    PARAMETERS_ELEMENT_LISTS,
    PARAMETERS_MODELS_COLLECTIONS,
)
from tests.tests_methods.utils import (
    build_collection,
    count_exact_match,
    index_exact_match,
)
from tests.utils import SEED, cartesian_product, check_elements, check_graph

# Set random seed
rd.seed(SEED)


@pytest.mark.parametrize(
    "model, elements, elements_check, model_elements",
    cartesian_product(
        PARAMETERS_MODELS_COLLECTIONS,
        PARAMETERS_ELEMENT_LISTS,
        [None, *PARAMETERS_MODELS_COLLECTIONS],
    ),
)
def test_elements(
    model: type,
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
    model_elements: Optional[type],
):
    """Test Collection objects' elements setter."""

    # Create Collection object
    collection, *_ = build_collection(model)

    # If a model is specified, create instance to initialize Collection object
    # with
    if model_elements is not None:
        elements = model_elements(SimpleGraph(), elements=elements)

    # Set elements property
    collection.elements = elements

    # Check that Collection object contains exactly all the elements
    check_elements(collection, elements)

    # Check that the graph is correct after calling the method
    check_graph(collection, elements_check)


@pytest.mark.parametrize(
    "model, elements_add, elements_add_check, model_elements_add",
    cartesian_product(
        PARAMETERS_MODELS_COLLECTIONS,
        PARAMETERS_ELEMENT_LISTS,
        [None, *PARAMETERS_MODELS_COLLECTIONS],
    ),
)
def test_add(
    model: type,
    elements_add: list[IRI | Literal | Any],
    elements_add_check: list[IRI | Literal],
    model_elements_add: Optional[type],
) -> None:
    """Test Collection objects' __add__ operator."""

    # If model is Alt, skip test (Alt does not have extend() method)
    if model == Alt:
        return

    # Create Collection object
    collection, elements, elements_check = build_collection(model)

    # TODO: Find a better way, but otherwise too long
    if len(elements_add) > 20:
        elements_add_with_check = list(zip(elements_add, elements_add_check))
        elements_add_with_check = rd.sample(elements_add_with_check, 20)
        elements_add, elements_add_check = tuple(zip(*elements_add_with_check))
        elements_add = list(elements_add)
        elements_add_check = list(elements_add_check)

    # If a model is specified, create instance to initialize Collection object
    # with
    if model_elements_add is not None:
        elements_add = model_elements_add(SimpleGraph(), elements=elements_add)

    # Freeze the state of the graph before calling the method
    graph_before = copy.deepcopy(collection.graph)

    # Add sequence to Collection object
    collection_new = collection + elements_add

    # Extend lists with additional elements
    elements += elements_add
    elements_check += elements_add_check

    # Check that the newCollection object contains exactly all the elements
    check_elements(collection_new, elements)

    # Check that the graph is correct after calling the method
    check_graph(collection_new, elements_check, graph_diff=graph_before)


@pytest.mark.parametrize(
    "model, elements_add, elements_add_check",
    cartesian_product(PARAMETERS_MODELS_COLLECTIONS, PARAMETERS_ELEMENT_LISTS),
)
def test_contains(
    model: type,
    elements_add: list[IRI | Literal | Any],
    elements_add_check: list[IRI | Literal],
):
    """Test Collection objects' __contains__ operator."""

    # Create Collection object
    collection, elements, elements_check = build_collection(model)

    # Create an extended list from the original and another one, and shuffle it
    element_list_with_check_extended = list(
        zip(
            elements + elements_add,
            elements_check + elements_add_check,
        )
    )
    rd.shuffle(element_list_with_check_extended)

    # For every element of the extended list
    for element, element_check in element_list_with_check_extended:

        # Find the index of element in list, if it contains it
        # Only consider exact matches (eg. 0 != 0.0 != False)
        index = index_exact_match(element_check, elements_check)

        # If element appears in the original list
        if index is not None:
            # Check that the element is indeed in object
            assert element in collection

        # Otherwise
        else:
            # Check that the element is not in object
            assert element not in collection


@pytest.mark.parametrize(
    "model, elements_add, elements_add_check, model_elements_add",
    cartesian_product(
        PARAMETERS_MODELS_COLLECTIONS,
        PARAMETERS_ELEMENT_LISTS,
        [None, *PARAMETERS_MODELS_COLLECTIONS],
    ),
)
def test_iadd(
    model: type,
    elements_add: list[IRI | Literal | Any],
    elements_add_check: list[IRI | Literal],
    model_elements_add: Optional[type],
) -> None:
    """Test Collection objects' __iadd__ operator."""

    # If model is Alt, skip test (Alt does not have extend() method)
    if model == Alt:
        return

    # Create Collection object
    collection, elements, elements_check = build_collection(model)

    # TODO: Find a better way, but otherwise too long
    if len(elements_add) > 20:
        elements_add_with_check = list(zip(elements_add, elements_add_check))
        elements_add_with_check = rd.sample(elements_add_with_check, 20)
        elements_add, elements_add_check = tuple(zip(*elements_add_with_check))
        elements_add = list(elements_add)
        elements_add_check = list(elements_add_check)

    # If a model is specified, create instance to initialize Collection object
    # with
    if model_elements_add is not None:
        elements_add = model_elements_add(SimpleGraph(), elements=elements_add)

    # Add sequence to Collection object
    collection += elements_add

    # Extend lists with additional elements
    elements += elements_add
    elements_check += elements_add_check

    # Check that Collection object contains exactly all the elements
    check_elements(collection, elements)

    # Check that the graph is correct after calling the method
    check_graph(collection, elements_check)


@pytest.mark.parametrize(
    "model, elements, elements_check",
    cartesian_product(PARAMETERS_MODELS_COLLECTIONS, PARAMETERS_ELEMENT_LISTS),
)
def test_iter(
    model: type,
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
):
    """Test Collection's __iter__ operator."""

    # Create Collection object
    collection = model(SimpleGraph(), elements=elements)

    # Iterate over object
    i = 0
    for element in collection:

        # TODO: Put in PARAMETERS
        # If object is an Alt or a Bag
        if model in [Alt, Bag]:
            # Check that element is indeed part of object's elements
            assert element in elements

        # Otherwise, if object is a List or a Seq
        else:
            # Check that element is the i-th element of object's elements
            assert element == elements[i]

        # Increment i
        i += 1

    # Check that the number of iterations is equal to the number of elements
    assert i == len(elements)


@pytest.mark.parametrize(
    "model, elements, elements_check",
    cartesian_product(PARAMETERS_MODELS_COLLECTIONS, PARAMETERS_ELEMENT_LISTS),
)
def test_len(
    model: type,
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
):
    """Test Collection's __len__ operator."""

    # Create Collection object
    collection = model(SimpleGraph(), elements=elements)

    # Check that the length of the Collection object is correct
    assert len(collection) == len(elements)


@pytest.mark.parametrize(
    "model, model_name, model_type, properties, elements, elements_check",
    cartesian_product(PARAMETERS_COLLECTIONS, PARAMETERS_ELEMENT_LISTS),
)
def test_str(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
):
    """Test Collection objects' __str__ operator."""

    # Create Collection object
    collection = model(SimpleGraph(), elements=elements)

    # Get the string representation of Collection object, and parse it
    elements_str = re.findall(
        rf"^{model_name}\(((.+?\,\s)*.+?)?\)$", str(collection)
    )[0][0]
    assert elements_str or not elements
    elements_str = elements_str.split(", ") if elements_str else []

    # Check that the string representation contains all the elements
    assert all(str(element) in elements_str for element in elements)
    assert len(elements_str) == len(elements)


@pytest.mark.parametrize(
    "model, elements, elements_check",
    cartesian_product(PARAMETERS_MODELS_COLLECTIONS, PARAMETERS_ELEMENT_LISTS),
)
def test_clear(
    model: type,
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
):
    """Test Collection objects' clear() method."""

    # Create Collection object
    collection = model(SimpleGraph(), elements=elements)

    # Clear Collection object
    collection.clear()

    # Check that Collection object is empty
    check_elements(collection, [])

    # Check that the graph is correct after calling the method
    check_graph(collection, [])


@pytest.mark.parametrize(
    "model, model_name, model_type, properties, elements, elements_check",
    cartesian_product(PARAMETERS_COLLECTIONS, PARAMETERS_ELEMENT_LISTS),
)
def test_copy(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
):
    """Test Collection objects' copy() method."""

    # Create Collection object
    collection = model(SimpleGraph(), elements=elements)

    # Freeze the state of the graph before calling the method
    graph_before = copy.deepcopy(collection.graph)

    # Copy Collection object
    collection_new = collection.copy()

    # Check that the copied Collection object is of the correct type
    assert isinstance(collection_new, model)

    # Check that the copied Collection object has the same elements
    check_elements(collection_new, elements)

    # Check that the copied Collection object has the same properties
    for property_ in properties:
        if hasattr(collection, property_):
            assert getattr(collection, property_) == getattr(
                collection_new, property_
            )
        else:
            assert not hasattr(collection_new, property_)

    # Check that the graph is correct after calling the method
    check_graph(collection_new, elements_check, graph_diff=graph_before)


@pytest.mark.parametrize(
    "model, elements_add, elements_add_check",
    cartesian_product(PARAMETERS_MODELS_COLLECTIONS, PARAMETERS_ELEMENT_LISTS),
)
def test_count(
    model: type,
    elements_add: list[IRI | Literal | Any],
    elements_add_check: list[IRI | Literal],
):
    """Test Collection objects' count() method."""

    # Create Collection object
    collection, elements, elements_check = build_collection(model)

    # Create an extended list from the original and another one, and shuffle it
    elements_with_check_extended = list(
        zip(
            elements + elements_add,
            elements_check + elements_add_check,
        )
    )
    elements_with_check_extended = list(set(elements_with_check_extended))
    rd.shuffle(elements_with_check_extended)

    # For every element of the extended list
    for element, element_check in elements_with_check_extended:

        # Check that the number of time it appears in the original list is
        # returned
        assert collection.count(element) == count_exact_match(
            element_check, elements_check
        )


@pytest.mark.parametrize(
    "model, elements_add, elements_add_check",
    cartesian_product(PARAMETERS_MODELS_COLLECTIONS, PARAMETERS_ELEMENT_LISTS),
)
def test_discard_element(
    model: type,
    elements_add: list[IRI | Literal | Any],
    elements_add_check: list[IRI | Literal],
):
    """Test Collection objects' discard_element() method."""

    # Create Collection object
    collection, elements, elements_check = build_collection(model)

    # Create an extended list from the original and another one, and shuffle it
    elements_with_check_extended = list(
        zip(
            elements + elements_add,
            elements_check + elements_add_check,
        )
    )
    rd.shuffle(elements_with_check_extended)

    # For every element of the extended list
    for element, element_check in elements_with_check_extended:

        # Discard element from object
        collection.discard_element(element)

        # Find the index of element in list, if it contains it
        # Only consider exact matches (eg. 0 != 0.0 != False)
        index = index_exact_match(element_check, elements_check)

        # If element is in Collection object, remove it from the list
        if index is not None:
            del elements[index]
            del elements_check[index]

        # Check that Collection object contains exactly all the elements
        check_elements(collection, elements)

        # Check that the graph is correct after calling the method
        check_graph(collection, elements_check)


@pytest.mark.parametrize(
    "model, elements_add, elements_add_check, model_elements_add",
    cartesian_product(
        PARAMETERS_MODELS_COLLECTIONS,
        PARAMETERS_ELEMENT_LISTS,
        [None, *PARAMETERS_MODELS_COLLECTIONS],
    ),
)
def test_extend(
    model: type,
    elements_add: list[IRI | Literal | Any],
    elements_add_check: list[IRI | Literal],
    model_elements_add: Optional[type],
) -> None:
    """Test Collection objects' extend() method."""

    # If model is Alt, skip test (Alt does not have extend() method)
    if model == Alt:
        return

    # Create Collection object
    collection, elements, elements_check = build_collection(model)

    # TODO: Find a better way, but otherwise too long
    if len(elements_add) > 20:
        elements_add_with_check = list(zip(elements_add, elements_add_check))
        elements_add_with_check = rd.sample(elements_add_with_check, 20)
        elements_add, elements_add_check = tuple(zip(*elements_add_with_check))
        elements_add = list(elements_add)
        elements_add_check = list(elements_add_check)

    # If a model is specified, create instance to initialize Collection object
    # with
    if model_elements_add is not None:
        elements_add = model_elements_add(SimpleGraph(), elements=elements_add)

    # Extend Collection object
    collection.extend(elements_add)

    # Extend lists with additional elements
    elements += elements_add
    elements_check += elements_add_check

    # Check that Collection object contains exactly all the elements
    check_elements(collection, elements)

    # Check that the graph is correct after calling the method
    check_graph(collection, elements_check)


@pytest.mark.parametrize(
    "model, elements_add, elements_add_check",
    cartesian_product(PARAMETERS_MODELS_COLLECTIONS, PARAMETERS_ELEMENT_LISTS),
)
def test_remove_element(
    model: type,
    elements_add: list[IRI | Literal | Any],
    elements_add_check: list[IRI | Literal],
):
    """Test Collection objects' remove_element() method."""

    # Create Collection object
    collection, elements, elements_check = build_collection(model)

    # Create an extended list from the original and another one, and shuffle it
    elements_with_check_extended = list(
        zip(
            elements + elements_add,
            elements_check + elements_add_check,
        )
    )
    rd.shuffle(elements_with_check_extended)

    # For every element of the extended list
    for element, element_check in elements_with_check_extended:

        # Find the index of element in list, if it contains it
        # Only consider exact matches (eg. 0 != 0.0 != False)
        index = index_exact_match(element_check, elements_check)

        # Try to remove element from object
        try:
            collection.remove_element(element)
            assert index is not None

            # If element is in Collection object, remove it from the list
            del elements[index]
            del elements_check[index]

        except ValueError:
            assert index is None

        # Check that Collection object contains exactly all the elements
        check_elements(collection, elements)

        # Check that the graph is correct after calling the method
        check_graph(collection, elements_check)
