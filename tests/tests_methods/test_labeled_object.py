"""Test labeled object methods"""

import pytest
from rdflib import URIRef as IRI

from rdflib_plus import SimpleGraph
from tests.parameters import PARAMETERS_LABELED_OBJECTS, PARAMETERS_LABELS
from tests.tests_methods.utils import check_str
from tests.utils import cartesian_product, get_label


# TODO: Test other namespaces
@pytest.mark.parametrize(
    "model, model_name, model_type, properties, camel_case, pascal_case,"
    "label,legal_label, label_camel_case, legal_label_camel_case,"
    "label_pascal_case, legal_label_pascal_case",
    cartesian_product(PARAMETERS_LABELED_OBJECTS, PARAMETERS_LABELS),
)
def test_str(
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
    """Test labeled objects' __str__() method."""

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

    # Initialize graph, and create labeled_object
    graph = SimpleGraph()
    labeled_object = model(graph, label_formatted)

    # Check the string representation of the labeled_object
    check_str(labeled_object, model_name, legal_label_formatted, sep=sep)
