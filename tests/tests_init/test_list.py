"""Test List constructor"""

from typing import Any

import pytest
from rdflib import RDF, Literal
from rdflib import URIRef as IRI

from tests.parameters import PARAMETERS_ELEMENT_LISTS, PARAMETERS_LIST
from tests.tests_init.utils import (
    check_elements,
    check_init_blank_node_object,
    format_elements,
)
from tests.utils import check_graph_triples


@pytest.mark.parametrize("element_list", PARAMETERS_ELEMENT_LISTS)
def test_init_with_elements(
    element_list: list[IRI | Literal | Any],
):
    """Test List creation with element list."""

    # Set kwargs to be used by constructor
    kwargs = {"elements": element_list}

    # Test constructor
    resource = check_init_blank_node_object(
        *PARAMETERS_LIST,
        kwargs=kwargs,
        check_triples=False,
    )

    # Check List's "elements" attribute
    check_elements(resource, element_list)

    # If there are elements in List
    if element_list:
        # Initialize triples to check
        triples = []
        iri = resource.iri

        # For each element
        for element in format_elements(element_list):
            # Add appropriate triples
            triples.append((iri, RDF.type, RDF.List))
            triples.append((iri, RDF.first, element))

            # Get IRI of next list
            triple_rest = list(resource.graph.triples((iri, RDF.rest, None)))
            assert len(triple_rest) == 1
            s, p, o = triple_rest[0]
            triples.append((iri, RDF.rest, o))

            # Set new iri
            iri = o

        # Check that last list points to RDF.nil
        assert iri == RDF.nil

        # Check that all triples are in the graph
        check_graph_triples(resource.graph, triples, exact=True)
