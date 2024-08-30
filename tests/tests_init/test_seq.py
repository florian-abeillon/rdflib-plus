"""Test Seq constructor"""

from typing import Any

import pytest
from rdflib import RDF, Literal
from rdflib import URIRef as IRI

from tests.parameters import PARAMETERS_ELEMENT_LISTS, PARAMETERS_SEQ
from tests.tests_init.utils import (
    check_elements,
    check_init_blank_node_object,
    format_elements,
)


@pytest.mark.parametrize("element_list", PARAMETERS_ELEMENT_LISTS)
def test_init_seq_with_elements(
    element_list: list[IRI | Literal | Any],
):
    """Test Seq creation with element list."""

    # Set kwargs to be used by constructor
    kwargs = {"elements": element_list}

    # Set additional triples
    elements = format_elements(element_list)
    add_triples = [
        (RDF[f"_{i + 1}"], element) for i, element in enumerate(elements)
    ]

    # Test constructor
    resource = check_init_blank_node_object(
        *PARAMETERS_SEQ,
        kwargs=kwargs,
        add_triples=add_triples,
    )

    # Check Seq's "elements" attribute
    check_elements(resource, element_list)
