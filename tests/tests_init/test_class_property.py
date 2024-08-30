"""Test Class constructor"""

import random as rd

import pytest
from rdflib import DCTERMS, RDF, RDFS, SKOS, XSD, Literal
from rdflib import URIRef as IRI

from rdflib_plus import Class, Property, SimpleGraph
from tests.parameters import (
    PARAMETERS_CLASS,
    PARAMETERS_LABELS,
    PARAMETERS_PROPERTY,
)
from tests.utils import SEED, cartesian_product, check_graph_triples, get_label

# Set random seed
rd.seed(SEED)


@pytest.mark.parametrize(
    "hierarchical_path, type_in_iri",
    cartesian_product([True, False], [True, False]),
)
def test_init_class_with_hierarchical_path_and_type_in_iri(
    hierarchical_path: bool, type_in_iri: bool
):
    """Test Class creation with super-class."""

    # Initialize graph
    graph = SimpleGraph()

    # Arbitrarily select labels
    labels_class, labels_super_class = rd.sample(PARAMETERS_LABELS, 2)
    (
        label_class,
        legal_label_class,
        label_camel_case_class,
        legal_label_camel_case_class,
        label_pascal_case_class,
        legal_label_pascal_case_class,
    ) = labels_class
    (
        label_super_class,
        legal_label_super_class,
        label_camel_case_super_class,
        legal_label_camel_case_super_class,
        label_pascal_case_super_class,
        legal_label_pascal_case_super_class,
    ) = labels_super_class

    assert (
        legal_label_camel_case_class != legal_label_camel_case_super_class
    ), (
        "Please change labels to intialize class and super-class with, "
        "as they currently have the same CamelCase formatting "
        "(hence the two resources have the same IRI and are thus "
        "considered as the same object)."
    )

    # Create super-class and class
    super_class = Class(
        graph,
        label_super_class,
        type_in_iri=type_in_iri,
    )
    class_ = Class(
        graph,
        label_class,
        super_class=super_class,
        hierarchical_path=hierarchical_path,
        type_in_iri=type_in_iri,
    )

    # Check IRI
    iri = IRI("http://default.example.com/")
    if hierarchical_path:
        if type_in_iri:
            iri += "Class/"
        iri += f"{legal_label_camel_case_super_class}/"
    iri += legal_label_camel_case_class

    # Format labels
    label_class = Literal(label_class, datatype=XSD.string)
    label_super_class = Literal(label_super_class, datatype=XSD.string)

    # Format identifiers
    identifier_class = Literal(label_camel_case_class, datatype=XSD.string)
    identifier_super_class = Literal(
        label_camel_case_super_class, datatype=XSD.string
    )

    # Define triples to look for
    triples = [
        (
            super_class.iri,
            RDF.type,
            RDFS.Class,
        ),
        (
            super_class.iri,
            DCTERMS.identifier,
            identifier_super_class,
        ),
        (
            super_class.iri,
            SKOS.prefLabel,
            label_super_class,
        ),
        (
            iri,
            RDF.type,
            RDFS.Class,
        ),
        (
            iri,
            DCTERMS.identifier,
            identifier_class,
        ),
        (
            iri,
            SKOS.prefLabel,
            label_class,
        ),
        (
            iri,
            RDFS.subClassOf,
            super_class.iri,
        ),
    ]

    # Check that all triples are in the graph
    check_graph_triples(graph, triples, exact=True)


