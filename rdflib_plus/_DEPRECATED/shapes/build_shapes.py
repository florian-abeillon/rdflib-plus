from rdflib import RDF, RDFS, SH, BNode, Graph, Literal, URIRef

from ..models import Class, Property
from ..utils import DEFAULT_NAMESPACE, SHAPES_NAMESPACE


def init_shape(label: str) -> tuple[URIRef, URIRef]:
    """
    Initialize SHACL shape
    """

    # Get target class and label
    if isinstance(label, URIRef):
        target_class = label
        label = label.fragment
    else:
        target_class = DEFAULT_NAMESPACE[label]

    shape = SHAPES_NAMESPACE[label]

    return shape, target_class


def build_property_shapes(graph: Graph, label: str, constraints: dict) -> None:
    """
    Build SHACL shape for data validation of properties
    """

    # Create and initialize shape
    shape, target_class = init_shape(label)

    graph.add((shape, SH.path, target_class))
    graph.add((shape, RDF.type, SH.PropertyShape))

    # Limit attributes to one instance
    if SH.datatype in constraints:
        graph.add((shape, SH.maxCount, 1))

    # For every constraint
    for constraint, value in constraints.items():
        if isinstance(value, URIRef):
            value = Class.format_fragment(value)

        # Add it to property
        if not isinstance(value, list):
            graph.add((shape, SH[constraint], value))

        # If list of values, put them in a sh:or statement
        else:
            # Create Blank node to link the sh:or to
            bn_or = BNode()
            graph.add((shape, SH["or"], bn_or))
            collection = graph.collection(bn_or)

            # Fill in the list
            for v in value:
                bn = BNode()
                graph.add((bn, SH[constraint], v))
                collection.append(bn)


def build_class_shapes(
    graph: Graph,
    label: str,
    properties: list = [],
    constraints: dict = {},
    ignored_properties: list[URIRef] = [],
) -> None:
    """
    Build SHACL shape for data validation of classes
    """

    # Create and initialize shape
    shape, target_class = init_shape(label)

    graph.add((shape, SH.targetClass, target_class))
    graph.add((shape, RDF.type, SH.NodeShape))

    # TODO: To fix
    # If not a base class
    if label != RDFS.Resource:
        graph.add((shape, SH.closed, Literal(True)))

    # For every predicate
    for property_ in properties:
        property_ = property_.fragment

        # Initialize property attribute
        label_shape = Property.format_fragment(property_).fragment
        property_shape = SHAPES_NAMESPACE[label_shape]

        # If a specific class is specified
        if property_ in constraints:
            # Create a Blank node subject to the same triples as PropertyShape
            bn = BNode()
            for p, o in graph.predicate_objects(property_shape):
                if p in [RDF.type, SH.targetClass]:
                    continue
                graph.add((bn, p, o))

            # Add class constraint
            constraint = Class.format_fragment(constraints[property_])
            graph.add((bn, SH["class"], constraint))
            property_shape = bn

        graph.add((shape, SH.property, property_shape))

    # If some properties need to be ignored
    if ignored_properties:
        # Create Blank node to link the ignored properties to
        bn = BNode()
        graph.add((shape, SH.ignoredProperties, bn))
        collection = graph.collection(bn)

        # Fill in the ignored properties
        collection += ignored_properties
