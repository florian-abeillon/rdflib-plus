"""Test List's methods"""

import copy
import random as rd
from typing import Any, Optional

import pytest
from rdflib import RDF, Literal
from rdflib import URIRef as IRI

from rdflib_plus import Alt, Bag, List, Seq
from tests.parameters import (
    PARAMETERS_ELEMENT_LISTS,
    PARAMETERS_PROPERTIES_LIST,
)
from tests.tests_methods.utils import (
    build_collection,
    check_elements,
    get_another_parameter,
)
from tests.utils import (
    SEED,
    cartesian_product,
    check_rem_add,
    parse_element_list_with_check,
    prepare_list_triples_for_check,
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
    """Test List' elements setter."""

    # Parse lists of elements with check
    element_list_before, element_list_check_before = (
        parse_element_list_with_check(element_list_with_check_before)
    )
    element_list_after, element_list_check_after = (
        parse_element_list_with_check(element_list_with_check_after)
    )

    # Create List
    list_ = build_collection(List, element_list=element_list_before)

    # Freeze the state of the graph before calling the method
    graph_before = copy.deepcopy(list_.graph)
    graph_after = list_.graph

    # Set elements property
    list_.elements = element_list_after

    # Check that collection appropriately contains all the elements of list
    check_elements(list_, element_list_after)

    # Prepare the removed and additional triples
    triples_rem = prepare_list_triples_for_check(
        list_.iri, element_list_check_before, graph_before
    )
    triples_add = prepare_list_triples_for_check(
        list_.iri, element_list_check_after, graph_after
    )

    # If the first element is the same in both lists
    if (
        element_list_before
        and element_list_after
        and element_list_check_before[0] == element_list_check_after[0]
    ):
        # Check that the first removed and additional triples are the same
        assert (
            triples_rem[0]
            == triples_add[0]
            == (list_.iri, RDF.first, element_list_check_before[0])
        )

        # Remove this first triple from both lists
        triples_rem = triples_rem[1:]
        triples_add = triples_add[1:]

    # Check the correctness of the removed and additional triples
    check_rem_add(graph_before, graph_after, triples_rem, triples_add)


@pytest.mark.parametrize("element_list_with_check", PARAMETERS_ELEMENT_LISTS)
def test_clear(
    element_list_with_check: list[tuple[IRI | Literal | Any, IRI | Literal]]
):
    """Test List's clear() method."""

    # Parse list of elements with check
    element_list, element_list_check = parse_element_list_with_check(
        element_list_with_check
    )

    # Create List
    list_ = build_collection(List, element_list=element_list)

    # Freeze the state of the graph before calling the method
    graph_before = copy.deepcopy(list_.graph)

    # Clear List
    list_.clear()

    # Check that element list is empty
    assert list_.elements == []

    # Prepare the removed and additional triples
    triples_rem = prepare_list_triples_for_check(
        list_.iri, element_list_check, graph_before
    )
    triples_add = []

    # Check the correctness of the removed and additional triples
    check_rem_add(graph_before, list_.graph, triples_rem, triples_add)


@pytest.mark.parametrize("element_list_with_check", PARAMETERS_ELEMENT_LISTS)
def test_copy(
    element_list_with_check: list[tuple[IRI | Literal | Any, IRI | Literal]]
):
    """Test List's copy() method."""

    # Parse list of elements with check
    element_list, element_list_check = parse_element_list_with_check(
        element_list_with_check
    )

    # Create List
    list_ = build_collection(List, element_list=element_list)

    # Freeze the state of the graph before calling the method
    graph_before = copy.deepcopy(list_.graph)
    graph_after = list_.graph

    # Copy List
    list_new = list_.copy()

    # Check that the copied List is of the correct type
    assert isinstance(list_new, List)
    # Check that the copied List has the same elements
    assert list_new.elements == list_.elements
    # Check that the copied List has the same properties
    for property_ in PARAMETERS_PROPERTIES_LIST:
        if hasattr(list_, property_):
            assert getattr(list_, property_) == getattr(list_new, property_)
        else:
            assert not hasattr(list_new, property_)

    # Prepare the removed and additional triples
    triples_rem = []
    triples_add = [(list_new.iri, RDF.type, RDF.List)]
    triples_add.extend(
        prepare_list_triples_for_check(
            list_new.iri, element_list_check, graph_after
        )
    )

    # Check the correctness of the removed and additional triples
    check_rem_add(graph_before, graph_after, triples_rem, triples_add)


@pytest.mark.parametrize("element_list_with_check", PARAMETERS_ELEMENT_LISTS)
def test_discard_element(
    element_list_with_check: list[tuple[IRI | Literal | Any, IRI | Literal]]
):
    """Test List's discard_element() method."""

    # Parse list of elements with check
    element_list, element_list_check = parse_element_list_with_check(
        element_list_with_check
    )

    # Create List
    list_ = build_collection(List, element_list=element_list)

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
        graph_before = copy.deepcopy(list_.graph)
        # Freeze the IRI of List (as it may change, if its first element gets
        # removed)
        list_iri = list_.iri

        # Discard element from object
        list_.discard_element(element)

        # Initialize removed and additional triples
        triples_rem = []
        triples_add = []

        # Find the index of element in list, if it contains it
        # Only consider exact matches (eg. 0 != 0.0 != False)
        index = None
        for i, el in enumerate(element_list):
            if (
                element == el
                and isinstance(element, type(el))
                and isinstance(el, type(element))
            ):
                index = i
                break

        # If element is in List
        if index is not None:

            # If element is the first element of list
            if index == 0:
                next_sublist = graph_before.value(list_iri, RDF.rest)

                # Prepare removed and additional triples
                triples_rem = [
                    (list_iri, RDF.type, RDF.List),
                    (list_iri, RDF.first, element_check),
                    (list_iri, RDF.rest, next_sublist),
                ]
                triples_add = []

            # Otherwise
            else:
                # Get the sublist just before the one corresponding to element
                sublist = list_iri
                for _ in range(index - 1):
                    sublist = graph_before.value(sublist, RDF.rest)

                # Get the sublist corresponding to element, as well as the one
                # just before and just after
                prev_sublist = sublist
                sublist = graph_before.value(prev_sublist, RDF.rest)
                next_sublist = graph_before.value(sublist, RDF.rest)

                # Prepare removed and additional triples
                triples_rem = [
                    (prev_sublist, RDF.rest, sublist),
                    (sublist, RDF.type, RDF.List),
                    (sublist, RDF.first, element_check),
                    (sublist, RDF.rest, next_sublist),
                ]
                triples_add = [(prev_sublist, RDF.rest, next_sublist)]

            # Remove element from element_list
            del element_list[index]

        # Check that collection appropriately contains all the remaining
        # elements of list
        check_elements(list_, element_list)

        # Check the correctness of the removed and additional triples
        check_rem_add(graph_before, list_.graph, triples_rem, triples_add)


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
    """Test List's extend() method."""

    # Parse list of elements with check
    element_list, element_list_check = parse_element_list_with_check(
        element_list_with_check
    )

    # Create List
    list_ = build_collection(List)

    # Freeze the state of the graph before calling the method
    graph_before = copy.deepcopy(list_.graph)
    graph_after = list_.graph

    # Keep elements in memory
    list_elements_before = copy.deepcopy(list_.elements)

    # Extend List
    if model is not None:
        collection = build_collection(
            model,
            element_list=element_list,
        )
        list_.extend(collection)
    else:
        list_.extend(element_list)

    # Check that List appropriately contains all the elements of the two lists
    check_elements(list_, list_elements_before + element_list)

    # Initialize removed and additional triples
    triples_rem = []
    triples_add = []

    # If List was indeed extended with additional elements
    if element_list:

        # If List was not empty before
        if list_elements_before:

            # Get the last sublist
            last_sublist = list_.iri
            for _ in range(len(list_elements_before) - 1):
                last_sublist = graph_before.value(last_sublist, RDF.rest)

            # Get the first additional sublist
            new_sublist = graph_after.value(last_sublist, RDF.rest)

            # Prepare the removed triple
            triples_rem = [(last_sublist, RDF.rest, RDF.nil)]

            # Prepare the additional triples
            triples_add = [
                (last_sublist, RDF.rest, new_sublist),
                (new_sublist, RDF.type, RDF.List),
            ]

        else:
            new_sublist = list_.iri

        triples_add.extend(
            prepare_list_triples_for_check(
                new_sublist, element_list_check, graph_after
            )
        )

    # Check the correctness of the removed and additional triples
    check_rem_add(graph_before, graph_after, triples_rem, triples_add)


@pytest.mark.parametrize("element_list_with_check", PARAMETERS_ELEMENT_LISTS)
def test_remove_element(
    element_list_with_check: list[tuple[IRI | Literal | Any, IRI | Literal]]
):
    """Test List's remove_element() method."""

    # Parse list of elements with check
    element_list, element_list_check = parse_element_list_with_check(
        element_list_with_check
    )

    # Create List
    list_ = build_collection(List, element_list=element_list)

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
        graph_before = copy.deepcopy(list_.graph)
        # Freeze the IRI of List (as it may change, if its first element gets
        # removed)
        list_iri = list_.iri

        # Initialize removed and additional triples
        triples_rem = []
        triples_add = []

        # Find the index of element in list, if it contains it
        # Only consider exact matches (eg. 0 != 0.0 != False)
        index = None
        for i, el in enumerate(element_list):
            if (
                element == el
                and isinstance(element, type(el))
                and isinstance(el, type(element))
            ):
                index = i
                break

        # If element is not in List
        if index is None:

            # Try to remove element from object
            try:
                list_.remove_element(element)
            except ValueError:
                pass

        # Otherwise, if element is in List
        else:

            # Remove element from object
            list_.remove_element(element)

            # If element is the first element of list
            if index == 0:
                next_sublist = graph_before.value(list_iri, RDF.rest)

                # Prepare removed and additional triples
                triples_rem = [
                    (list_iri, RDF.type, RDF.List),
                    (list_iri, RDF.first, element_check),
                    (list_iri, RDF.rest, next_sublist),
                ]
                triples_add = []

            # Otherwise
            else:
                # Get the sublist just before the one corresponding to element
                sublist = list_iri
                for _ in range(index - 1):
                    sublist = graph_before.value(sublist, RDF.rest)

                # Get the sublist corresponding to element, as well as the one
                # just before and just after
                prev_sublist = sublist
                sublist = graph_before.value(prev_sublist, RDF.rest)
                next_sublist = graph_before.value(sublist, RDF.rest)

                # Prepare removed and additional triples
                triples_rem = [
                    (prev_sublist, RDF.rest, sublist),
                    (sublist, RDF.type, RDF.List),
                    (sublist, RDF.first, element_check),
                    (sublist, RDF.rest, next_sublist),
                ]
                triples_add = [(prev_sublist, RDF.rest, next_sublist)]

            # Remove element from element_list
            del element_list[index]

        # Check that collection appropriately contains all the remaining
        # elements of list
        check_elements(list_, element_list)

        # Check the correctness of the removed and additional triples
        check_rem_add(graph_before, list_.graph, triples_rem, triples_add)
