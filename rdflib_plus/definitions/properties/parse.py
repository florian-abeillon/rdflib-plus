"""Functions to parse Property definition files"""

from rdflib import URIRef as IRI

from rdflib_plus.definitions.utils import (
    parse_constraints,
    parse_definition_file,
)
from rdflib_plus.namespaces import parse_prefixed_iri

CONSTRAINTS_OBJECTS = {
    "class": parse_prefixed_iri,
    "datatype": parse_prefixed_iri,
    "minCount": None,
    "maxCount": None,
    # "unique": None,
}


def parse_property_constraints(
    constraints: dict[str, str | int]
) -> dict[str, IRI | int]:
    """Parse property constraints, as defined in YAML file.

    Args:
        constraints (dict[str, str | int]):
            Constraints to parse.

    Returns:
        dict[str, IRI | int]: Parsed constraints.
    """

    return parse_constraints(
        constraints, is_class=False, constraint_processes=CONSTRAINTS_OBJECTS
    )


# Define legal fields in definition file
# and their respective processes to parse their values
PARSING_PROCESSES_PROPERTY = {
    "constraints": parse_property_constraints,
    "super_property": parse_prefixed_iri,
}


def parse_property_definition_file(path: str) -> dict[IRI, dict]:
    """Parse Property definition file into Python dictionary.

        Args:
            path (str):
                Path to Property definition file to parse.

    Returns:
        dict[IRI, dict]: Parsed Property definition dictionary.
    """

    return parse_definition_file(path, PARSING_PROCESSES_PROPERTY)
