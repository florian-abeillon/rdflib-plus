"""Test Alt's methods"""

import copy
import random as rd
import re
from contextlib import nullcontext
from typing import Any, Optional

import pytest
from rdflib import Literal
from rdflib import URIRef as IRI

from rdflib_plus import Alt, SimpleGraph
from tests.parameters import (
    PARAMETERS_ELEMENT_LISTS,
    PARAMETERS_ELEMENTS,
    PARAMETERS_MODELS_COLLECTIONS,
    PARAMETERS_PROPERTIES_CONTAINER,
)
from tests.tests_methods.utils import (
    build_collection,
    count_exact_match,
    index_exact_match,
)
from tests.utils import (
    SEED,
    WARNING_MESSAGE_ALT_COUNT,
    WARNING_MESSAGE_DEFAULT,
    WARNING_MESSAGE_DEFAULT_REMOVED,
    WARNING_MESSAGE_DUPLICATES,
    cartesian_product,
    check_elements,
    check_elements_unordered_collection,
    check_graph_alt,
    check_graph_collection,
    remove_duplicated_elements,
)

# Set random seed
rd.seed(SEED)


@pytest.mark.parametrize(
    "elements, elements_check, model",
    cartesian_product(
        PARAMETERS_ELEMENT_LISTS, [None, *PARAMETERS_MODELS_COLLECTIONS]
    ),
)
def test_elements(
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
    model: Optional[type],
):
    """Test Alt's elements setter."""

    # Initialize Alt
    alt, *_ = build_collection(Alt, allow_duplicates=False)

    # If a model is specified, create instance to initialize Alt with
    if model is not None:
        # If model is Alt and list of elements is not empty, expect warning
        with (
            pytest.warns(UserWarning)
            if model == Alt and elements
            else nullcontext()
        ):
            elements = model(SimpleGraph(), elements=elements)

    # If list of elements is not empty, expect warning
    with pytest.warns(UserWarning) if elements else nullcontext() as record:

        # Set elements property
        alt.elements = elements

        # If expecting warnings
        if record is not None:

            # Check default warning
            *record, default_warning = record
            assert re.search(
                WARNING_MESSAGE_DEFAULT, str(default_warning.message)
            )

            # If list of elements contains duplicates
            nb_duplicates = len(elements_check) - len(set(elements_check))
            if nb_duplicates > 0:

                # Check that one warning is raised for each duplicate
                assert len(record) == nb_duplicates
                for r in record:
                    assert re.search(
                        WARNING_MESSAGE_DUPLICATES, str(r.message)
                    )

    # Remove them from the list
    elements, elements_check = remove_duplicated_elements(
        elements, elements_check
    )

    # Check that Alt contains exactly all the elements
    check_elements_unordered_collection(alt, elements)

    # Check that the graph is correct after calling the method
    check_graph_alt(alt, elements_check)


@pytest.mark.parametrize(
    "alternatives, alternatives_check, model, allow_duplicates",
    cartesian_product(
        PARAMETERS_ELEMENT_LISTS,
        [None, *PARAMETERS_MODELS_COLLECTIONS],
        [True, False],
    ),
)
def test_alternatives(
    alternatives: list[IRI | Literal | Any],
    alternatives_check: list[IRI | Literal],
    allow_duplicates: bool,
    model: Optional[type],
):
    """Test Alt's alternatives setter."""

    # Initialize Alt
    alt, elements, elements_check = build_collection(
        Alt, allow_duplicates=allow_duplicates
    )

    # Remember whether Alt is empty
    was_alt_empty = not bool(elements)

    # If a model is specified, create instance to initialize Alt with
    if model is not None:
        # If model is Alt and list of elements is not empty, expect warning
        with (
            pytest.warns(UserWarning)
            if model == Alt and alternatives
            else nullcontext()
        ):
            alternatives = model(SimpleGraph(), elements=alternatives)

    # Keep the first element (if any), and add the alternatives to make
    # the new element list
    if elements:
        elements = [elements[0]]
        elements_check = [elements_check[0]]
    elements += alternatives
    elements_check += alternatives_check

    # If alternatives contains unallowed duplicates, expect warning
    nb_duplicates = len(elements_check) - len(set(elements_check))
    with (
        pytest.warns(UserWarning)
        if (was_alt_empty and alternatives)
        or (not allow_duplicates and nb_duplicates > 0)
        else nullcontext()
    ) as record:

        # Set elements property
        alt.alternatives = alternatives

        # If no default element is specified
        if was_alt_empty and alternatives:
            # Check default warning
            *record, default_warning = record
            assert re.search(
                WARNING_MESSAGE_DEFAULT, str(default_warning.message)
            )

        # If list of elements contains duplicates
        if not allow_duplicates and nb_duplicates > 0:

            # Check that one warning is raised for each duplicate
            assert len(record) == nb_duplicates
            for r in record:
                assert re.search(WARNING_MESSAGE_DUPLICATES, str(r.message))

    # If duplicates are not allowed, remove any from the element list
    if not allow_duplicates:
        elements, elements_check = remove_duplicated_elements(
            elements, elements_check
        )

    # Check that Alt contains exactly all the elements
    check_elements_unordered_collection(alt, elements)

    # Check that the graph is correct after calling the method
    check_graph_alt(alt, elements_check)


