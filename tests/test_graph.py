"""Test custom Graph constructor"""

from typing import Callable

from rdflib import RDF, RDFS

from rdflib_plus import Graph


def test_init():
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


def test_add_model():
    """Test Graph's add_model() method."""

    # Define a custom constructor
    def __init__(self, graph, **kwargs):
        return object().__init__()

    A = type("A", (), {"__init__": __init__})

    # Initialize graph
    graph = Graph()

    # Add constructor
    graph.add_model(A)

    # Check constructor was added to Graph as a method
    assert hasattr(graph, "A")
    assert isinstance(graph.A, Callable)
    assert isinstance(graph.A(), A)


def test_add_models():
    """Test Graph's add_models() method."""

    # Define custom constructors
    def __init__(self, graph, **kwargs):
        return object().__init__()

    A = type("A", (), {"__init__": __init__})
    B = type("B", (), {"__init__": __init__})
    C = type("C", (), {"__init__": __init__})

    # Initialize graph
    graph = Graph()

    # Add constructors
    models = [A, B, C]
    graph.add_models(models)

    # For every model
    for model in models:
        # Get its name
        model_name = model.__name__

        # Check respective constructor was added to Graph as a method
        assert hasattr(graph, model_name)
        constructor = getattr(graph, model_name)
        assert isinstance(constructor, Callable)
        assert isinstance(constructor(), model)


def test_load():
    """Test Graph's load() method."""
    pass


def test_save():
    """Test Graph's save() method."""
    pass
