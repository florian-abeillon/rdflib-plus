from types import SimpleNamespace

from rdflib import Graph
from utils import parse_yaml

from ..models import Property

config = parse_yaml("properties.yaml", __file__, normalize=True)


# Initialize graph to initialize properties into
GRAPH_PROPERTIES = Graph()
properties = {}
CONSTRAINTS_PROPERTIES = {}

for label, kwargs in config.items():
    # Get constraints and infer superproperty
    constraints = kwargs.pop("constraints")
    superproperty = kwargs.pop("superproperty", None)

    # Create property object
    property_ = Property(
        label=label,
        graph=GRAPH_PROPERTIES,
        super_property=superproperty,
        **kwargs
    )

    # Update property-formatted label
    label = property_.fragment
    properties[label] = property_
    CONSTRAINTS_PROPERTIES[label] = constraints

# Create a namespace for properties
props = SimpleNamespace(**properties)