@pytest.mark.parametrize(
    "default, default_check, allow_duplicates",
    cartesian_product(PARAMETERS_ELEMENTS, [True, False]),
)
def test_default(
    default: IRI | Literal | Any,
    default_check: IRI | Literal,
    allow_duplicates: bool,
):
    """Test Alt's default setter."""

    # Initialize Alt
    alt, elements, elements_check = build_collection(
        Alt, allow_duplicates=allow_duplicates
    )

    # Set default
    alt.default = default

    # If duplicates are not allowed
    if not allow_duplicates:

        # Remove any duplicate from the list
        elements, elements_check = remove_duplicated_elements(
            elements, elements_check
        )

        # Remove new default from the list (if it appears in it)
        index = index_exact_match(default_check, elements_check)
        if index is not None:
            del elements[index]
            del elements_check[index]

    # Check that the default and elements properties were updated correctly
    assert alt.default == default

    # Check that Alt contains exactly all the elements
    check_elements_unordered_collection(alt, [default] + elements)

    # Check that the graph is correct after calling the method
    check_graph_alt(alt, elements_check, default=default_check)


@pytest.mark.parametrize(
    "element, element_check, allow_duplicates",
    cartesian_product(PARAMETERS_ELEMENTS, [True, False]),
)
def test_add_alternative(
    element: IRI | Literal | Any,
    element_check: IRI | Literal,
    allow_duplicates: bool,
):
    """Test Alt's add_alternative() method."""

    # Initialize Alt
    alt, elements, elements_check = build_collection(
        Alt, allow_duplicates=allow_duplicates
    )

    # If duplicates are not allowed and list of elements contains
    # element, expect warning
    with (
        pytest.warns(UserWarning)
        if not allow_duplicates and element_check in elements_check
        else nullcontext()
    ) as record:

        # Add alternative
        alt.add_alternative(element)

        # If expecting warnings
        if record is not None:
            assert len(record) == 1
            assert re.search(
                WARNING_MESSAGE_DUPLICATES, str(record[0].message)
            )

    # If duplicates are not allowed, remove them from the list
    if not allow_duplicates:
        elements, elements_check = remove_duplicated_elements(
            elements, elements_check
        )

    # If duplicates are allowed, or new alternative does not appear in
    # original list
    if allow_duplicates or element_check not in elements_check:
        # Add new alternative to lists
        elements.append(element)
        elements_check.append(element_check)

    # Check that Alt contains exactly all the elements
    check_elements_unordered_collection(alt, elements)

    # Check that the graph is correct after calling the method
    check_graph_alt(alt, elements_check)


@pytest.mark.parametrize("elements, elements_check", PARAMETERS_ELEMENT_LISTS)
def test_any_alternative(
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
):
    """Test Alt's any_alternative() method."""

    # If list of elements is not empty, expect warning
    with (
        pytest.warns(UserWarning, match=WARNING_MESSAGE_DEFAULT)
        if elements
        else nullcontext()
    ):
        # Initialize Alt
        alt = Alt(SimpleGraph(), elements=elements)

    # If no alternatives were specified,
    # make sure that None is returned every time
    if len(elements) < 2:
        for _ in range(10):
            assert alt.any_alternative() is None

    # Otherwise, make sure that elements from the list are returned every time
    else:
        for _ in range(3 * len(elements)):
            assert alt.any_alternative() in elements


@pytest.mark.parametrize("elements, elements_check", PARAMETERS_ELEMENT_LISTS)
def test_copy(
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
):
    """Test Alt's copy() method."""

    # If list of elements is not empty, expect warning
    with (
        pytest.warns(UserWarning, match=WARNING_MESSAGE_DEFAULT)
        if elements
        else nullcontext()
    ):
        # Create Alt
        alt = Alt(SimpleGraph(), elements=elements)

    # Freeze the state of the graph before calling the method
    graph_before = copy.deepcopy(alt.graph)

    # Copy Alt
    alt_new = alt.copy()

    # Check that the copied Alt is of the correct type
    assert isinstance(alt_new, Alt)

    # Check that the copied Alt has the same elements, default and alternatives
    check_elements_unordered_collection(alt_new, elements)
    assert alt_new.default == alt.default
    assert alt_new.alternatives == alt.alternatives

    # Check that the copied Alt has the same properties
    for property_ in PARAMETERS_PROPERTIES_CONTAINER:
        if hasattr(alt, property_):
            assert getattr(alt, property_) == getattr(alt_new, property_)
        else:
            assert not hasattr(alt_new, property_)

    # Check that the graph is correct after calling the method
    check_graph_alt(alt_new, elements_check, graph_diff=graph_before)


