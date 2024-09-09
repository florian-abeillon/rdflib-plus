"""Test Seq's methods"""

import copy
import random as rd
from typing import Any, Optional

import pytest
from rdflib import RDF, Literal
from rdflib import URIRef as IRI

from rdflib_plus import Alt, Bag, List, Seq
from tests.parameters import (
    PARAMETERS_ELEMENT_LISTS,
    PARAMETERS_ELEMENTS,
    PARAMETERS_PROPERTIES_CONTAINER,
)
from tests.tests_methods.utils import (
    build_collection,
    check_elements,
    get_another_parameter,
    index_exact_match,
)
from tests.utils import (
    cartesian_product,
    check_rem_add,
    parse_element_list_with_check,
)


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
    """Test Seq' elements setter."""

    # Parse lists of elements with check
    element_list_before, element_list_check_before = (
        parse_element_list_with_check(element_list_with_check_before)
    )
    element_list_after, element_list_check_after = (
        parse_element_list_with_check(element_list_with_check_after)
    )

    # Create Seq
    seq = build_collection(Seq, element_list=element_list_before)

    # Freeze the state of the graph before calling the method
    graph_before = copy.deepcopy(seq.graph)

    # Set elements property
    seq.elements = element_list_after

    # Check that collection appropriately contains all the elements of Seq
    check_elements(seq, element_list_after)

    # Prepare the removed and additional triples
    triples_rem = [
        (seq.iri, RDF[f"_{i + 1}"], element_check_before)
        for i, element_check_before in enumerate(element_list_check_before)
    ]
    triples_add = [
        (seq.iri, RDF[f"_{i + 1}"], element_check_after)
        for i, element_check_after in enumerate(element_list_check_after)
    ]

    # Check the correctness of the removed and additional triples
    check_rem_add(graph_before, seq.graph, triples_rem, triples_add)


@pytest.mark.parametrize("element_list_with_check", PARAMETERS_ELEMENT_LISTS)
def test_delitem(
    element_list_with_check: list[tuple[IRI | Literal | Any, IRI | Literal]]
):
    """Test Seq's __delitem__ operator."""

    # Parse list of elements with check
    element_list, element_list_check = parse_element_list_with_check(
        element_list_with_check
    )

    # Create Seq
    seq = build_collection(Seq, element_list=element_list)

    n = len(element_list)
    for i in range(n):

        # Freeze the state of the graph before calling the method
        graph_before = copy.deepcopy(seq.graph)

        # Get an index at random
        index = rd.randint(0, n - i - 1)

        # Remove element corresponding to this index
        del seq[index]

        # Prepare removed and additional triples
        triples_rem = [
            (seq.iri, RDF[f"_{i + index + 1}"], el)
            for i, el in enumerate(element_list_check[index:])
        ]
        triples_add = [
            (seq.iri, RDF[f"_{i + index + 1}"], el)
            for i, el in enumerate(element_list_check[index + 1 :])
        ]

        # Check that collection appropriately contains all the remaining
        # elements of list
        check_elements(seq, element_list)

        # Check the correctness of the removed and additional triples
        check_rem_add(graph_before, seq.graph, triples_rem, triples_add)

        # Remove element from lists
        del element_list[index]
        del element_list_check[index]


@pytest.mark.parametrize("element_list_with_check", PARAMETERS_ELEMENT_LISTS)
def test_reversed(
    element_list_with_check: list[tuple[IRI | Literal | Any, IRI | Literal]]
):
    """Test Seq's __reversed__ operator."""

    # Parse list of elements with check
    element_list, element_list_check = parse_element_list_with_check(
        element_list_with_check
    )

    # Create Seq
    seq = build_collection(Seq, element_list=element_list)

    # Freeze the state of the graph before calling the method
    graph_before = copy.deepcopy(seq.graph)

    # Reverse object
    seq_reversed = reversed(seq)

    # Check that collection appropriately contains all the remaining
    # elements of list
    check_elements(seq_reversed, list(reversed(element_list)))

    # Prepare removed and additional triples
    triples_rem = [
        (seq.iri, RDF[f"_{i + 1}"], el)
        for i, el in enumerate(element_list_check)
    ]
    triples_add = [
        (seq.iri, RDF[f"_{i + 1}"], el)
        for i, el in enumerate(reversed(element_list_check))
    ]

    # Check the correctness of the removed and additional triples
    check_rem_add(graph_before, seq.graph, triples_rem, triples_add)


