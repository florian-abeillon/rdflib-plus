"""Test ordered collections' methods"""

import random as rd
from contextlib import nullcontext
from typing import Any, Callable, Iterable, Optional

import pytest
from rdflib import Literal
from rdflib import URIRef as IRI

from rdflib_plus import Alt, SimpleGraph
from tests.parameters import (
    PARAMETERS_ELEMENT_LISTS,
    PARAMETERS_ELEMENTS,
    PARAMETERS_KEY_FUNCTIONS,
    PARAMETERS_MODELS_COLLECTIONS,
    PARAMETERS_MODELS_ORDERED_COLLECTIONS,
)
from tests.tests_methods.utils import build_collection, index_exact_match
from tests.utils import (
    SEED,
    cartesian_product,
    check_elements_ordered_collection,
    check_graph_collection,
)

# Set random seed
rd.seed(SEED)


# TODO: Write tests with indices outside of range, raising errors
@pytest.mark.parametrize(
    "model, elements, elements_check",
    cartesian_product(
        PARAMETERS_MODELS_ORDERED_COLLECTIONS, PARAMETERS_ELEMENT_LISTS
    ),
)
def test_delitem(
    model: type,
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
):
    """Test ordered collections' __delitem__ operator."""

    # Create ordered collection
    collection = model(SimpleGraph(), elements=elements)

    # For every element of the list
    n = len(elements)
    for _ in range(n):

        # Get an index at random
        index = rd.randint(-n, n - 1)

        # Remove element corresponding to this index
        del collection[index]

        # Remove element from lists as well
        del elements[index]
        del elements_check[index]
        n -= 1

        # Check that Seq contains exactly all the elements
        check_elements_ordered_collection(collection, elements)

        # Check that the graph is correct after calling the method
        check_graph_collection(collection, elements_check)


@pytest.mark.parametrize(
    "model, elements, elements_check",
    cartesian_product(
        PARAMETERS_MODELS_ORDERED_COLLECTIONS, PARAMETERS_ELEMENT_LISTS
    ),
)
def test_getitem(
    model: type,
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
):
    """Test ordered collections' __getitem__ operator."""

    # Create ordered collection
    collection = model(SimpleGraph(), elements=elements)

    # For every index
    n = len(elements)
    for i in range(n):

        # Check that the i-th element is the correct one
        assert collection[i] == elements[i]

        # Check that the -(i + 1)-th element is the correct one
        assert collection[-(i + 1)] == elements[-(i + 1)]

    # For every index
    for i in range(n):

        # Check that slicing returns the correct list
        assert collection[i:] == elements[i:]
        assert collection[:i] == elements[:i]
        assert collection[-(i + 1) :] == elements[-(i + 1) :]
        assert collection[: -(i + 1)] == elements[: -(i + 1)]

    # For every pair of indices
    for i in range(n):
        for j in range(n):

            # Check that slicing returns the correct list
            assert collection[i:j] == elements[i:j]
            assert collection[i : -(j + 1)] == elements[i : -(j + 1)]
            assert (
                collection[-(i + 1) : -(j + 1)]
                == elements[-(i + 1) : -(j + 1)]
            )


@pytest.mark.parametrize(
    "model, elements, elements_check",
    cartesian_product(
        PARAMETERS_MODELS_ORDERED_COLLECTIONS, PARAMETERS_ELEMENT_LISTS
    ),
)
def test_reversed(
    model: type,
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
):
    """Test ordered collections' __reversed__ operator."""

    # Create ordered collection
    collection = model(SimpleGraph(), elements=elements)

    # Reverse ordered collection
    collection_reversed = reversed(collection)

    # Make sure reversed collection is an iterable
    assert isinstance(collection_reversed, Iterable)

    # If ordered collection is empty
    if not elements:
        try:
            _ = next(collection_reversed)
            assert False
        except StopIteration:
            assert True

    # Otherwise
    else:
        # Check that reversed collection contains exactly all the elements,
        # in reverse order
        for i, element in enumerate(collection_reversed):
            assert element == elements[-(i + 1)]
        assert i == len(elements) - 1


