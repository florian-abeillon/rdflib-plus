"""Test Seq constructor"""

from typing import Any

import pytest
from rdflib import RDF, Literal
from rdflib import URIRef as IRI

from tests.parameters import PARAMETERS_ELEMENT_LISTS, PARAMETERS_SEQ
from tests.tests_init.utils import check_init_blank_node_object


@pytest.mark.parametrize("elements, elements_check", PARAMETERS_ELEMENT_LISTS)
def test_init_seq_with_elements(
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
):
    """Test Seq creation with element list."""

    # Set kwargs to be used by constructor
    kwargs = {"elements": elements}

    # Set additional triples
    triples_add = [
        (RDF[f"_{i + 1}"], element_check)
        for i, element_check in enumerate(elements_check)
    ]

    # Test constructor
    seq = check_init_blank_node_object(
        *PARAMETERS_SEQ,
        kwargs=kwargs,
        triples_add=triples_add,
    )

    # Check elements property
    assert seq.elements == elements
