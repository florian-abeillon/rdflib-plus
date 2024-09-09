"""Test blank node object constructors"""

import pytest
from rdflib import DCTERMS, Namespace
from rdflib import URIRef as IRI

from rdflib_plus import DEFAULT_NAMESPACE
from tests.parameters import (
    PARAMETERS_BLANK_NODE_OBJECTS,
    PARAMETERS_NAMESPACES,
)
from tests.tests_init.utils import check_init_blank_node_object
from tests.utils import cartesian_product


@pytest.mark.parametrize(
    "model, model_name, model_type, properties", PARAMETERS_BLANK_NODE_OBJECTS
)
def test_init_blank_node_object(
    model: type, model_name: str, model_type: IRI, properties: set[IRI]
):
    """Test blank node object creation."""

    # Test constructor
    _ = check_init_blank_node_object(model, model_name, model_type, properties)


@pytest.mark.parametrize(
    "model, model_name, model_type, properties, namespace, local",
    cartesian_product(
        PARAMETERS_BLANK_NODE_OBJECTS, PARAMETERS_NAMESPACES, [True, False]
    ),
)
def test_init_blank_node_object_within_namespace(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    namespace: Namespace,
    local: bool,
):
    """Test blank node object creation within a namespace."""

    # Set kwargs to be used by constructor
    kwargs = {"namespace": namespace, "local": local}

    # Format namespace and set source
    if str(namespace)[-1] != "/":
        namespace = Namespace(f"{namespace}/")
    source = IRI(namespace)
    if not local:
        namespace = DEFAULT_NAMESPACE

    # Set additional triples
    triples_add = [(DCTERMS.source, source)]

    # Test constructor
    _ = check_init_blank_node_object(
        model,
        model_name,
        model_type,
        properties,
        kwargs=kwargs,
        namespace=namespace,
        triples_add=triples_add,
    )
