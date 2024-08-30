"""Test List and Seq's methods"""

import copy
import random as rd
from typing import Any, Callable, Optional

import pytest
from rdflib import Literal
from rdflib import URIRef as IRI

from tests.parameters import (
    PARAMETERS_ELEMENT_LISTS,
    PARAMETERS_ELEMENTS,
    PARAMETERS_KEY_FUNCTIONS,
    PARAMETERS_LIST,
    PARAMETERS_SEQ,
)
from tests.tests_methods.utils import build_collection, check_elements
from tests.utils import SEED, cartesian_product

# Set random seed
rd.seed(SEED)


@pytest.mark.parametrize(
    "model, model_name, model_type, properties, element_list",
    cartesian_product(
        [PARAMETERS_LIST, PARAMETERS_SEQ], PARAMETERS_ELEMENT_LISTS
    ),
)
def test_delitem(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    element_list: list[IRI | Literal | Any],
):
    """Test List and Seq's __delitem__ operator."""

    # Create List or Seq
    collection = build_collection(model, element_list=element_list)

    n = len(element_list)
    for i in range(n):

        # Get an index at random
        index = rd.randint(0, n - i - 1)

        # Remove element corresponding to this index
        del collection[index]

        # Check that the index-th element has indeed been removed
        del element_list[index]
        assert collection.elements == element_list


@pytest.mark.parametrize(
    "model, model_name, model_type, properties, element_list",
    cartesian_product(
        [PARAMETERS_LIST, PARAMETERS_SEQ], PARAMETERS_ELEMENT_LISTS
    ),
)
def test_getitem(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    element_list: list[IRI | Literal | Any],
):
    """Test List and Seq's __getitem__ operator."""

    # Create List or Seq
    collection = build_collection(model, element_list=element_list)

    # For every index
    for i, element in enumerate(element_list):
        # Check that the i-th element is the correct one
        assert collection[i] == element

    # TODO: Test slicers


@pytest.mark.parametrize(
    "model, model_name, model_type, properties, element_list",
    cartesian_product(
        [PARAMETERS_LIST, PARAMETERS_SEQ], PARAMETERS_ELEMENT_LISTS
    ),
)
def test_reversed(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    element_list: list[IRI | Literal | Any],
):
    """Test Lit and Seq's __reversed__ operator."""

    # Create List or Seq
    collection = build_collection(model, element_list=element_list)

    # Reverse object
    collection_reversed = reversed(collection)

    # Check that elements were reversed
    assert collection_reversed.elements == list(reversed(element_list))


@pytest.mark.parametrize(
    "model, model_name, model_type, properties, element_list",
    cartesian_product(
        [PARAMETERS_LIST, PARAMETERS_SEQ], PARAMETERS_ELEMENT_LISTS
    ),
)
def test_setitem(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    element_list: list[IRI | Literal | Any],
):
    """Test List and Seq's __setitem__ operator."""

    # Create List or Seq
    collection = build_collection(model)

    # Keep elements in memory
    collection_elements_before = copy.deepcopy(collection.elements)

    n = len(collection)
    for element in element_list:

        # Pick an index at random
        i = rd.randint(0, n - 1)

        # Set i-th element
        collection[i] = element

        # Check that the element was correctly replaced
        collection_elements_before[i] = element
        assert collection.elements == collection_elements_before


@pytest.mark.parametrize(
    "model, model_name, model_type, properties, element",
    cartesian_product([PARAMETERS_LIST, PARAMETERS_SEQ], PARAMETERS_ELEMENTS),
)
def test_append(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    element: IRI | Literal | Any,
):
    """Test List and Seq's append() method."""

    # Arbitrarily select list of elements, and create List or Seq
    collection = build_collection(model)

    # Keep elements in memory
    collection_elements_before = copy.deepcopy(collection.elements)

    # Append element
    collection.append(element)

    # Check that collection appropriately contains all the elements of list
    # plus element
    check_elements(
        model, collection.elements, collection_elements_before + [element]
    )


@pytest.mark.parametrize(
    "model, model_name, model_type, properties, element_list",
    cartesian_product(
        [PARAMETERS_LIST, PARAMETERS_SEQ], PARAMETERS_ELEMENT_LISTS
    ),
)
def test_index(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    element_list: list[IRI | Literal | Any],
):
    """Test List and Seq's index() method."""

    # Create List or Seq
    collection = build_collection(model, element_list=element_list)

    # Shuffle element_list
    element_list_original = copy.deepcopy(element_list)
    rd.shuffle(element_list)

    # For every element
    for element in element_list:
        # Check that the index returned is the same as for the original list
        assert collection.index(element) == element_list_original.index(
            element
        )


@pytest.mark.parametrize(
    "model, model_name, model_type, properties, element_list",
    cartesian_product(
        [PARAMETERS_LIST, PARAMETERS_SEQ], PARAMETERS_ELEMENT_LISTS
    ),
)
def test_index_with_start(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    element_list: list[IRI | Literal | Any],
):
    """Test List and Seq's index() method, while specifying a start index."""

    # Create List or Seq
    collection = build_collection(model, element_list=element_list)

    # Shuffle element_list
    element_list_original = copy.deepcopy(element_list)
    rd.shuffle(element_list)

    # For every element
    for element in element_list:
        # For every possible start
        for start in range(len(element_list)):
            # Try to find element in collection
            try:
                index_collection = collection.index(element, start=start)

            # If it cannot be found
            except ValueError:
                # Make sure that it cannot be found in list neither,
                # then go to the next element
                try:
                    element_list_original.index(element, start=start)
                    assert False
                except ValueError:
                    break

            # Check that the index returned is the same as for the original
            # list
            assert index_collection == element_list_original.index(
                element, start=start
            )


