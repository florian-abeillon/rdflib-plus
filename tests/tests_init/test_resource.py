"""Test Resource constructor"""

import pytest
from rdflib import DCTERMS, RDF, RDFS, XSD, Literal
from rdflib import URIRef as IRI
from rdflib_plus import SimpleGraph
from tests.parameters import (
    PARAMETERS_IDENTIFIERS,
    PARAMETERS_LABELS,
    PARAMETERS_LANGS,
    PARAMETERS_PATHS,
    PARAMETERS_RESOURCE,
)
from tests.tests_init.utils import check_init_labeled_object
from tests.utils import (
    build_iri,
    cartesian_product,
    check_attributes,
    check_graph_triples,
)

# TODO: Test constraints


@pytest.mark.parametrize(
    "identifier,legal_identifier,datatype", PARAMETERS_IDENTIFIERS
)
def test_init_resource_with_identifier(
    identifier: str | int,
    legal_identifier: str,
    datatype: IRI,
):
    """Test Resource creation with identifier."""

    # Set kwargs to be used by constructor
    kwargs = {"identifier": identifier}

    # Format identifier
    identifier = Literal(identifier, datatype=datatype)

    # Test constructor
    _ = check_init_labeled_object(
        *PARAMETERS_RESOURCE,
        identifier,
        legal_identifier,
        kwargs,
    )


@pytest.mark.parametrize(
    "identifier,legal_identifier,datatype,label,legal_label,label_camel_case,"
    "legal_label_camel_case,label_pascal_case,legal_label_pascal_case",
    cartesian_product(PARAMETERS_IDENTIFIERS, PARAMETERS_LABELS),
)
def test_init_resource_with_identifier_and_label(
    identifier: str | int,
    legal_identifier: str,
    datatype: IRI,
    label: str,
    legal_label: str,
    label_camel_case: str,
    legal_label_camel_case: str,
    label_pascal_case: str,
    legal_label_pascal_case: str,
):
    """Test Resource creation with identifier and label."""

    # Set kwargs to be used by constructor
    kwargs = {"identifier": identifier, "label": label}

    # Format identifier
    identifier = Literal(identifier, datatype=datatype)
    label = Literal(label, datatype=XSD.string)

    # Test constructor
    _ = check_init_labeled_object(
        *PARAMETERS_RESOURCE,
        identifier,
        legal_identifier,
        kwargs=kwargs,
        label=label,
    )


@pytest.mark.parametrize(
    "identifier,legal_identifier,datatype,label,legal_label,label_camel_case,"
    "legal_label_camel_case,label_pascal_case,legal_label_pascal_case,lang",
    cartesian_product(
        PARAMETERS_IDENTIFIERS, PARAMETERS_LABELS, PARAMETERS_LANGS
    ),
)
def test_init_resource_with_identifier_and_label_and_lang(
    identifier: str | int,
    legal_identifier: str,
    datatype: IRI,
    label: str,
    legal_label: str,
    label_camel_case: str,
    legal_label_camel_case: str,
    label_pascal_case: str,
    legal_label_pascal_case: str,
    lang: str,
):
    """Test Resource creation with identifier, label and language."""

    # Set kwargs to be used by constructor
    kwargs = {"identifier": identifier, "label": label, "lang": lang}

    # Format identifier
    identifier = (
        Literal(identifier, lang=lang)
        if datatype == XSD.string
        else Literal(identifier, datatype=datatype)
    )
    label = Literal(label, lang=lang)

    # Test constructor
    _ = check_init_labeled_object(
        *PARAMETERS_RESOURCE,
        identifier,
        legal_identifier,
        kwargs=kwargs,
        label=label,
    )


@pytest.mark.parametrize(
    "identifier,legal_identifier,datatype", PARAMETERS_IDENTIFIERS
)
def test_init_resource_with_iri(
    identifier: str | int,
    legal_identifier: str,
    datatype: IRI,
):
    """Test Resource creation with iri."""

    # Get Resource model
    model, model_name, model_type, properties = PARAMETERS_RESOURCE

    # Build IRI from elements
    iri = build_iri(legal_identifier)

    # Initialize graph, and create Resource object
    graph = SimpleGraph()
    resource = model(graph, iri=iri)

    # Check attributes
    check_attributes(
        resource,
        iri=iri,
        path=[model_name],
        type=model_type,
        identifier_property=DCTERMS.identifier,
        properties=properties,
    )

    # Define triples to look for
    triples = [
        (
            iri,
            RDF.type,
            RDFS.Resource,
        ),
    ]

    # Check that all triples are in the graph
    check_graph_triples(graph, triples, exact=True)


@pytest.mark.parametrize("path,path_joined", PARAMETERS_PATHS)
def test_init_resource_with_path(path: list[str], path_joined: str):
    """Test Resource creation with a path."""

    # Arbitrarily select first identifier
    identifier, legal_identifier, datatype = PARAMETERS_IDENTIFIERS[0]

    # Set kwargs to be used by constructor
    kwargs = {"identifier": identifier, "path": path}

    # Format identifier
    identifier = Literal(identifier, datatype=datatype)

    # Test constructor
    _ = check_init_labeled_object(
        *PARAMETERS_RESOURCE,
        identifier,
        legal_identifier,
        kwargs,
        path=path,
        path_joined=path_joined,
    )
