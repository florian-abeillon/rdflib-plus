"""Test List constructor"""

from typing import Any

import pytest
from rdflib import Literal
from rdflib import URIRef as IRI

from tests.parameters import PARAMETERS_ELEMENT_LISTS, PARAMETERS_LIST
from tests.tests_init.utils import check_init_blank_node_object
from tests.utils import check_graph_list


@pytest.mark.parametrize(
    "element_list, element_list_check", PARAMETERS_ELEMENT_LISTS
)
def test_init_with_elements(
    element_list: list[IRI | Literal | Any],
    element_list_check: list[IRI | Literal],
):
    """Test List creation with element list."""

    # Set kwargs to be used by constructor
    kwargs = {"elements": element_list}

    # Test constructor
    list_ = check_init_blank_node_object(
        *PARAMETERS_LIST,
        kwargs=kwargs,
        check_triples=False,
    )

    # Check elements property
    assert list_.elements == element_list

    # Check that the graph contains the list with all the elements
    check_graph_list(list_.iri, element_list_check, list_.graph)
