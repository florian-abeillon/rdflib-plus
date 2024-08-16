"""Test Resource methods"""

from typing import Any

import pytest
from rdflib import RDF, RDFS, XSD, Literal
from rdflib import URIRef as IRI

from rdflib_plus import Resource, SimpleGraph


@pytest.mark.parametrize(
    "o,is_o_resource,value",
    [
        (
            IRI("http://default.example.com/Resource#2"),
            False,
            IRI("http://default.example.com/Resource#2"),
        ),
        (
            IRI("http://default.example.com/Resource#object"),
            True,
            IRI("http://default.example.com/Resource#object"),
        ),
        (2, False, Literal(2, datatype=XSD.integer)),
        ("two", False, Literal("two", datatype=XSD.string)),
        (True, False, Literal(True, datatype=XSD.boolean)),
    ],
)
def test_add_predicate_resource(
    o: Resource | IRI | Literal | Any,
    is_o_resource: bool,
    value: IRI | Literal,
):
    """Test Resource's add() method, with a Resource as predicate."""

    # Initialize graph
    graph = SimpleGraph()

    # Create Resource subject and predicate
    subject = Resource(graph, check_triples=False)
    predicate = Resource(graph)

    # If o should be considered as a resource
    if is_o_resource:
        # Create Resource object
        o = Resource(graph, iri=o)

    # Add triple
    subject.add(predicate, o)

    # Check adequate triples are in graph
    triples = [
        (
            subject.iri,
            RDF.type,
            RDFS.Resource,
        ),
        (
            predicate.iri,
            RDF.type,
            RDFS.Resource,
        ),
        (
            subject.iri,
            predicate.iri,
            o.iri if is_o_resource else value,
        ),
    ]
    if is_o_resource:
        triples.append(
            (
                o.iri,
                RDF.type,
                RDFS.Resource,
            )
        )
    assert len(graph) == len(triples)
    for triple in triples:
        assert triple in graph


@pytest.mark.parametrize(
    "p,o,is_o_resource,value",
    [
        (
            IRI("http://default.example.com/Resource#1"),
            IRI("http://default.example.com/Resource#2"),
            False,
            IRI("http://default.example.com/Resource#2"),
        ),
        (
            IRI("http://default.example.com/Resource#1"),
            IRI("http://default.example.com/Resource#2"),
            True,
            IRI("http://default.example.com/Resource#2"),
        ),
        (
            IRI("http://default.example.com/Resource#predicate"),
            2,
            False,
            Literal(2, datatype=XSD.integer),
        ),
        (
            IRI("http://default.example.com/Resource#relation"),
            "two",
            False,
            Literal("two", datatype=XSD.string),
        ),
        (
            IRI("http://default.example.com/Resource#link"),
            True,
            False,
            Literal(True, datatype=XSD.boolean),
        ),
    ],
)
def test_add_predicate_iri(
    p: IRI,
    o: Resource | IRI | Literal | Any,
    is_o_resource: bool,
    value: IRI | Literal,
):
    """Test Resource's add() method, with an IRI as predicate."""

    # Initialize graph
    graph = SimpleGraph()

    # Create Resource subject
    subject = Resource(graph, check_triples=False)

    # If o should be considered as a resource
    if is_o_resource:
        # Create Resource object
        o = Resource(graph, iri=o)

    # Add triple
    subject.add(p, o)

    # Check adequate triples are in graph
    triples = [
        (
            subject.iri,
            RDF.type,
            RDFS.Resource,
        ),
        (
            subject.iri,
            p,
            o.iri if is_o_resource else value,
        ),
    ]
    if is_o_resource:
        triples.append(
            (
                o.iri,
                RDF.type,
                RDFS.Resource,
            )
        )
    assert len(graph) == len(triples)
    for triple in triples:
        assert triple in graph


@pytest.mark.parametrize(
    "o,is_o_resource,lang,value",
    [
        (
            IRI("http://default.example.com/Resource#2"),
            False,
            "en-us",
            IRI("http://default.example.com/Resource#2"),
        ),
        (
            IRI("http://default.example.com/Resource#2"),
            True,
            "en-us",
            IRI("http://default.example.com/Resource#2"),
        ),
        (
            2,
            False,
            "en-us",
            Literal(2, datatype=XSD.integer),
        ),
        (
            "two",
            False,
            "en-us",
            Literal("two", lang="en-us"),
        ),
        (
            "deux",
            False,
            "fr",
            Literal("deux", lang="fr"),
        ),
        (
            True,
            False,
            "en-us",
            Literal(True, datatype=XSD.boolean),
        ),
    ],
)
def test_add_lang(
    o: Resource | IRI | Literal | Any,
    is_o_resource: bool,
    lang: str,
    value: IRI | Literal,
):
    """Test Resource's add() method, with a language specified."""

    # Initialize graph
    graph = SimpleGraph()

    # Create Resource subject and predicate
    subject = Resource(graph, check_triples=False)
    predicate = Resource(graph)

    # If o should be considered as a resource
    if is_o_resource:
        # Create Resource object
        o = Resource(graph, iri=o)

    # Add triple
    subject.add(predicate, o, lang=lang)

    # Check adequate triples are in graph
    triples = [
        (
            subject.iri,
            RDF.type,
            RDFS.Resource,
        ),
        (
            predicate.iri,
            RDF.type,
            RDFS.Resource,
        ),
        (
            subject.iri,
            predicate.iri,
            o.iri if is_o_resource else value,
        ),
    ]
    if is_o_resource:
        triples.append(
            (
                o.iri,
                RDF.type,
                RDFS.Resource,
            )
        )
    assert len(graph) == len(triples)
    for triple in triples:
        assert triple in graph


@pytest.mark.parametrize(
    "o,is_o_resource,value",
    [
        (
            IRI("http://default.example.com/Resource#2"),
            False,
            IRI("http://default.example.com/Resource#2"),
        ),
        (
            IRI("http://default.example.com/Resource#object"),
            True,
            IRI("http://default.example.com/Resource#object"),
        ),
        (2, False, Literal(2, datatype=XSD.integer)),
        ("two", False, Literal("two", datatype=XSD.string)),
        (True, False, Literal(True, datatype=XSD.boolean)),
    ],
)
def test_add_graph(
    o: Resource | IRI | Literal | Any,
    is_o_resource: bool,
    value: IRI | Literal,
):
    """Test Resource's add() method, with another graph specified."""

    # Initialize graph
    graph = SimpleGraph()

    # Create Resource subject and predicate in graph
    subject = Resource(graph, check_triples=False)
    predicate = Resource(graph)

    # If o should be considered as a resource
    if is_o_resource:
        # Create Resource object
        o = Resource(graph, iri=o)

    # Initialize another graph
    graph_add = SimpleGraph()

    # Add triple
    subject.add(predicate, o, graph=graph_add)

    # Check adequate triples are in graph
    triples = [
        (
            subject.iri,
            RDF.type,
            RDFS.Resource,
        ),
        (
            predicate.iri,
            RDF.type,
            RDFS.Resource,
        ),
    ]
    if is_o_resource:
        triples.append(
            (
                o.iri,
                RDF.type,
                RDFS.Resource,
            )
        )
    assert len(graph) == len(triples)
    for triple in triples:
        assert triple in graph

    # Check adequate triples are in graph_add
    triples_add = [
        (
            subject.iri,
            predicate.iri,
            o.iri if is_o_resource else value,
        ),
    ]
    assert len(graph_add) == len(triples_add)
    for triple_add in triples_add:
        assert triple_add in graph_add
