"""Test List constructor"""

from typing import Any

import pytest
from rdflib import Literal
from rdflib import URIRef as IRI

from tests.parameters import PARAMETERS_ELEMENT_LISTS, PARAMETERS_LIST
from tests.tests_init.utils import check_init_blank_node_object
from tests.utils import check_graph_list


@pytest.mark.parametrize("elements, elements_check", PARAMETERS_ELEMENT_LISTS)
def test_init_with_elements(
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
):
    """Test List creation with element list."""

    # Set kwargs to be used by constructor
    kwargs = {"elements": elements}

    # Test constructor
    list_ = check_init_blank_node_object(
        *PARAMETERS_LIST,
        kwargs=kwargs,
        check_triples=False,
    )

    # Check elements property
    assert list_.elements == elements

    # Check that the graph contains the list with all the elements
    check_graph_list(list_, elements_check)
