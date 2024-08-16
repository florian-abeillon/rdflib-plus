from rdflib import SH, Graph

from ..base import CONSTRAINTS_BASE_CLASSES, CONSTRAINTS_BASE_PROPERTIES
from ..classes import CONSTRAINTS_CLASSES
from ..properties import CONSTRAINTS_PROPERTIES
from ..utils import SHAPES_NAMESPACE
from .build_shapes import build_class_shapes, build_property_shapes


def build_shapes_graph() -> Graph:
    """
    Build shape graph for data validation
    """

    # Initialize shapes graph
    graph = Graph()
    graph.bind("sh", SH)
    graph.bind("shapes", SHAPES_NAMESPACE)

    # Add shape for every property
    constraints_properties = list(CONSTRAINTS_BASE_PROPERTIES.items()) + list(
        CONSTRAINTS_PROPERTIES.items()
    )

    for label, constraints in constraints_properties:
        build_property_shapes(graph, label, constraints)

    # Add shape for every class
    constraints_classes = list(CONSTRAINTS_BASE_CLASSES.items()) + list(
        CONSTRAINTS_CLASSES.items()
    )

    for label, kwargs in constraints_classes:
        build_class_shapes(graph, label, **kwargs)

    return graph
