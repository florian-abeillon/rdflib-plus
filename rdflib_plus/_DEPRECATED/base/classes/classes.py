"""Define constraints of standard RDFS classes"""

from rdflib import RDFS

from ...utils import parse_yaml

CONSTRAINTS_BASE_CLASSES = parse_yaml(
    "classes.yaml", __file__, normalize=True, normalize_keys=True
)

ignored_properties = CONSTRAINTS_BASE_CLASSES[RDFS.Resource]["properties"]

for class_ in CONSTRAINTS_BASE_CLASSES:
    if class_ == RDFS.Resource:
        continue

    # Add Resource's properties to class's ignored properties
    CONSTRAINTS_BASE_CLASSES[class_]["ignored_properties"] = ignored_properties


IGNORED_PROPERTIES = (
    ignored_properties + CONSTRAINTS_BASE_CLASSES[RDFS.Class]["properties"]
)
