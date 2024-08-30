"""Test Ontology methods"""

import pytest

from rdflib_plus import Ontology, SimpleGraph
from tests.parameters import PARAMETERS_LABELS
from tests.tests_methods.utils import check_str


# TODO: Test other namespaces
@pytest.mark.parametrize(
    "label, legal_label, label_camel_case, legal_label_camel_case,"
    "label_pascal_case, legal_label_pascal_case",
    PARAMETERS_LABELS,
)
def test_str(
    label: str,
    legal_label: str,
    label_camel_case: str,
    legal_label_camel_case: str,
    label_pascal_case: str,
    legal_label_pascal_case: str,
):
    """Test Ontology's __str__() method."""

    # Initialize graph, and create Ontology
    graph = SimpleGraph()
    ontology = Ontology(graph, label)

    # Check the string representation of the Ontology
    check_str(ontology, "Ontology", legal_label)
