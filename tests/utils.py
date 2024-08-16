"""Useful functions for testing"""

import itertools
from typing import Optional

from rdflib import Namespace
from rdflib import URIRef as IRI

from rdflib_plus import MultiGraph, Resource, SimpleGraph

SEED = 1


def cartesian_product(*args):
    """Return cartesian product of multiple lists."""

    return [
        list(
            itertools.chain(
                *[
                    element if isinstance(element, tuple) else [element]
                    for element in combination
                ]
            )
        )
        for combination in itertools.product(*args)
    ]


def build_iri(
    identifier: str,
    namespace: Optional[Namespace | str] = None,
    path_joined: str = "",
    sep: str = "#",
    model_name: Optional[str] = "Resource",
):
    """Build resource IRI."""

    # If needed, set default namespace
    namespace = (
        "http://default.example.com" if namespace is None else str(namespace)
    )

    # Concatenate elements
    iri = namespace
    if path_joined:
        iri += "/" + path_joined
    if model_name is not None:
        iri += "/" + model_name
    iri += sep + identifier

    return IRI(iri)


def check_attributes(resource: Resource, **kwargs):
    """Check attribute values of resource."""

    # For every attribute-value pair
    for attribute, value in kwargs.items():
        # Check that resource has attribute
        assert hasattr(resource, attribute)
        print(resource, attribute)
        print(
            getattr(resource, attribute) == value,
            getattr(resource, attribute),
            type(getattr(resource, attribute)),
            value,
            type(value),
        )
        print("------------------")

        # Check that attribute has the right value
        assert getattr(resource, attribute) == value


def check_graph_triples(
    graph: SimpleGraph | MultiGraph,
    triples: list[tuple[IRI, IRI, IRI]],
    exact: bool = True,
):
    """Check that graph contains (or is equal to) a set of triples."""
    print("TRIPLES IN GRAPH")
    for triple in graph:
        print(triple)
    print("----------")

    # For every triple
    for triple in triples:
        # Check that it appears in graph
        print(triple in graph, triple)
        assert triple in graph

    if exact:
        # Check that graph is exactly the set of triples
        assert len(graph) == len(triples)
