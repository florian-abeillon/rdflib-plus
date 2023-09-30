"""Load and parse definition YAML files"""

from rdflib_plus.definitions.parse_classes import parse_class_definition_file
from rdflib_plus.definitions.parse_properties import (
    parse_property_definition_file,
)
from rdflib_plus.utils.load import get_path_to_dir

# Get absolute path to current directory
path_to_dir = get_path_to_dir(__file__)

# Parse Property YAML file
path_to_properties = path_to_dir / "definition_properties.yaml"
RDF_PROPERTIES = parse_property_definition_file(path_to_properties)

# Parse Class YAML file
path_to_classes = path_to_dir / "definition_classes.yaml"
RDFS_CLASSES = parse_class_definition_file(
    path_to_classes, properties=RDF_PROPERTIES
)
