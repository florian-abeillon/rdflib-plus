"""Test Collection constructors"""

from typing import Any

import pytest
from rdflib import RDF, Literal
from rdflib import URIRef as IRI

from tests.parameters import (
    PARAMETERS_BAG,
    PARAMETERS_ELEMENT_LISTS,
    PARAMETERS_ELEMENTS,
    PARAMETERS_LIST,
    PARAMETERS_SEQ,
)
from tests.tests_init.utils import (
    check_container_predicates,
    check_elements,
    check_init_alt,
    check_init_blank_node_object,
    format_elements,
)
from tests.utils import check_graph_triples


@pytest.mark.parametrize("element_list", PARAMETERS_ELEMENT_LISTS)
def test_init_list_with_elements(
    element_list: list[IRI | Literal | Any],
):
    """Test List creation with element list."""

    # Set kwargs to be used by constructor
    kwargs = {"elements": element_list}

    # Test constructor
    graph, resource = check_init_blank_node_object(
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
            triple_rest = list(graph.triples((iri, RDF.rest, None)))
            assert len(triple_rest) == 1
            s, p, o = triple_rest[0]
            triples.append((iri, RDF.rest, o))

            # Set new iri
            iri = o

        # Check that last list points to RDF.nil
        assert iri == RDF.nil

        # Check that all triples are in the graph
        check_graph_triples(graph, triples, exact=True)


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
    graph, resource = check_init_blank_node_object(
        *PARAMETERS_SEQ,
        kwargs=kwargs,
        add_triples=add_triples,
    )

    # Check Seq's "elements" attribute
    check_elements(resource, element_list)


@pytest.mark.parametrize("element_list", PARAMETERS_ELEMENT_LISTS)
def test_init_bag_with_elements(
    element_list: list[IRI | Literal | Any],
):
    """Test Bag creation with element list."""

    # Set kwargs to be used by constructor
    kwargs = {"elements": element_list}

    # Set additional triples
    elements = format_elements(element_list)
    add_triples = [(None, element) for element in elements]

    # Test constructor
    graph, resource = check_init_blank_node_object(
        *PARAMETERS_BAG,
        kwargs=kwargs,
        add_triples=add_triples,
    )

    # Check Bag's "elements" attribute
    check_elements(resource, element_list)

    # Check that elements are related to resource with appropriate properties
    check_container_predicates(elements, graph, resource)


@pytest.mark.parametrize("element", PARAMETERS_ELEMENTS)
def test_init_alt_with_default(
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
def test_init_alt_with_alternatives(
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
def test_init_alt_with_default_and_alternatives(
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
