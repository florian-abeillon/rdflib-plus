"""Test Alt constructor"""

import re
from contextlib import nullcontext
from typing import Any

import pytest
from rdflib import Literal
from rdflib import URIRef as IRI

from tests.parameters import (
    PARAMETERS_ALT,
    PARAMETERS_ELEMENT_LISTS,
    PARAMETERS_ELEMENTS,
)
from tests.tests_init.utils import check_init_blank_node_object
from tests.utils import (
    WARNING_MESSAGE_DEFAULT,
    WARNING_MESSAGE_DUPLICATES,
    cartesian_product,
    check_elements_unordered_collection,
    check_graph_alt,
    remove_duplicated_elements,
)


@pytest.mark.parametrize(
    "element, element_check, allow_duplicates",
    cartesian_product(PARAMETERS_ELEMENTS, [True, False]),
)
def test_init_with_default(
    element: IRI | Literal | Any,
    element_check: IRI | Literal,
    allow_duplicates: bool,
):
    """Test Alt creation with default element."""

    # Set kwargs to be used by constructor
    kwargs = {"default": element, "allow_duplicates": allow_duplicates}

    # Test constructor
    alt = check_init_blank_node_object(
        *PARAMETERS_ALT,
        kwargs=kwargs,
        check_triples=False,
    )

    # Check default, alternatives and elements properties
    assert alt.default == element
    assert alt.alternatives == []
    assert alt.elements == [element]

    # Check that the graph is correct after calling the method
    check_graph_alt(alt, [element_check])


@pytest.mark.parametrize(
    "elements, elements_check, allow_duplicates",
    cartesian_product(PARAMETERS_ELEMENT_LISTS, [True, False]),
)
def test_init_with_alternatives(
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
    allow_duplicates: bool,
):
    """Test Alt creation with alternative elements."""

    # Set kwargs to be used by constructor
    kwargs = {
        "alternatives": elements,
        "allow_duplicates": allow_duplicates,
    }

    # If list of elements is not empty, expect warning
    with pytest.warns(UserWarning) if elements else nullcontext() as record:

        # Test constructor
        alt = check_init_blank_node_object(
            *PARAMETERS_ALT,
            kwargs=kwargs,
            check_triples=False,
        )

        # If expecting warnings
        if record is not None:

            # Check default warning
            *record, default_warning = record
            assert re.search(
                WARNING_MESSAGE_DEFAULT, str(default_warning.message)
            )

            # If duplicates are not allowed
            if not allow_duplicates:

                # If there are duplicates
                nb_duplicates = len(elements_check) - len(set(elements_check))
                if nb_duplicates > 0:

                    # Check that one warning is raised for each duplicate
                    assert len(record) == nb_duplicates
                    for r in record:
                        assert re.search(
                            WARNING_MESSAGE_DUPLICATES, str(r.message)
                        )

    # If duplicates are not allowed, remove them from the list
    if not allow_duplicates:
        elements, elements_check = remove_duplicated_elements(
            elements, elements_check
        )

    # If no elements were specified, check that default and alternatives
    # properties were initialized correctly
    if not elements:
        assert alt.default is None
        assert alt.alternatives == []

    # Check that Alt contains exactly all the elements
    check_elements_unordered_collection(alt, elements)

    # Check that the graph is correct after calling the method
    check_graph_alt(alt, elements_check)


@pytest.mark.parametrize(
    "default, default_check, alternatives, alternatives_check, "
    "allow_duplicates",
    cartesian_product(
        PARAMETERS_ELEMENTS, PARAMETERS_ELEMENT_LISTS, [True, False]
    ),
)
def test_init_with_default_and_alternatives(
    default: IRI | Literal | Any,
    default_check: IRI | Literal,
    alternatives: list[IRI | Literal | Any],
    alternatives_check: list[IRI | Literal],
    allow_duplicates: bool,
):
    """Test Alt creation with default and alternative elements."""

    # Set kwargs to be used by constructor
    kwargs = {
        "default": default,
        "alternatives": alternatives,
        "allow_duplicates": allow_duplicates,
    }

    # Set up the list of elements
    elements = [default] + alternatives
    elements_check = [default_check] + alternatives_check

    # If no default element is specified or list of elements contains
    # unallowed duplicates, expect warning
    nb_duplicates = len(elements_check) - len(set(elements_check))
    with (
        pytest.warns(UserWarning)
        if default is None or (not allow_duplicates and nb_duplicates > 0)
        else nullcontext()
    ) as record:

        # Test constructor
        alt = check_init_blank_node_object(
            *PARAMETERS_ALT,
            kwargs=kwargs,
            check_triples=False,
        )

        # If no default element is specified
        if default is None:
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

    # Check that default property was initialized correctly
    assert alt.default == default

    # If duplicates are not allowed, remove them from the list
    if not allow_duplicates:
        elements, elements_check = remove_duplicated_elements(
            elements, elements_check
        )

    # Check that Alt contains exactly all the elements
    check_elements_unordered_collection(alt, elements)

    # Check that alternatives property was initialized correctly
    check_elements_unordered_collection(alt.alternatives, elements[1:])

    # Check that the graph is correct after calling the method
    check_graph_alt(alt, elements_check[1:], default=default_check)


@pytest.mark.parametrize(
    "elements, elements_check, allow_duplicates",
    cartesian_product(PARAMETERS_ELEMENT_LISTS, [True, False]),
)
def test_init_with_elements(
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
    allow_duplicates: bool,
):
    """Test Alt creation with elements."""

    # Set kwargs to be used by constructor
    kwargs = {"elements": elements, "allow_duplicates": allow_duplicates}

    # If list of elements is not empty, expect warning
    with pytest.warns(UserWarning) if elements else nullcontext() as record:

        # Test constructor
        alt = check_init_blank_node_object(
            *PARAMETERS_ALT,
            kwargs=kwargs,
            check_triples=False,
        )

        # If expecting warnings
        if record is not None:

            # Check default warning
            *record, default_warning = record
            assert re.search(
                WARNING_MESSAGE_DEFAULT, str(default_warning.message)
            )

            # If list of elements contains duplicates
            nb_duplicates = len(elements_check) - len(set(elements_check))
            if not allow_duplicates and nb_duplicates > 0:

                # Check that one warning is raised for each duplicate
                assert len(record) == nb_duplicates
                for r in record:
                    assert re.search(
                        WARNING_MESSAGE_DUPLICATES, str(r.message)
                    )

    # If duplicates are not allowed, remove them from the list
    if not allow_duplicates:
        elements, elements_check = remove_duplicated_elements(
            elements, elements_check
        )

    # If no elements were specified, check that default and alternatives
    # properties were initialized correctly
    if not elements:
        assert alt.default is None
        assert alt.alternatives == []

    # Check that Alt contains exactly all the elements
    check_elements_unordered_collection(alt, elements)

    # Check that the graph is correct after calling the method
    check_graph_alt(alt, elements_check)


# TODO: Write test for error raised by __init__()
