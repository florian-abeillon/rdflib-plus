"""Test SimpleGraph constructor"""

from typing import Callable, Optional

import pytest
from rdflib import DCTERMS, OWL, RDF, RDFS, SKOS, XSD, Literal

from rdflib_plus import (
    Alt,
    Bag,
    Class,
    FunctionalProperty,
    InverseFunctionalProperty,
    List,
    NaryProperty,
    Ontology,
    Property,
    PropertyWithAttributes,
    Resource,
    Seq,
    SimpleGraph,
    SymmetricProperty,
    TransitiveProperty,
)


@pytest.mark.parametrize(
    "model,label",
    [
        (Alt, None),
        (Bag, None),
        (Class, "ClassLabel"),
        (FunctionalProperty, "functionalPropertyLabel"),
        (InverseFunctionalProperty, "inverseFunctionalPropertyLabel"),
        (List, None),
        (NaryProperty, "naryPropertyLabel"),
        (Ontology, "OntologyLabel"),
        (Property, "propertyLabel"),
        (PropertyWithAttributes, "propertyWithAttributesLabel"),
        (Resource, None),
        (Seq, None),
        (SymmetricProperty, "symmetricPropertyLabel"),
        (TransitiveProperty, "transitivePropertyLabel"),
    ],
)
def test_init(model: type, label: Optional[str]):
    """Test SimpleGraph object creation."""

    # Initialize graph
    graph = SimpleGraph()

    # Check attributes
    assert hasattr(graph, model.__name__)
    graph_model = getattr(graph, model.__name__)
    assert isinstance(graph_model, Callable)

    # Create RDFS Resource from graph
    args = (label,) if label is not None else ()
    resource = graph_model(*args)

    # Check adequate triples (and no others) are in graph
    triples = [
        (
            resource.iri,
            RDF.type,
            resource.type,
        ),
    ]
    if label is not None:
        if resource.type == OWL.Ontology:
            triples.append(
                (resource.iri, RDFS.label, Literal(label, datatype=XSD.string))
            )
        else:
            triples += [
                (
                    resource.iri,
                    SKOS.prefLabel,
                    Literal(label, datatype=XSD.string),
                ),
                (
                    resource.iri,
                    DCTERMS.identifier,
                    Literal(label, datatype=XSD.string),
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
    graph = SimpleGraph()

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
    graph = SimpleGraph()

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

    # TODO


def test_save():
    """Test Graph's save() method."""

    # TODO
