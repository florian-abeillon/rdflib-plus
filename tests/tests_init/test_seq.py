"""Test Seq constructor"""

from typing import Any

import pytest
from rdflib import RDF, Literal
from rdflib import URIRef as IRI

from tests.parameters import PARAMETERS_ELEMENT_LISTS, PARAMETERS_SEQ
from tests.tests_init.utils import check_init_blank_node_object


@pytest.mark.parametrize(
    "element_list, element_list_check", PARAMETERS_ELEMENT_LISTS
)
def test_init_seq_with_elements(
    element_list: list[IRI | Literal | Any],
    element_list_check: list[IRI | Literal],
):
    """Test Seq creation with element list."""

    # Set kwargs to be used by constructor
    kwargs = {"elements": element_list}

    # Set additional triples
    triples_add = [
        (RDF[f"_{i + 1}"], element_check)
        for i, element_check in enumerate(element_list_check)
    ]

    # Test constructor
    seq = check_init_blank_node_object(
        *PARAMETERS_SEQ,
        kwargs=kwargs,
        triples_add=triples_add,
    )

    # Check elements property
    assert seq.elements == element_list
