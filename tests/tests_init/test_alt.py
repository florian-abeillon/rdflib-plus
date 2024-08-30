"""Test Alt constructor"""

from typing import Any

import pytest
from rdflib import Literal
from rdflib import URIRef as IRI

from tests.parameters import PARAMETERS_ELEMENT_LISTS, PARAMETERS_ELEMENTS
from tests.tests_init.utils import check_init_alt


@pytest.mark.parametrize("element", PARAMETERS_ELEMENTS)
def test_init_with_default(
    element: IRI | Literal | Any,
):
    """Test Alt creation with default element."""

    # Define default and alternative elements,
    # and set additional triples
    default = element
    alternatives = None

    # Check Alt creation
    check_init_alt(default, alternatives)


@pytest.mark.parametrize("element_list", PARAMETERS_ELEMENT_LISTS)
def test_init_with_alternatives(
    element_list: list[IRI | Literal | Any],
):
    """Test Alt creation with default and alternative elements."""

    # Define default and alternative elements,
    # and set additional triples
    default = None
    alternatives = element_list

    # Check Alt creation
    check_init_alt(default, alternatives)


@pytest.mark.parametrize("element_list", PARAMETERS_ELEMENT_LISTS)
def test_init_with_default_and_alternatives(
    element_list: list[IRI | Literal | Any],
):
    """Test Alt creation with default and alternative elements."""

    # Define default and alternative elements,
    # and set additional triples
    if element_list:
        default, *alternatives = element_list

    else:
        default = None
        alternatives = None

    # Check Alt creation
    check_init_alt(default, alternatives)
