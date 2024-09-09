"""Test Bag's methods"""

import copy
import random as rd
from typing import Any, Optional

import pytest
from rdflib import RDF, Literal
from rdflib import URIRef as IRI

from rdflib_plus import Bag, List, Seq
from tests.parameters import (
    PARAMETERS_ELEMENT_LISTS,
    PARAMETERS_ELEMENTS,
    PARAMETERS_PROPERTIES_CONTAINER,
)
from tests.tests_methods.utils import (
    build_collection,
    check_elements,
    check_rem_add,
    get_another_parameter,
    index_exact_match,
)
from tests.utils import (
    cartesian_product,
    check_graph_diff_unordered_collection,
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
    """Test Bag' elements setter."""

    # Parse lists of elements with check
    element_list_before, element_list_check_before = (
        parse_element_list_with_check(element_list_with_check_before)
    )
    element_list_after, element_list_check_after = (
        parse_element_list_with_check(element_list_with_check_after)
    )

    # Create Bag
    bag = build_collection(Bag, element_list=element_list_before)

    # Freeze the state of the graph before calling the method
    graph_before = copy.deepcopy(bag.graph)

    # Set elements property
    bag.elements = element_list_after

    # Check that collection appropriately contains all the elements of Bag
    check_elements(bag, element_list_after)

    # Prepare the removed and additional predicates
    predicates_rem = [
        RDF[f"_{i + 1}"] for i in range(len(element_list_check_before))
    ]
    predicates_add = [
        RDF[f"_{i + 1}"] for i in range(len(element_list_check_after))
    ]

    # Check that the removed and additional predicates and objects are correct
    check_graph_diff_unordered_collection(
        graph_before,
        bag.graph,
        bag.iri,
        predicates_rem,
        predicates_add,
        element_list_check_before,
        element_list_check_after,
    )


@pytest.mark.parametrize("element_with_check", PARAMETERS_ELEMENTS)
def test_add_element(
    element_with_check: tuple[IRI | Literal | Any, IRI | Literal]
):
    """Test Bag's add_element() method."""

    # Parse list of elements with check
    element, element_check = element_with_check

    # Arbitrarily select list of elements, and create Bag
    bag = build_collection(Bag)

    # Freeze the state of the graph before calling the method
    graph_before = copy.deepcopy(bag.graph)

    # Keep elements in memory
    bag_elements_before = copy.deepcopy(bag.elements)
    bag_elements_after = bag_elements_before + [element]

    # Add element
    bag.add_element(element)

    # Check that there are as many elements in Collection object as in list
    assert len(bag.elements) == len(bag_elements_before) + 1
    # Check that all elements in list also appear in Collection
    assert all(element in bag.elements for element in bag_elements_after)

    # TODO: Wrong test, as it doesn't account for the unordered nature of Bag
    # Prepare the removed and additional predicates
    triples_rem = []
    triples_add = [
        (bag.iri, RDF[f"_{len(bag_elements_after)}"], element_check)
    ]

    # Check the correctness of the removed and additional triples
    check_rem_add(graph_before, bag.graph, triples_rem, triples_add)

    # # Prepare the removed and additional predicates
    # predicates_rem = [
    #     RDF[f"_{i + 1}"] for i in range(len(bag_elements_before))
    # ]
    # predicates_add = [RDF[f"_{i + 1}"] for i in range(len(bag_elements_after))]

    # # Check that the removed and additional predicates and objects are correct
    # check_rem_add_unordered(
    #     graph_before,
    #     bag.graph,
    #     bag.iri,
    #     predicates_rem,
    #     predicates_add,
    #     bag_elements_before,
    #     bag_elements_after,
    # )


@pytest.mark.parametrize("element_list", PARAMETERS_ELEMENT_LISTS)
def test_any(
    element_list_with_check: list[tuple[IRI | Literal | Any, IRI | Literal]]
):
    """Test Bag's any() method."""

    # Parse list of elements with check
    element_list, element_list_check = parse_element_list_with_check(
        element_list_with_check
    )

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


@pytest.mark.parametrize("element_list_with_check", PARAMETERS_ELEMENT_LISTS)
def test_clear(
    element_list_with_check: list[tuple[IRI | Literal | Any, IRI | Literal]]
):
    """Test Bag's clear() method."""

    # Parse list of elements with check
    element_list, element_list_check = parse_element_list_with_check(
        element_list_with_check
    )

    # Create Bag
    bag = build_collection(Bag, element_list=element_list)

    # Freeze the state of the graph before calling the method
    graph_before = copy.deepcopy(bag.graph)

    # Clear List
    bag.clear()

    # Check that element list is empty
    assert bag.elements == []

    # Prepare the removed and additional predicates
    predicates_rem = [RDF[f"_{i + 1}"] for i in range(len(element_list))]
    predicates_add = []

    # Check that the removed and additional predicates and objects are correct
    check_graph_diff_unordered_collection(
        graph_before,
        bag.graph,
        bag.iri,
        predicates_rem,
        predicates_add,
        element_list_check,
        [],
    )


@pytest.mark.parametrize("element_list_with_check", PARAMETERS_ELEMENT_LISTS)
def test_copy(
    element_list_with_check: list[tuple[IRI | Literal | Any, IRI | Literal]]
):
    """Test Bag's copy() method."""

    # Parse list of elements with check
    element_list, element_list_check = parse_element_list_with_check(
        element_list_with_check
    )

    # Create Bag
    bag = build_collection(Bag, element_list=element_list)

    # Freeze the state of the graph before calling the method
    graph_before = copy.deepcopy(bag.graph)

    # Copy Bag
    bag_new = bag.copy()

    # Check that the copied Bag is of the correct type
    assert isinstance(bag_new, Bag)
    # Check that the copied Bag has the same elements
    assert bag_new.elements == bag.elements
    # Check that the copied Bag has the same properties
    for property_ in PARAMETERS_PROPERTIES_CONTAINER:
        if hasattr(bag, property_):
            assert getattr(bag, property_) == getattr(bag_new, property_)
        else:
            assert not hasattr(bag_new, property_)

    # Prepare the removed and additional predicates
    predicates_rem = []
    predicates_add = [RDF[f"_{i + 1}"] for i in range(len(element_list))]

    # Check that the removed and additional predicates and objects are correct
    check_graph_diff_unordered_collection(
        graph_before,
        bag.graph,
        bag_new.iri,
        predicates_rem,
        predicates_add,
        [],
        element_list_check,
        triples_add=[(bag_new.iri, RDF.type, RDF.Bag)],
    )


@pytest.mark.parametrize("element_list_with_check", PARAMETERS_ELEMENTS)
def test_discard_element(
    element_list_with_check: list[tuple[IRI | Literal | Any, IRI | Literal]]
):
    """Test Bag's discard_element() method."""

    # Parse list of elements with check
    element_list, element_list_check = parse_element_list_with_check(
        element_list_with_check
    )

    # Create Bag
    bag = build_collection(Bag, element_list=element_list)

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
        graph_before = copy.deepcopy(bag.graph)

        # Discard element from object
        bag.discard_element(element)

        # Initialize removed and additional predicates and objects
        predicates_rem = []
        predicates_add = []
        objects_rem = copy.deepcopy(element_list_check)
        objects_add = copy.deepcopy(element_list_check)

        # Find the index of element in list, if it contains it
        # Only consider exact matches (eg. 0 != 0.0 != False)
        index = index_exact_match(element, element_list)

        # If element is in Bag
        if index is not None:

            # Prepare the removed and additional predicates
            predicates_rem = [
                RDF[f"_{i + 1}"] for i in range(len(element_list))
            ]
            predicates_add = predicates_rem[:-1]

            # Remove element from lists
            del element_list[index]
            del element_list_check[index]
            del objects_add[index]

        # Check that collection appropriately contains all the remaining
        # elements of list
        check_elements(bag, element_list)

        # Check that the removed and additional predicates and objects are
        # correct
        check_graph_diff_unordered_collection(
            graph_before,
            bag.graph,
            bag.iri,
            predicates_rem,
            predicates_add,
            objects_rem,
            objects_add,
        )


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
    """Test Bag's extend() method."""

    # Parse list of elements with check
    element_list, element_list_check = parse_element_list_with_check(
        element_list_with_check
    )

    # Create Bag
    bag = build_collection(Bag)

    # Freeze the state of the graph before calling the method
    graph_before = copy.deepcopy(bag.graph)

    # Keep elements in memory
    bag_elements_before = copy.deepcopy(bag.elements)

    # Extend Bag
    if model is not None:
        collection = build_collection(
            model,
            element_list=element_list,
        )
        bag.extend(collection)
    else:
        bag.extend(element_list)

    # Check that Bag appropriately contains all the elements of the two lists
    check_elements(bag, bag_elements_before + element_list)

    # TODO: Wrong test, as it doesn't account for the unordered nature of Bag
    # Prepare the removed and additional predicates
    triples_rem = []
    triples_add = [
        (bag.iri, RDF[f"_{len(bag_elements_before) + i + 1}"], element_check)
        for i, element_check in enumerate(element_list_check)
    ]

    # Check the correctness of the removed and additional triples
    check_rem_add(graph_before, bag.graph, triples_rem, triples_add)

    # # Prepare the removed and additional predicates
    # predicates_rem = [
    #     RDF[f"_{i + 1}"] for i in range(len(bag_elements_before))
    # ]
    # predicates_add = [RDF[f"_{i + 1}"] for i in range(len(bag_elements_after))]

    # # Check that the removed and additional predicates and objects are correct
    # check_rem_add_unordered(
    #     graph_before,
    #     bag.graph,
    #     bag.iri,
    #     predicates_rem,
    #     predicates_add,
    #     bag_elements_before,
    #     bag_elements_after,
    # )


@pytest.mark.parametrize("element_list_with_check", PARAMETERS_ELEMENT_LISTS)
def test_remove_element(
    element_list_with_check: list[tuple[IRI | Literal | Any, IRI | Literal]]
):
    """Test Bag's remove_element() method."""

    # Parse list of elements with check
    element_list, element_list_check = parse_element_list_with_check(
        element_list_with_check
    )

    # Create Bag
    bag = build_collection(Bag, element_list=element_list)

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
        graph_before = copy.deepcopy(bag.graph)

        # Initialize removed and additional predicates and objects
        predicates_rem = []
        predicates_add = []
        objects_rem = copy.deepcopy(element_list_check)
        objects_add = copy.deepcopy(element_list_check)

        # Find the index of element in list, if it contains it
        # Only consider exact matches (eg. 0 != 0.0 != False)
        index = index_exact_match(element, element_list)

        # If element is not in List
        if index is None:

            # Try to remove element from object
            try:
                bag.remove_element(element)
            except ValueError:
                pass

        # Otherwise, if element is in List
        else:

            # Remove element from object
            bag.remove_element(element)

            # Prepare the removed and additional predicates
            predicates_rem = [
                RDF[f"_{i + 1}"] for i in range(len(element_list))
            ]
            predicates_add = predicates_rem[:-1]

            # Remove element from lists
            del element_list[index]
            del element_list_check[index]
            del objects_add[index]

        # Check that collection appropriately contains all the remaining
        # elements of list
        check_elements(bag, element_list)

        # Check that the removed and additional predicates and objects are
        # correct
        check_graph_diff_unordered_collection(
            graph_before,
            bag.graph,
            bag.iri,
            predicates_rem,
            predicates_add,
            objects_rem,
            objects_add,
        )
