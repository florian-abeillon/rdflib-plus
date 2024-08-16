"""Test labeled object constructors"""

import pytest
from rdflib import DCTERMS, XSD, Literal, Namespace
from rdflib import URIRef as IRI

from rdflib_plus import DEFAULT_NAMESPACE
from tests.parameters import (
    PARAMETERS_LABELED_OBJECTS,
    PARAMETERS_LABELS,
    PARAMETERS_LANGS,
    PARAMETERS_NAMESPACES,
)
from tests.tests_init.utils import check_init_labeled_object, get_label
from tests.utils import cartesian_product


@pytest.mark.parametrize(
    "model,model_name,model_type,properties,camel_case,pascal_case,"
    "label,legal_label,label_camel_case,legal_label_camel_case,"
    "label_pascal_case,legal_label_pascal_case",
    cartesian_product(PARAMETERS_LABELED_OBJECTS, PARAMETERS_LABELS),
)
def test_init_labeled_object_with_label(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    camel_case: bool,
    pascal_case: bool,
    label: str,
    legal_label: str,
    label_camel_case: str,
    legal_label_camel_case: str,
    label_pascal_case: str,
    legal_label_pascal_case: str,
):
    """Test labeled object creation with label."""

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

    # Set kwargs to be used by constructor
    kwargs = {"label": label_formatted}

    # Format identifier and label
    identifier = Literal(label_formatted, datatype=XSD.string)
    label = Literal(label_formatted, datatype=XSD.string)
    legal_identifier = legal_label_formatted

    # Test constructor
    _ = check_init_labeled_object(
        model,
        model_name,
        model_type,
        properties,
        identifier,
        legal_identifier,
        kwargs,
        sep=sep,
        label=label,
    )


@pytest.mark.parametrize(
    "model,model_name,model_type,properties,camel_case,pascal_case,lang",
    cartesian_product(PARAMETERS_LABELED_OBJECTS, PARAMETERS_LANGS),
)
def test_init_labeled_object_with_label_lang(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    camel_case: bool,
    pascal_case: bool,
    lang: str,
):
    """Test labeled object creation with label and language."""

    # Arbitrarily select first label
    label, legal_label, sep = get_label(
        camel_case, pascal_case, *PARAMETERS_LABELS[0]
    )

    # Set kwargs to be used by constructor
    kwargs = {"label": label, "lang": lang}

    # Format identifier and label
    identifier = Literal(label, lang=lang)
    label = Literal(label, lang=lang)
    legal_identifier = legal_label

    # Test constructor
    _ = check_init_labeled_object(
        model,
        model_name,
        model_type,
        properties,
        identifier,
        legal_identifier,
        kwargs,
        sep=sep,
        label=label,
    )


@pytest.mark.parametrize(
    "model,model_name,model_type,properties,camel_case,pascal_case,namespace,"
    "local",
    cartesian_product(
        PARAMETERS_LABELED_OBJECTS, PARAMETERS_NAMESPACES, [True, False]
    ),
)
def test_init_labeled_object_within_namespace(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    camel_case: str,
    pascal_case: str,
    namespace: Namespace,
    local: bool,
):
    """Test labeled object creation within a namespace."""

    # Arbitrarily select first label
    label, legal_label, sep = get_label(
        camel_case, pascal_case, *PARAMETERS_LABELS[0]
    )
    legal_identifier = legal_label

    # Set kwargs to be used by constructor
    kwargs = {"label": label, "namespace": namespace, "local": local}

    # Format identifier and label
    identifier = Literal(label, datatype=XSD.string)
    label = Literal(label, datatype=XSD.string)

    # Format namespace and set source
    if str(namespace)[-1] != "/":
        namespace = Namespace(f"{namespace}/")
    source = IRI(namespace)
    if not local:
        namespace = DEFAULT_NAMESPACE

    # Set additional triple
    add_triples = [(DCTERMS.source, source)]

    # Test constructor
    _ = check_init_labeled_object(
        model,
        model_name,
        model_type,
        properties,
        identifier,
        legal_identifier,
        kwargs,
        namespace=namespace,
        sep=sep,
        label=label,
        add_triples=add_triples,
    )
