"""Test Resource, Class and Property constructors"""

import re
from contextlib import nullcontext

import pytest
from rdflib import XSD, Literal
from rdflib import URIRef as IRI

from rdflib_plus import Resource
from tests.parameters import (
    PARAMETERS_CLASS,
    PARAMETERS_LABELS,
    PARAMETERS_PROPERTY,
    PARAMETERS_RESOURCE,
)
from tests.tests_init.utils import check_init_labeled_object
from tests.utils import (
    WARNING_MESSAGE_FORMATTING,
    cartesian_product,
    get_label,
)


@pytest.mark.parametrize(
    "model, model_name, model_type, properties, camel_case, pascal_case,"
    "label, legal_label, label_camel_case, legal_label_camel_case,"
    "label_pascal_case, legal_label_pascal_case, type_in_iri",
    cartesian_product(
        [
            (
                *PARAMETERS_RESOURCE,
                False,
                False,
            ),
            PARAMETERS_CLASS,
            PARAMETERS_PROPERTY,
        ],
        PARAMETERS_LABELS,
        [True, False],
    ),
)
def test_init_with_type_in_iri(
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
    type_in_iri: bool,
):
    """Test Resource, Class and Property creation with super-class."""

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
    kwargs = {"label": label, "type_in_iri": type_in_iri}

    # Format identifier
    identifier = Literal(label_formatted, datatype=XSD.string)
    legal_identifier = legal_label_formatted

    # If label is not well-formatted, expect warning
    with (
        pytest.warns(UserWarning)
        if model != Resource and label != label_formatted
        else nullcontext()
    ) as record:

        # Format label
        label = Literal(label, datatype=XSD.string)

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
            type_in_iri=type_in_iri,
        )

        # If expecting warnings
        if record is not None:
            assert len(record) == 1
            assert WARNING_MESSAGE_FORMATTING.format(
                label, label_formatted
            ) in str(record[0].message)