@pytest.mark.parametrize(
    "model, model_name, model_type, properties, element_list",
    cartesian_product(
        [PARAMETERS_LIST, PARAMETERS_SEQ], PARAMETERS_ELEMENT_LISTS
    ),
)
def test_index_with_end(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    element_list: list[IRI | Literal | Any],
):
    """Test List and Seq's index() method, while specifying a end index."""

    # Create List or Seq
    collection = build_collection(model, element_list=element_list)

    # Shuffle element_list
    element_list_original = copy.deepcopy(element_list)
    rd.shuffle(element_list)

    # For every element
    for element in element_list:
        # For every possible end
        for end in range(len(element_list)):
            end = len(element_list) - end - 1

            # Try to find element in collection
            try:
                index_collection = collection.index(element, end=end)

            # If it cannot be found
            except ValueError:
                # Make sure that it cannot be found in list neither,
                # then go to the next element
                try:
                    element_list_original.index(element, end=end)
                    assert False
                except ValueError:
                    break

            # Check that the index returned is the same as for the original
            # list
            assert index_collection == element_list_original.index(
                element, end=end
            )


@pytest.mark.parametrize(
    "model, model_name, model_type, properties, element_list",
    cartesian_product(
        [PARAMETERS_LIST, PARAMETERS_SEQ], PARAMETERS_ELEMENT_LISTS
    ),
)
def test_index_with_start_and_end(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    element_list: list[IRI | Literal | Any],
):
    """
    Test List and Seq's index() method, while specifying a start and an end
    indices.
    """

    # Create List or Seq
    collection = build_collection(model, element_list=element_list)

    # Shuffle element_list
    element_list_original = copy.deepcopy(element_list)
    rd.shuffle(element_list)

    # For every element
    for element in element_list:
        # For every possible start
        for start in range(len(element_list)):
            # For every possible end
            for end in range(len(element_list)):
                end = len(element_list) - end - 1

                # Try to find element in collection
                try:
                    index_collection = collection.index(
                        element, start=start, end=end
                    )

                # If it cannot be found
                except ValueError:
                    # Make sure that it cannot be found in list neither,
                    # then go to the next element
                    try:
                        element_list_original.index(
                            element, start=start, end=end
                        )
                        assert False
                    except ValueError:
                        break

                # Check that the index returned is the same as for the original
                # list
                assert index_collection == element_list_original.index(
                    element, start=start, end=end
                )


@pytest.mark.parametrize(
    "model, model_name, model_type, properties, element_list",
    cartesian_product(
        [PARAMETERS_LIST, PARAMETERS_SEQ], PARAMETERS_ELEMENT_LISTS
    ),
)
def test_insert(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    element_list: list[IRI | Literal | Any],
):
    """Test List and Seq's insert() method."""

    # Create List or Seq
    collection = build_collection(model)

    # Keep elements in memory
    collection_elements_before = copy.deepcopy(collection.elements)

    # For every element
    for element in element_list:
        # Get an index at random
        index = rd.randint(0, len(collection))

        # Insert element at the index that was just picked
        collection.insert(index, element)

        # Check that the element was indeed popped
        collection_elements_before.insert(index, element)
        assert collection.elements == collection_elements_before


@pytest.mark.parametrize(
    "model, model_name, model_type, properties, element_list",
    cartesian_product(
        [PARAMETERS_LIST, PARAMETERS_SEQ], PARAMETERS_ELEMENT_LISTS
    ),
)
def test_pop(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    element_list: list[IRI | Literal | Any],
):
    """Test List and Seq's pop() method."""

    # Create List or Seq
    collection = build_collection(model, element_list=element_list)

    # For every element
    n = len(element_list)
    for i in range(n):
        # Get an index at random
        index = rd.randint(0, n - i - 1)

        # Pop element corresponding at index
        element_collection = collection.pop(index)

        # Check that the element popped is the correct one
        element = element_list.pop(index)
        assert element_collection == element
        # Check that the element was indeed popped
        assert collection.elements == element_list


@pytest.mark.parametrize(
    "model, model_name, model_type, properties, element_list, key_function, "
    "reverse",
    cartesian_product(
        [PARAMETERS_LIST, PARAMETERS_SEQ],
        PARAMETERS_ELEMENT_LISTS,
        [None] + PARAMETERS_KEY_FUNCTIONS,
        [True, False],
    ),
)
def test_sort(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    element_list: list[IRI | Literal | Any],
    key_function: Optional[Callable],
    reverse: bool,
):
    """Test List and Seq's sort() method."""

    # Create List or Seq
    collection = build_collection(model, element_list=element_list)

    # Reverse object
    collection.sort(key=key_function, reverse=reverse)

    # Check that elements were sorted
    assert collection.elements == sorted(
        element_list, key=key_function, reverse=reverse
    )


@pytest.mark.parametrize(
    "model, model_name, model_type, properties, element_list",
    cartesian_product(
        [PARAMETERS_LIST, PARAMETERS_SEQ], PARAMETERS_ELEMENT_LISTS
    ),
)
def test_reverse(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    element_list: list[IRI | Literal | Any],
):
    """Test List and Seq's reverse() method."""

    # Create List or Seq
    collection = build_collection(model, element_list=element_list)

    # Reverse object
    collection.reverse()

    # Check that elements were reversed
    assert collection.elements == list(reversed(element_list))
