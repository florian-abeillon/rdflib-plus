from collections import OrderedDict
from types import SimpleNamespace

from rdflib import Graph
from utils import DEFAULT_NAMESPACE, parse_yaml

from ..base import IGNORED_PROPERTIES
from ..models import Class, Instance

config = parse_yaml(
    "classes.yaml", __file__, normalize=True, namespace=DEFAULT_NAMESPACE
)

# Sort config in appropriate way for superclass/subclass linking
# WARNING: Robust only for one-level-deep dependencies
config = OrderedDict(config)
keys = list(config.keys())
idx_superclass = [
    keys.index(kwargs["superclass"].fragment) if "superclass" in kwargs else -1
    for kwargs in config.values()
]
config = OrderedDict(
    {k: v for _, (k, v) in sorted(zip(idx_superclass, config.items()))}
)


# Initialize graph to initialize classes into
GRAPH_CLASSES = Graph()
classes, class_instances = {}, {}
CONSTRAINTS_CLASSES = {}

for label, kwargs in config.items():
    # Pop and format superclass
    superclass = kwargs.pop("superclass", None)
    if superclass:
        superclass = Class.format_fragment(superclass).fragment
        superclass = classes[superclass]

    # Create class object
    class_ = Class(label=label, graph=GRAPH_CLASSES, super_class=superclass)

    # Update class-formatted label
    label = class_.fragment
    classes[label] = class_

    # Add ignored properties, and save constraints for class
    bnode = kwargs.pop("bnode", False)
    kwargs["ignored_properties"] = IGNORED_PROPERTIES
    label_id = kwargs.pop("label_id", Class._identifier_property)
    CONSTRAINTS_CLASSES[label] = kwargs

    # Create instances of this class
    class_instances[label] = type(
        label,
        (Instance,),
        {"_type": class_, "_label_id": label_id, "_bnode": bnode},
    )

# Create a namespace for classes
classes = SimpleNamespace(**class_instances)