@pytest.mark.parametrize(
    "elements_add, elements_add_check, allow_duplicates",
    cartesian_product(PARAMETERS_ELEMENT_LISTS, [True, False]),
)
def test_count(
    elements_add: list[IRI | Literal | Any],
    elements_add_check: list[IRI | Literal],
    allow_duplicates: bool,
):
    """Test Alt's count() method."""

    # Initialize Alt
    alt, elements, elements_check = build_collection(
        Alt, allow_duplicates=allow_duplicates
    )

    # Create an extended list from the original and another one
    elements_with_check_extended = list(
        zip(
            elements + elements_add,
            elements_check + elements_add_check,
        )
    )

    # If duplicates are not allowed, remove any from the element list
    if not allow_duplicates:
        elements, elements_check = remove_duplicated_elements(
            elements, elements_check
        )

    # Shuffle extended list
    rd.shuffle(elements_with_check_extended)

    # If duplicates are not allowed, expect warning
    with (
        pytest.warns(UserWarning, match=re.escape(WARNING_MESSAGE_ALT_COUNT))
        if not allow_duplicates
        else nullcontext()
    ) as record:

        # For every element of the extended list
        for element, element_check in elements_with_check_extended:

            # Check that the number of time it appears in the original list is
            # returned
            assert alt.count(element) == count_exact_match(
                element_check, elements_check
            )

        # If expecting warnings, check them
        if record is not None:
            assert len(record) == len(elements_with_check_extended)


@pytest.mark.parametrize(
    "elements_add, elements_add_check", PARAMETERS_ELEMENT_LISTS
)
def test_discard_element(
    elements_add: list[IRI | Literal | Any],
    elements_add_check: list[IRI | Literal],
):
    """Test Alt's discard_element() method."""

    # Create Alt
    alt, elements, elements_check = build_collection(Alt)

    # Create an extended list from the original and another one, and shuffle it
    elements_with_check_extended = list(
        zip(
            elements + elements_add,
            elements_check + elements_add_check,
        )
    )
    rd.shuffle(elements_with_check_extended)

    # Always expect warning (as all elements of Alt will be discarded,
    # default must be removed at least once)
    with pytest.warns(UserWarning) if elements else nullcontext() as record:

        # Keep track of the series of Alt's default
        default = alt.default
        defaults = []

        # For every element of the extended list
        for element, element_check in elements_with_check_extended:

            # Discard element from object
            alt.discard_element(element)

            # If default changed, remember it
            if alt.default != default:
                defaults.append(alt.default)
                default = alt.default

            # Find the index of element in list, if it contains it
            # Only consider exact matches (eg. 0 != 0.0 != False)
            index = index_exact_match(element_check, elements_check)

            # If element is in Alt, remove it from the list
            if index is not None:
                del elements[index]
                del elements_check[index]

            # Check that Alt contains exactly all the elements
            check_elements(alt, elements)

            # Check that the graph is correct after calling the method
            check_graph_alt(alt, elements_check)

        # If expecting warnings, check them
        if record is not None:
            assert len(record) > 0
            for r, default in zip(record, defaults):
                assert WARNING_MESSAGE_DEFAULT_REMOVED.format(default) in str(
                    r.message
                )


@pytest.mark.parametrize(
    "elements_add, elements_add_check", PARAMETERS_ELEMENT_LISTS
)
def test_remove_element(
    elements_add: list[IRI | Literal | Any],
    elements_add_check: list[IRI | Literal],
):
    """Test Alt's remove_element() method."""

    # Create Alt
    alt, elements, elements_check = build_collection(Alt)

    # Create an extended list from the original and another one, and shuffle it
    elements_with_check_extended = list(
        zip(
            elements + elements_add,
            elements_check + elements_add_check,
        )
    )
    rd.shuffle(elements_with_check_extended)

    # Always expect warning (as all elements of Alt will be discarded,
    # default must be removed at least once)
    with pytest.warns(UserWarning) if elements else nullcontext() as record:

        # Keep track of the series of Alt's default
        default = alt.default
        defaults = []

        # For every element of the extended list
        for element, element_check in elements_with_check_extended:

            # Find the index of element in list, if it contains it
            # Only consider exact matches (eg. 0 != 0.0 != False)
            index = index_exact_match(element_check, elements_check)

            # Try to remove element from object
            try:
                alt.remove_element(element)
                assert index is not None

                # If default changed, remember it
                if alt.default != default:
                    defaults.append(alt.default)
                    default = alt.default

                # If element is in Alt, remove it from the list
                del elements[index]
                del elements_check[index]

            except ValueError:
                assert index is None

            # Check that Alt contains exactly all the elements
            check_elements(alt, elements)

            # Check that the graph is correct after calling the method
            check_graph_collection(alt, elements_check)

        # If expecting warnings, check them
        if record is not None:
            for r, default in zip(record, defaults):
                assert WARNING_MESSAGE_DEFAULT_REMOVED.format(default) in str(
                    r.message
                )
