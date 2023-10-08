"""Load and parse RDF Property definition file"""

from rdflib_plus.definitions.properties.parse import (
    parse_property_definition_file,
)
from rdflib_plus.utils.load import get_path_to_dir

# Get absolute path to current directory
path_to_dir = get_path_to_dir(__file__)

# Parse Property YAML file
path_to_properties = path_to_dir / "definition_properties.yaml"
RDF_PROPERTIES = parse_property_definition_file(path_to_properties)


__all__ = [
    "RDF_PROPERTIES",
    "parse_property_definition_file",
]