@pytest.mark.parametrize(
    "element_list_with_check_before, element_list_with_check_after",
    cartesian_product(
        PARAMETERS_ELEMENT_LISTS,
        PARAMETERS_ELEMENT_LISTS,
    ),
)
def test_setitem(
    element_list_with_check_before: list[
        tuple[IRI | Literal | Any, IRI | Literal]
    ],
    element_list_with_check_after: list[
        tuple[IRI | Literal | Any, IRI | Literal]
    ],
):
    """Test Seq's __setitem__ operator."""

    # Parse lists of elements with check
    element_list_before, element_list_check_before = (
        parse_element_list_with_check(element_list_with_check_before)
    )

    # Create Seq
    seq = build_collection(Seq, element_list=element_list_before)

    n = len(element_list_before)
    for element_after, element_check_after in element_list_with_check_after:

        # Pick an index at random
        i = rd.randint(0, n - 1)

        # Freeze the state of the graph before calling the operator
        graph_before = copy.deepcopy(seq.graph)

        # Set i-th element
        seq[i] = element_after

        # Prepare removed and additional triples
        triples_rem = [
            (seq.iri, RDF[f"_{i + 1}"], element_list_check_before[i])
        ]
        triples_add = [(seq.iri, RDF[f"_{i + 1}"], element_check_after)]

        # Check the correctness of the removed and additional triples
        check_rem_add(graph_before, seq.graph, triples_rem, triples_add)

        # Check that seq's elements was correctly changed
        element_list_check_before[i] = element_check_after
        check_elements(seq, element_list_check_before)


@pytest.mark.parametrize("element_with_check", PARAMETERS_ELEMENTS)
def test_append(element_with_check: tuple[IRI | Literal | Any, IRI | Literal]):
    """Test Seq's append() method."""

    # Parse element with check
    element, element_check = element_with_check

    # Create Seq
    seq = build_collection(Seq)

    # Keep elements in memory
    seq_elements_before = copy.deepcopy(seq.elements)

    # Freeze the state of the graph before calling the method
    graph_before = copy.deepcopy(seq.graph)

    # Append element
    seq.append(element)

    # Prepare removed and additional triples
    index = len(seq_elements_before)
    triples_rem = []
    triples_add = [(seq.iri, RDF[f"_{index + 1}"], element_check)]

    # Check the correctness of the removed and additional triples
    check_rem_add(graph_before, seq.graph, triples_rem, triples_add)

    # Check that collection appropriately contains all the elements of list
    # plus element
    check_elements(seq, seq_elements_before + [element])


@pytest.mark.parametrize("element_list_with_check", PARAMETERS_ELEMENT_LISTS)
def test_clear(
    element_list_with_check: list[tuple[IRI | Literal | Any, IRI | Literal]]
):
    """Test Seq's clear() method."""

    # Parse list of elements with check
    element_list, element_list_check = parse_element_list_with_check(
        element_list_with_check
    )

    # Create Seq
    seq = build_collection(Seq, element_list=element_list)

    # Freeze the state of the graph before calling the method
    graph_before = copy.deepcopy(seq.graph)

    # Clear List
    seq.clear()

    # Check that element list is empty
    assert seq.elements == []

    # Prepare the removed and additional triples
    triples_rem = [
        (seq.iri, RDF[f"_{i + 1}"], element_check)
        for i, element_check in enumerate(element_list_check)
    ]
    triples_add = []

    # Check the correctness of the removed and additional triples
    check_rem_add(graph_before, seq.graph, triples_rem, triples_add)


@pytest.mark.parametrize("element_list_with_check", PARAMETERS_ELEMENT_LISTS)
def test_copy(
    element_list_with_check: list[tuple[IRI | Literal | Any, IRI | Literal]]
):
    """Test Seq's copy() method."""

    # Parse list of elements with check
    element_list, element_list_check = parse_element_list_with_check(
        element_list_with_check
    )

    # Create Seq
    seq = build_collection(Seq, element_list=element_list)

    # Freeze the state of the graph before calling the method
    graph_before = copy.deepcopy(seq.graph)

    # Copy Seq
    seq_new = seq.copy()

    # Check that the copied Seq is of the correct type
    assert isinstance(seq_new, Seq)
    # Check that the copied Seq has the same elements
    assert seq_new.elements == seq.elements
    # Check that the copied Seq has the same properties
    for property_ in PARAMETERS_PROPERTIES_CONTAINER:
        if hasattr(seq, property_):
            assert getattr(seq, property_) == getattr(seq_new, property_)
        else:
            assert not hasattr(seq_new, property_)

    # Prepare the removed and additional triples
    triples_rem = []
    triples_add = [(seq_new.iri, RDF.type, RDF.Seq)]
    triples_add.extend(
        [
            (seq_new.iri, RDF[f"_{i + 1}"], element_check)
            for i, element_check in enumerate(element_list_check)
        ]
    )

    # Check the correctness of the removed and additional triples
    check_rem_add(graph_before, seq.graph, triples_rem, triples_add)


