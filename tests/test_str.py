"""Test Resource stringify"""

import pytest
from rdflib import URIRef as IRI

from rdflib_plus import SimpleGraph
from tests.parameters import (
    PARAMETERS_IDENTIFIERS,
    PARAMETERS_LABELED_OBJECTS,
    PARAMETERS_LABELS,
)
from tests.utils import (
    build_iri,
    cartesian_product,
    check_attributes,
    check_graph_triples,
)

# @pytest.mark.parametrize(
#     "model,model_name,model_type", PARAMETERS_LABELED_OBJECTS
# )
# def test_str_model_with_label(model: type, model_name: str, model_type: IRI):
#     """Test str() result on Resource initialized with label."""

#     # Initialize graph, and create object
#     graph = SimpleGraph()
#     resource = model(graph)

#     # Check str() result
#     assert str(resource) == f":{model_name}#{resource.id}"