@pytest.mark.parametrize(
    "hierarchical_path, type_in_iri",
    cartesian_product([True, False], [True, False]),
)
def test_init_property_with_hierarchical_path_and_type_in_iri(
    hierarchical_path: bool, type_in_iri: bool
):
    """Test Property creation with super-property."""

    # Initialize graph
    graph = SimpleGraph()

    # Arbitrarily select labels
    labels_property, labels_super_property = rd.sample(PARAMETERS_LABELS, 2)
    (
        label_property,
        legal_label_property,
        label_camel_case_property,
        legal_label_camel_case_property,
        label_pascal_case_property,
        legal_label_pascal_case_property,
    ) = labels_property
    (
        label_super_property,
        legal_label_super_property,
        label_camel_case_super_property,
        legal_label_camel_case_super_property,
        label_pascal_case_super_property,
        legal_label_pascal_case_super_property,
    ) = labels_super_property

    assert (
        legal_label_pascal_case_property
        != legal_label_pascal_case_super_property
    ), (
        "Please change labels to intialize property and super-property with, "
        "as they currently have the same pascalCase formatting "
        "(hence the two resources have the same IRI and are thus "
        "considered as the same object)."
    )

    # Create super-property and property
    super_property = Property(
        graph,
        label_super_property,
        type_in_iri=type_in_iri,
    )
    property = Property(
        graph,
        label_property,
        super_property=super_property,
        hierarchical_path=hierarchical_path,
        type_in_iri=type_in_iri,
    )

    # Check IRI
    iri = IRI("http://default.example.com/")
    if hierarchical_path:
        if type_in_iri:
            iri += "Property/"
        iri += f"{legal_label_pascal_case_super_property}/"
    iri += legal_label_pascal_case_property

    # Format labels
    label_property = Literal(label_property, datatype=XSD.string)
    label_super_property = Literal(label_super_property, datatype=XSD.string)

    # Format identifiers
    identifier_property = Literal(
        label_pascal_case_property, datatype=XSD.string
    )
    identifier_super_property = Literal(
        label_pascal_case_super_property, datatype=XSD.string
    )

    # Define triples to look for
    triples = [
        (
            super_property.iri,
            RDF.type,
            RDF.Property,
        ),
        (
            super_property.iri,
            DCTERMS.identifier,
            identifier_super_property,
        ),
        (
            super_property.iri,
            SKOS.prefLabel,
            label_super_property,
        ),
        (
            iri,
            RDF.type,
            RDF.Property,
        ),
        (
            iri,
            DCTERMS.identifier,
            identifier_property,
        ),
        (
            iri,
            SKOS.prefLabel,
            label_property,
        ),
        (
            iri,
            RDFS.subPropertyOf,
            super_property.iri,
        ),
    ]

    # Check that all triples are in the graph
    check_graph_triples(graph, triples, exact=True)


@pytest.mark.parametrize(
    "model, model_name, model_type, properties, camel_case, pascal_case,"
    "type_in_iri",
    cartesian_product([PARAMETERS_CLASS, PARAMETERS_PROPERTY], [True, False]),
)
def test_init_class_property_with_type_in_iri(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    camel_case: bool,
    pascal_case: bool,
    type_in_iri: bool,
):
    """Test Class and Property creation with super-class."""

    # Initialize graph
    graph = SimpleGraph()

    # Arbitrarily select label
    (
        label,
        legal_label,
        label_camel_case,
        legal_label_camel_case,
        label_pascal_case,
        legal_label_pascal_case,
    ) = rd.choice(PARAMETERS_LABELS)

    class_or_property = model(graph, label, type_in_iri=type_in_iri)

    # Get appropriate label
    label_formatted, legal_label_formatted, sep = get_label(
        camel_case,
        pascal_case,
        label,
        legal_label,
        label_camel_case,
        legal_label_camel_case,
        label_pascal_case,
        legal_label_pascal_case,
    )

    # Check IRI
    iri = IRI("http://default.example.com/")
    if type_in_iri:
        iri += f"{model_name}/"
    iri += legal_label_formatted

    # Format label and identifier
    identifier = Literal(legal_label_formatted, datatype=XSD.string)
    label = Literal(label, datatype=XSD.string)

    # Define triples to look for
    triples = [
        (
            iri,
            RDF.type,
            model_type,
        ),
        (
            iri,
            DCTERMS.identifier,
            identifier,
        ),
        (
            iri,
            SKOS.prefLabel,
            label,
        ),
    ]

    # Check that all triples are in the graph
    check_graph_triples(graph, triples, exact=True)


# TODO: Test for update_constraints