@pytest.mark.parametrize(
    "model, elements_add, elements_add_check",
    cartesian_product(
        PARAMETERS_MODELS_ORDERED_COLLECTIONS, PARAMETERS_ELEMENT_LISTS
    ),
)
def test_setitem(
    model: type,
    elements_add: list[IRI | Literal | Any],
    elements_add_check: list[IRI | Literal],
) -> None:
    """Test ordered collections' __setitem__ operator."""

    # Create Collection object
    collection, elements, elements_check = build_collection(
        model, not_empty=True
    )

    # For every element of additional list
    n = len(collection)
    for element_add, element_add_check in zip(
        elements_add, elements_add_check
    ):

        # Pick an index at random
        i = rd.randint(-n, n - 1)

        # Set i-th element of ordered collection
        collection[i] = element_add

        # Set i-th element of lists
        elements[i] = element_add
        elements_check[i] = element_add_check

        # Check that ordered collection contains exactly all the elements
        check_elements_ordered_collection(collection, elements)

        # Check that the graph is correct after calling the method
        check_graph_collection(collection, elements_check)


@pytest.mark.parametrize(
    "model, element, element_check",
    cartesian_product(
        PARAMETERS_MODELS_ORDERED_COLLECTIONS, PARAMETERS_ELEMENTS
    ),
)
def test_append(
    model: type, element: IRI | Literal | Any, element_check: IRI | Literal
):
    """Test ordered collections' append() method."""

    # Create Collection object
    collection, elements, elements_check = build_collection(model)

    # Append element
    collection.append(element)

    # Append element to lists
    elements.append(element)
    elements_check.append(element_check)

    # Check that ordered collection contains exactly all the elements
    check_elements_ordered_collection(collection, elements)

    # Check that the graph is correct after calling the method
    check_graph_collection(collection, elements_check)


