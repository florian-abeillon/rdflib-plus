"""Test Bag constructor"""

from typing import Any

import pytest
from rdflib import RDF, Literal
from rdflib import URIRef as IRI

from tests.parameters import PARAMETERS_BAG, PARAMETERS_ELEMENT_LISTS
from tests.tests_init.utils import check_init_blank_node_object
from tests.utils import check_graph_unordered_collection


@pytest.mark.parametrize(
    "element_list, element_list_check", PARAMETERS_ELEMENT_LISTS
)
def test_init_with_elements(
    element_list: list[IRI | Literal | Any],
    element_list_check: list[IRI | Literal],
):
    """Test Bag creation with element list."""

    # Set kwargs to be used by constructor
    kwargs = {"elements": element_list}

    # Test constructor
    bag = check_init_blank_node_object(
        *PARAMETERS_BAG,
        kwargs=kwargs,
        check_triples=False,
    )

    # Check elements property
    assert all(element in bag.elements for element in element_list)
    assert len(bag.elements) == len(element_list)

    # Check that the expected triples, predicates and objects (and only them)
    # were indeed added to the graph
    triples = [(bag.iri, RDF.type, RDF.Bag)]
    predicates = [RDF[f"_{i + 1}"] for i in range(len(element_list_check))]
    objects = element_list_check.copy()
    check_graph_unordered_collection(
        bag.iri,
        bag.graph,
        predicates,
        objects,
        triples=triples,
        exact=True,
    )
