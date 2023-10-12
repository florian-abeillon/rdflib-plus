"""Test RDFS Resource constructor"""

import pytest
from rdflib import DCTERMS, RDF, RDFS, SKOS, XSD, Literal, Namespace
from rdflib import URIRef as IRI

from rdflib_plus import MultiGraph, Resource, SimpleGraph


@pytest.mark.parametrize(
    "identifier,iri",
    [
        (1, IRI("http://default.example.com/Resource#1")),
        (42, IRI("http://default.example.com/Resource#42")),
        ("0.1.0", IRI("http://default.example.com/Resource#0.1.0")),
        ("identifier", IRI("http://default.example.com/Resource#identifier")),
    ],
)
def test_init_with_identifier(identifier: str, iri: IRI):
    """Test Resource object creation with identifier."""

    # Initialize graph
    graph = SimpleGraph()

    # Create Resource object
    resource = Resource(graph, identifier=identifier)

    # Check attributes
    assert resource.iri == iri
    assert resource.path == ["Resource"]
    assert resource.type == RDFS.Resource

    # Check adequate triples (and no others) are in graph
    triples = [
        (
            iri,
            RDF.type,
            RDFS.Resource,
        ),
        (
            iri,
            DCTERMS.identifier,
            Literal(identifier, datatype=XSD.string),
        ),
    ]
    assert len(graph) == len(triples)
    for triple in triples:
        assert triple in graph


@pytest.mark.parametrize(
    "label,iri",
    [
        ("label", IRI("http://default.example.com/Resource#label")),
        ("Label", IRI("http://default.example.com/Resource#Label")),
        ("LABEL", IRI("http://default.example.com/Resource#LABEL")),
        ("laBel", IRI("http://default.example.com/Resource#laBel")),
        ("123456789", IRI("http://default.example.com/Resource#123456789")),
        ("R2-D2", IRI("http://default.example.com/Resource#R2-D2")),
        ("fun.", IRI("http://default.example.com/Resource#fun.")),
        (
            "label> a rdfs:Resource . <http://evil.com#command> a <http://evil.com#injection",
            IRI(
                "http://default.example.com/Resource#label%3E%20a%20rdfs:Resource%20.%20%3Chttp://evil.com%23command%3E%20a%20%3Chttp://evil.com%23injection"
            ),
        ),
    ],
)
def test_init_with_label(label: str, iri: IRI):
    """Test Resource object creation with label."""

    # Initialize graph
    graph = SimpleGraph()

    # Create Resource object
    resource = Resource(graph, label=label)

    # Check attributes
    assert resource.iri == iri
    assert resource.path == ["Resource"]
    assert resource.type == RDFS.Resource

    # Check adequate triples are in graph
    triples = [
        (
            iri,
            RDF.type,
            RDFS.Resource,
        ),
        (
            iri,
            DCTERMS.identifier,
            Literal(label, datatype=XSD.string),
        ),
        (
            iri,
            SKOS.prefLabel,
            Literal(label, datatype=XSD.string),
        ),
    ]
    assert len(graph) == len(triples)
    for triple in triples:
        assert triple in graph


@pytest.mark.parametrize(
    "label,lang,iri",
    [
        (
            "behaviour",
            "en",
            IRI("http://default.example.com/Resource#behaviour"),
        ),
        (
            "behavior",
            "en-us",
            IRI("http://default.example.com/Resource#behavior"),
        ),
        (
            "comportement",
            "fr-FR",
            IRI("http://default.example.com/Resource#comportement"),
        ),
    ],
)
def test_init_with_label_and_lang(label: str, lang: str, iri: IRI):
    """Test Resource object creation with label and language."""

    # Initialize graph
    graph = SimpleGraph()

    # Create Resource object
    resource = Resource(graph, label=label, lang=lang)

    # Check attributes
    assert resource.iri == iri
    assert resource.path == ["Resource"]
    assert resource.type == RDFS.Resource

    # Check adequate triples are in graph
    triples = [
        (
            iri,
            RDF.type,
            RDFS.Resource,
        ),
        (
            iri,
            DCTERMS.identifier,
            Literal(label, lang=lang),
        ),
        (
            iri,
            SKOS.prefLabel,
            Literal(label, lang=lang),
        ),
    ]
    assert len(graph) == len(triples)
    for triple in triples:
        assert triple in graph


