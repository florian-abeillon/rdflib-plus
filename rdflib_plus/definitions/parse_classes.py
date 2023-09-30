"""Functions to parse Class definition files"""

from typing import Optional

from rdflib import URIRef as IRI

from rdflib_plus.definitions.utils import (
    parse_definition_file,
    parse_identifier_property,
    parse_prefixed_iri,
)


def parse_class_constraints(
    constraints: dict[str, Optional[str]]
) -> dict[IRI, Optional[IRI]]:
    """Parse class property constraints, as defined in YAML file.

    Args:
        constraints (dict[str, Optional[str]]):
            Property constraints to parse.

    Returns:
        dict[IRI, Optional[IRI]]: Parsed property constraints.
    """

    return {
        parse_prefixed_iri(property_): parse_prefixed_iri(constraint)
        for property_, constraint in constraints.items()
    }


# Define legal fields in definition file
# and their respective processes to parse their values
PARSING_PROCESSES_CLASS = {
    "bnode": None,
    "constraints": parse_class_constraints,
    "identifier_property": parse_identifier_property,
    "properties": parse_prefixed_iri,
    "super_class": parse_prefixed_iri,
}


def parse_class_definition_file(
    path: str, properties: Optional[dict] = None
) -> dict[IRI, dict]:
    """Parse Class definition file into Python dictionary.

        Args:
            path (str):
                Path to Class definition file to parse.
            properties (Optional[dict], optional):
                Parsed Class definition dictionary. Defaults to None.

    Returns:
        dict[IRI, dict]: Parsed Class definition dictionary.
    """

    # Parse definition file
    classes = parse_definition_file(path, PARSING_PROCESSES_CLASS)

    # For every class
    for class_definition in classes.values():
        # Pop class's constraints (if any), and restructure them
        class_constraints = class_definition.pop("constraints", {})
        class_constraints = {
            property_iri: {"class": property_constraint}
            for property_iri, property_constraint in class_constraints
        }

        # If properties are specified
        if properties is not None:
            # Pop class's properties (if any)
            class_properties = class_definition.pop("properties", [])

            # Add class's properties constraints, as defined in properties
            # and update them with class's constraints (if any)
            for property_iri in class_properties:
                class_constraints[property_iri] = properties[property_iri][
                    "constraints"
                ] | class_constraints.get(property_iri, {})

        # Update class's property constraints
        class_definition["constraints"] = class_constraints

    return classes
