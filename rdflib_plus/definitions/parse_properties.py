"""Functions to parse Property definition files"""

from rdflib import URIRef as IRI

from rdflib_plus.definitions.constraints import CONSTRAINTS_OBJECTS
from rdflib_plus.definitions.utils import (
    parse_definition_file,
    parse_prefixed_iri,
)


def parse_property_constraints(
    constraints: dict[str, str | int]
) -> dict[str, IRI | int]:
    """Parse property constraints, as defined in YAML file.

    Args:
        constraints (dict[str, str | int]):
            Property constraints to parse.

    Returns:
        dict[str, IRI | int]: Parsed property constraints.
    """

    # Initialize parsed constraints
    constraints_parsed = {}

    # For every constraint
    for constraint, value in constraints.items():
        # Get its associated process to apply to value
        process = CONSTRAINTS_OBJECTS[constraint]

        # Add it to the parsed constraints dictionary
        constraints_parsed[constraint] = (
            process(value) if process is not None else value
        )

    return constraints_parsed


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