@pytest.mark.parametrize(
    "identifier,label,iri",
    [
        (
            "identifier",
            "identifier",
            IRI("http://default.example.com/Resource#identifier"),
        ),
        (1, "label", IRI("http://default.example.com/Resource#1")),
    ],
)
def test_init_with_identifier_and_label(identifier: str, label: str, iri: IRI):
    """Test Resource object creation with identifier and label."""

    # Initialize graph
    graph = SimpleGraph()

    # Create Resource object
    resource = Resource(graph, identifier=identifier, label=label)

    # Check attributes
    assert resource.iri == iri
    assert resource.path == ["Resource"]
    assert resource.type == RDFS.Resource

    # Check adequate triples are in graph
    triples = [
        (
            iri,
            RDF.type,
            RDFS.Resource,
        ),
        (
            iri,
            DCTERMS.identifier,
            Literal(identifier, datatype=XSD.string),
        ),
        (
            iri,
            SKOS.prefLabel,
            Literal(label, datatype=XSD.string),
        ),
    ]
    assert len(graph) == len(triples)
    for triple in triples:
        assert triple in graph


@pytest.mark.parametrize(
    "iri",
    [
        IRI("http://default.example.com/Resource#1"),
        IRI("http://default.example.com/Resource#label"),
    ],
)
def test_init_with_iri(iri: IRI):
    """Test Resource object creation with iri."""

    # Initialize graph
    graph = SimpleGraph()

    # Create Resource object
    resource = Resource(graph, iri=iri)

    # Check attributes
    assert resource.iri == iri
    assert resource.path == ["Resource"]
    assert resource.type == RDFS.Resource

    # Check adequate triples are in graph
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


def test_init_blank_node():
    """Test blank node creation."""

    # Initialize graph
    graph = SimpleGraph()

    # Create Resource object
    resource = Resource(graph)

    # Check attributes
    assert isinstance(resource.iri, IRI)
    assert resource.path == ["Resource"]
    assert resource.type == RDFS.Resource

    # Check adequate triples are in graph
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


@pytest.mark.parametrize(
    "identifier,path,iri",
    [
        (
            1,
            ["path", "to", "resource"],
            IRI("http://default.example.com/path/to/resource/Resource#1"),
        ),
        (
            "id",
            ["ResourceParent"],
            IRI("http://default.example.com/ResourceParent/Resource#id"),
        ),
    ],
)
def test_init_with_path(identifier: str, path: list[str], iri: IRI):
    """Test Resource object creation with a path."""

    # Initialize graph
    graph = SimpleGraph()

    # Create Resource object
    resource = Resource(graph, identifier=identifier, path=path)

    # Check attributes
    assert resource.iri == iri
    assert resource.path == (path + ["Resource"])
    assert resource.type == RDFS.Resource

    # Check adequate triples are in graph
    triples = [
        (
            iri,
            RDF.type,
            RDFS.Resource,
        ),
        (
            iri,
            DCTERMS.identifier,
            Literal(identifier, datatype=XSD.string),
        ),
    ]
    assert len(graph) == len(triples)
    for triple in triples:
        assert triple in graph


@pytest.mark.parametrize(
    "identifier,namespace,iri",
    [
        (
            1,
            Namespace("http://special.example.com/"),
            IRI("http://special.example.com/Resource#1"),
        ),
        (
            "id",
            Namespace("http://special.example.com"),
            IRI("http://special.example.com/Resource#id"),
        ),
    ],
)
def test_init_with_namespace(identifier: str, namespace: Namespace, iri: IRI):
    """Test Resource object creation within a namespace."""

    # Initialize graph
    graph = MultiGraph()

    # Create Resource object
    resource = Resource(graph, identifier=identifier, namespace=namespace)

    print(graph.serialize())

    # Check attributes
    assert resource.iri == iri
    assert resource.path == ["Resource"]
    assert resource.type == RDFS.Resource

    # Format namespace
    if str(namespace)[-1] != "/":
        namespace = Namespace(f"{namespace}/")

    # Check adequate triples are in graph
    triples = [
        (
            iri,
            RDF.type,
            RDFS.Resource,
        ),
        (
            iri,
            DCTERMS.identifier,
            Literal(identifier, datatype=XSD.string),
        ),
        (
            iri,
            DCTERMS.source,
            IRI(namespace),
        ),
    ]
    assert len(graph) == len(triples)
    for triple in triples:
        assert triple in graph


def test_init_with_check_triples():
    """Test Resource object creation with a systematic check of triples."""
    pass


def test_get_attribute():
    """Test Resource's get_attribute() method."""
    pass


def test_add():
    """Test Resource's add() method."""
    pass


def test_set():
    """Test Resource's set() method."""
    pass


def test_replace():
    """Test Resource's replace() method."""
    pass


def test_add_alt_label():
    """Test Resource's add_alt_label() method."""
    pass


def test_set_pref_label():
    """Test Resource's set_pref_label() method."""
    pass