@pytest.mark.parametrize(
    "model, elements_add, elements_add_check, model_elements_add",
    cartesian_product(
        PARAMETERS_MODELS_ORDERED_COLLECTIONS,
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
    """Test ordered collections' extend() method."""

    # Create ordered collection
    collection, elements, elements_check = build_collection(model)

    # TODO: Find a better way, but otherwise too long
    if len(elements_add) > 20:
        elements_add_with_check = list(zip(elements_add, elements_add_check))
        elements_add_with_check = rd.sample(elements_add_with_check, 20)
        elements_add, elements_add_check = tuple(zip(*elements_add_with_check))
        elements_add = list(elements_add)
        elements_add_check = list(elements_add_check)

    # If a model is specified, create instance to initialize ordered collection
    # with
    if model_elements_add is not None:

        # If model is Alt and list of elements is not empty, expect warning
        with (
            pytest.warns(UserWarning)
            if model_elements_add == Alt and elements_add
            else nullcontext()
        ):
            elements_add = model_elements_add(
                SimpleGraph(), elements=elements_add
            )

    # Extend ordered collection
    collection.extend(elements_add)

    # Extend lists with additional elements
    elements += elements_add
    elements_check += elements_add_check

    # Check that ordered collection contains exactly all the elements
    check_elements_ordered_collection(collection, elements)

    # Check that the graph is correct after calling the method
    check_graph_collection(collection, elements_check)


@pytest.mark.parametrize(
    "model, elements, elements_check",
    cartesian_product(
        PARAMETERS_MODELS_ORDERED_COLLECTIONS, PARAMETERS_ELEMENT_LISTS
    ),
)
def test_index(
    model: type,
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
) -> None:
    """Test ordered collections' index() method."""

    # Create ordered collection
    collection = model(SimpleGraph(), elements=elements)

    # Shuffle element_list
    elements_with_check = list(zip(elements, elements_check))
    rd.shuffle(elements_with_check)

    # For every element
    for element, element_check in elements_with_check:

        # Find the index of element in list, if it contains it
        # Only consider exact matches (eg. 0 != 0.0 != False)
        index = index_exact_match(element_check, elements_check)

        # Check that the index returned is the same
        assert collection.index(element) == index


@pytest.mark.parametrize(
    "model, elements, elements_check",
    cartesian_product(
        PARAMETERS_MODELS_ORDERED_COLLECTIONS, PARAMETERS_ELEMENT_LISTS
    ),
)
def test_index_with_start(
    model: type,
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
) -> None:
    """
    Test ordered collections' index() method, while specifying a start index.
    """

    # Create ordered collection
    collection = model(SimpleGraph(), elements=elements)

    # Shuffle element_list
    elements_with_check = list(zip(elements, elements_check))
    rd.shuffle(elements_with_check)

    # For every element
    n = len(collection)
    for element, element_check in elements_with_check:

        # For every start index
        for i in range(-n, n):

            # Find the index of element in list, if it contains it
            # Only consider exact matches (eg. 0 != 0.0 != False)
            index = index_exact_match(element_check, elements_check, start=i)

            # If element could be found in element list
            if index is not None:
                # Check that the index returned is the same
                assert collection.index(element, start=i) == index

            # Otherwise
            else:
                # Make sure call to method raises a ValueError
                try:
                    _ = collection.index(element, start=i)
                    assert False
                except ValueError:
                    assert True


@pytest.mark.parametrize(
    "model, elements, elements_check",
    cartesian_product(
        PARAMETERS_MODELS_ORDERED_COLLECTIONS, PARAMETERS_ELEMENT_LISTS
    ),
)
def test_index_with_end(
    model: type,
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
) -> None:
    """
    Test ordered collections' index() method, while specifying an end index.
    """

    # Create ordered collection
    collection = model(SimpleGraph(), elements=elements)

    # Shuffle element_list
    elements_with_check = list(zip(elements, elements_check))
    rd.shuffle(elements_with_check)

    # For every element
    n = len(collection)
    for element, element_check in elements_with_check:

        # For every end index
        for i in range(-n, n):

            # Find the index of element in list, if it contains it
            # Only consider exact matches (eg. 0 != 0.0 != False)
            index = index_exact_match(element_check, elements_check, end=i)

            # If element could be found in element list
            if index is not None:
                # Check that the index returned is the same
                assert collection.index(element, end=i) == index

            # Otherwise
            else:
                # Make sure call to method raises a ValueError
                try:
                    _ = collection.index(element, end=i)
                    assert False
                except ValueError:
                    assert True


# TODO: Too long to run
@pytest.mark.parametrize(
    "model, elements, elements_check",
    cartesian_product(
        PARAMETERS_MODELS_ORDERED_COLLECTIONS, PARAMETERS_ELEMENT_LISTS
    ),
)
def test_index_with_start_and_end(
    model: type,
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
) -> None:
    """
    Test ordered collections' index() method,
    while specifying a start and an end indices.
    """

    # Create ordered collection
    collection = model(SimpleGraph(), elements=elements)

    # Shuffle element_list
    elements_with_check = list(zip(elements, elements_check))
    rd.shuffle(elements_with_check)

    # For every element
    n = len(collection)
    for element, element_check in elements_with_check:

        # For every start index
        for i in range(-n, n):

            # For every end index
            for j in range(-n, n):

                # Find the index of element in list, if it contains it
                # Only consider exact matches (eg. 0 != 0.0 != False)
                index = index_exact_match(
                    element_check, elements_check, start=i, end=j
                )

                # If element could be found in element list
                if index is not None:
                    # Check that the index returned is the same
                    assert collection.index(element, start=i, end=j) == index

                # Otherwise
                else:
                    # Make sure call to method raises a ValueError
                    try:
                        _ = collection.index(element, start=i, end=j)
                        assert False
                    except ValueError:
                        assert True


# TODO: Doesn't pass
@pytest.mark.parametrize(
    "model, elements_add, elements_add_check",
    cartesian_product(
        PARAMETERS_MODELS_ORDERED_COLLECTIONS, PARAMETERS_ELEMENT_LISTS
    ),
)
def test_insert(
    model: type,
    elements_add: list[IRI | Literal | Any],
    elements_add_check: list[IRI | Literal],
) -> None:
    """Test ordered collections' insert() method."""

    # Create ordered collection
    collection, elements, elements_check = build_collection(model)

    # For every element of additional list
    n = len(collection)
    for element_add, element_add_check in zip(
        elements_add, elements_add_check
    ):

        # Pick an index at random
        i = rd.randint(-n, n - 1) if n > 0 else 0

        # Set i-th element of ordered collection
        collection.insert(i, element_add)

        # Set i-th element of lists
        elements.insert(i, element_add)
        elements_check.insert(i, element_add_check)

        # Check that ordered collection contains exactly all the elements
        check_elements_ordered_collection(collection, elements)

        # Check that the graph is correct after calling the method
        check_graph_collection(collection, elements_check)

        # Increment n
        n += 1


@pytest.mark.parametrize(
    "model, elements, elements_check",
    cartesian_product(
        PARAMETERS_MODELS_ORDERED_COLLECTIONS, PARAMETERS_ELEMENT_LISTS
    ),
)
def test_pop(
    model: type,
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
):
    """Test ordered collections' pop() method."""

    # Create ordered collection
    collection = model(SimpleGraph(), elements=elements)

    # For every element
    n = len(elements)
    for i in range(n):

        # Get an index at random
        index = rd.randint(-n + i, n - i - 1)

        # Pop element at corresponding index
        element_popped = collection.pop(index)

        # Check that the popped element is the correct one
        element = elements.pop(index)
        del elements_check[index]
        assert element_popped == element

        # Check that ordered collection contains exactly all the elements
        check_elements_ordered_collection(collection, elements)

        # Check that the graph is correct after calling the method
        check_graph_collection(collection, elements_check)


@pytest.mark.parametrize(
    "model, elements, elements_check",
    cartesian_product(
        PARAMETERS_MODELS_ORDERED_COLLECTIONS, PARAMETERS_ELEMENT_LISTS
    ),
)
def test_reverse(
    model: type,
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
):
    """Test ordered collections' reverse() method."""

    # Create ordered collection
    collection = model(SimpleGraph(), elements=elements)

    # Reverse ordered collection
    collection.reverse()

    # Reverse element lists
    elements = list(reversed(elements))
    elements_check = list(reversed(elements_check))

    # Check that ordered collection contains exactly all the elements
    check_elements_ordered_collection(collection, elements)

    # Check that the graph is correct after calling the method
    check_graph_collection(collection, elements_check)


# TODO: Does not pass if no key specified (bc of element types not comparable)
@pytest.mark.parametrize(
    "model, elements, elements_check, key_function, reverse",
    cartesian_product(
        PARAMETERS_MODELS_ORDERED_COLLECTIONS,
        PARAMETERS_ELEMENT_LISTS,
        PARAMETERS_KEY_FUNCTIONS,
        [True, False],
    ),
)
def test_sort(
    model: type,
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
    key_function: Optional[Callable],
    reverse: bool,
):
    """Test ordered collections' sort() method."""

    # Create ordered collection
    collection = model(SimpleGraph(), elements=elements)

    # Sort ordered collection
    collection.sort(key=key_function, reverse=reverse)

    # If element lists are not empty
    if elements:

        # Necessary to have the same sorting behaviour
        def key(x):
            if key_function is None:
                return x[0]
            return key_function(x[0])

        # Sort element lists
        elements_with_check = sorted(
            zip(elements, elements_check), key=key, reverse=reverse
        )
        elements, elements_check = tuple(zip(*elements_with_check))

    # Check that ordered collection contains exactly all the elements
    check_elements_ordered_collection(collection, elements)

    # Check that the graph is correct after calling the method
    check_graph_collection(collection, elements_check)
