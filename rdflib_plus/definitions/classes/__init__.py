"""Load and parse RDFS Class definition file"""

from rdflib_plus.definitions.classes.parse import parse_class_definition_file
from rdflib_plus.definitions.properties import RDF_PROPERTIES
from rdflib_plus.utils.load import get_path_to_dir

# Get absolute path to current directory
path_to_dir = get_path_to_dir(__file__)

# Parse Class YAML file
path_to_classes = path_to_dir / "definition_classes.yaml"
RDFS_CLASSES = parse_class_definition_file(
    path_to_classes, properties=RDF_PROPERTIES
)

__all__ = [
    "RDFS_CLASSES",
    "parse_class_definition_file",
]