@pytest.mark.parametrize("element_list_with_check", PARAMETERS_ELEMENT_LISTS)
def test_discard_element(
    element_list_with_check: list[tuple[IRI | Literal | Any, IRI | Literal]]
):
    """Test Seq's discard_element() method."""

    # Parse list of elements with check
    element_list, element_list_check = parse_element_list_with_check(
        element_list_with_check
    )

    # Create Seq
    seq = build_collection(Seq, element_list=element_list)

    # Create an extended list from the original and another one, that contains
    # different elements, and shuffle it
    element_set = set(element_list_with_check)
    element_list_with_check_extended = (
        element_list_with_check
        + get_another_parameter(
            PARAMETERS_ELEMENT_LISTS,
            key=lambda new_parameter: new_parameter
            and set(new_parameter) != element_set,
        )
    )
    rd.shuffle(element_list_with_check_extended)

    # For every element of the extended list
    for element, element_check in element_list_with_check_extended:

        # Freeze the state of the graph before calling the method
        graph_before = copy.deepcopy(seq.graph)

        # Discard element from object
        seq.discard_element(element)

        # Initialize removed and additional triples
        triples_rem = []
        triples_add = []

        # Find the index of element in list, if it contains it
        # Only consider exact matches (eg. 0 != 0.0 != False)
        index = index_exact_match(element, element_list)

        # If element is in Seq
        if index is not None:

            # Prepare removed and additional triples
            triples_rem = [
                (seq.iri, RDF[f"_{i + index + 1}"], el)
                for i, el in enumerate(element_list_check[index:])
            ]
            triples_add = [
                (seq.iri, RDF[f"_{i + index + 1}"], el)
                for i, el in enumerate(element_list_check[index + 1 :])
            ]

            # Remove element from lists
            del element_list[index]
            del element_list_check[index]

        # Check that collection appropriately contains all the remaining
        # elements of list
        check_elements(seq, element_list)

        # Check the correctness of the removed and additional triples
        check_rem_add(graph_before, seq.graph, triples_rem, triples_add)


# TODO: Adapt for Alt and Bag
@pytest.mark.parametrize(
    "element_list_with_check, model",
    cartesian_product(
        PARAMETERS_ELEMENT_LISTS,
        [None, List, Seq],
        # PARAMETERS_ELEMENT_LISTS, [None, Alt, Bag, List, Seq]
    ),
)
def test_extend(
    element_list_with_check: list[tuple[IRI | Literal | Any, IRI | Literal]],
    model: Optional[type],
):
    """Test Seq's extend() method."""

    # Parse list of elements with check
    element_list, element_list_check = parse_element_list_with_check(
        element_list_with_check
    )

    # Create Seq
    seq = build_collection(Seq)

    # Freeze the state of the graph before calling the method
    graph_before = copy.deepcopy(seq.graph)

    # Keep elements in memory
    set_elements_before = copy.deepcopy(seq.elements)

    # Extend Seq
    if model is not None:
        collection = build_collection(
            model,
            element_list=element_list,
        )
        seq.extend(collection)
    else:
        seq.extend(element_list)

    # Check that Seq appropriately contains all the elements of the two lists
    check_elements(seq, set_elements_before + element_list)

    # Prepare removed and additional triples
    triples_rem = []
    triples_add = [
        (seq.iri, RDF[f"_{i + len(set_elements_before) + 1}"], element_check)
        for i, element_check in enumerate(element_list_check)
    ]

    # Check the correctness of the removed and additional triples
    check_rem_add(graph_before, seq.graph, triples_rem, triples_add)


