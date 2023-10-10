"""Test custom Graph constructor"""

from typing import Callable

from rdflib import RDF, RDFS

from rdflib_plus import Graph


def test_init() -> None:
    """Test Graph object creation."""

    # Initialize graph
    graph = Graph()

    # Check attributes
    assert hasattr(graph, "Resource")
    assert isinstance(graph.Resource, Callable)

    # Create RDFS Resource from graph
    resource = graph.Resource()

    # Check adequate triples (and no others) are in graph
    triples = [
        (
            resource.iri,
            RDF.type,
            RDFS.Resource,
        ),
    ]
    assert len(graph) == len(triples)
    for triple in triples:
        assert triple in graph