@pytest.mark.parametrize("element_list_with_check", PARAMETERS_ELEMENT_LISTS)
def test_remove_element(
    element_list_with_check: list[tuple[IRI | Literal | Any, IRI | Literal]]
):
    """Test Seq's remove_element() method."""

    # Parse list of elements with check
    element_list, element_list_check = parse_element_list_with_check(
        element_list_with_check
    )

    # Create Seq
    seq = build_collection(Seq, element_list=element_list)

    # Create an extended list from the original and another one, that contains
    # different elements, and shuffle it
    element_set = set(element_list_with_check)
    element_list_with_check_extended = (
        element_list_with_check
        + get_another_parameter(
            PARAMETERS_ELEMENT_LISTS,
            key=lambda new_parameter: new_parameter
            and set(new_parameter) != element_set,
        )
    )
    rd.shuffle(element_list_with_check_extended)

    # For every element of the extended list
    for element, element_check in element_list_with_check_extended:

        # Freeze the state of the graph before calling the method
        graph_before = copy.deepcopy(seq.graph)

        # Initialize removed and additional triples
        triples_rem = []
        triples_add = []

        # Find the index of element in list, if it contains it
        # Only consider exact matches (eg. 0 != 0.0 != False)
        index = index_exact_match(element, element_list)

        # If element is not in List
        if index is None:

            # Try to remove element from object
            try:
                seq.remove_element(element)
            except ValueError:
                pass

        # Otherwise, if element is in List
        else:

            # Remove element from object
            seq.remove_element(element)

            # Prepare removed and additional triples
            triples_rem = [
                (seq.iri, RDF[f"_{i + index + 1}"], el)
                for i, el in enumerate(element_list_check[index:])
            ]
            triples_add = [
                (seq.iri, RDF[f"_{i + index + 1}"], el)
                for i, el in enumerate(element_list_check[index + 1 :])
            ]

            # Remove element from lists
            del element_list[index]
            del element_list_check[index]

        # Check that collection appropriately contains all the remaining
        # elements of list
        check_elements(seq, element_list)

        # Check the correctness of the removed and additional triples
        check_rem_add(graph_before, seq.graph, triples_rem, triples_add)


# @pytest.mark.parametrize(
#     "model, model_name, model_type, properties, element_list",
#     cartesian_product(
#         [PARAMETERS_LIST, PARAMETERS_SEQ], PARAMETERS_ELEMENT_LISTS
#     ),
# )
# def test_insert(
#     model: type,
#     model_name: str,
#     model_type: IRI,
#     properties: set[IRI],
#     element_list: list[IRI | Literal | Any],
# ):
#     """Test List and Seq's insert() method."""

#     # Create List or Seq
#     collection = build_collection(model)

#     # Keep elements in memory
#     collection_elements_before = copy.deepcopy(collection.elements)

#     # For every element
#     for element in element_list:
#         # Get an index at random
#         index = rd.randint(0, len(collection))

#         # Insert element at the index that was just picked
#         collection.insert(index, element)

#         # Check that the element was indeed popped
#         collection_elements_before.insert(index, element)
#         assert collection.elements == collection_elements_before


# @pytest.mark.parametrize(
#     "model, model_name, model_type, properties, element_list",
#     cartesian_product(
#         [PARAMETERS_LIST, PARAMETERS_SEQ], PARAMETERS_ELEMENT_LISTS
#     ),
# )
# def test_pop(
#     model: type,
#     model_name: str,
#     model_type: IRI,
#     properties: set[IRI],
#     element_list: list[IRI | Literal | Any],
# ):
#     """Test List and Seq's pop() method."""

#     # Create List or Seq
#     collection = build_collection(model, element_list=element_list)

#     # For every element
#     n = len(element_list)
#     for i in range(n):
#         # Get an index at random
#         index = rd.randint(0, n - i - 1)

#         # Pop element corresponding at index
#         element_collection = collection.pop(index)

#         # Check that the element popped is the correct one
#         element = element_list.pop(index)
#         assert element_collection == element
#         # Check that the element was indeed popped
#         assert collection.elements == element_list


# @pytest.mark.parametrize(
#     "model, model_name, model_type, properties, element_list, key_function, "
#     "reverse",
#     cartesian_product(
#         [PARAMETERS_LIST, PARAMETERS_SEQ],
#         PARAMETERS_ELEMENT_LISTS,
#         [None] + PARAMETERS_KEY_FUNCTIONS,
#         [True, False],
#     ),
# )
# def test_sort(
#     model: type,
#     model_name: str,
#     model_type: IRI,
#     properties: set[IRI],
#     element_list: list[IRI | Literal | Any],
#     key_function: Optional[Callable],
#     reverse: bool,
# ):
#     """Test List and Seq's sort() method."""

#     # Create List or Seq
#     collection = build_collection(model, element_list=element_list)

#     # Reverse object
#     collection.sort(key=key_function, reverse=reverse)

#     # Check that elements were sorted
#     assert collection.elements == sorted(
#         element_list, key=key_function, reverse=reverse
#     )


# @pytest.mark.parametrize(
#     "model, model_name, model_type, properties, element_list",
#     cartesian_product(
#         [PARAMETERS_LIST, PARAMETERS_SEQ], PARAMETERS_ELEMENT_LISTS
#     ),
# )
# def test_reverse(
#     model: type,
#     model_name: str,
#     model_type: IRI,
#     properties: set[IRI],
#     element_list: list[IRI | Literal | Any],
# ):
#     """Test List and Seq's reverse() method."""

#     # Create List or Seq
#     collection = build_collection(model, element_list=element_list)

#     # Reverse object
#     collection.reverse()

#     # Check that elements were reversed
#     assert collection.elements == list(reversed(element_list))
