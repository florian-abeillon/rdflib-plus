"""Functions to parse Class definition files"""

from typing import Optional

from rdflib import URIRef as IRI

from rdflib_plus.definitions.utils import (
    parse_constraints,
    parse_definition_file,
)
from rdflib_plus.namespaces import parse_prefixed_iri


def parse_class_properties(properties: list[str]) -> list[IRI]:
    """Parse a class's properties.

    Args:
        properties (list[str]):
            Class's properties, as strings.

    Returns:
        list[IRI]: Parsed class's properties.
    """

    return [parse_prefixed_iri(property_) for property_ in properties]


def parse_identifier_property(
    identifier_property: str | list[str],
) -> IRI | list[IRI]:
    """Parse a class's identifier property/ies.

    Args:
        identifier_property (str | list[str]):
            Class's specific identifier property or properties.

    Returns:
        IRI | list[IRI]: Parsed identifier property/ies.
    """

    # If there are several identifier properties
    if isinstance(identifier_property, list):
        # Parse each one of them
        return parse_class_properties(identifier_property)

    return parse_prefixed_iri(identifier_property)


def parse_class_constraints(
    constraints: dict[str, str | int]
) -> dict[str, IRI | int]:
    """Parse a class's property constraints, as defined in YAML file.

    Args:
        constraints (dict[str, str | int]):
            Constraints to parse.

    Returns:
        dict[str, IRI | int]: Parsed constraints.
    """

    return parse_constraints(constraints, is_class=True)


# Define legal fields in definition file
# and their respective processes to parse their values
PARSING_PROCESSES_CLASS = {
    "bnode": None,
    "constraints": parse_class_constraints,
    "identifier_property": parse_identifier_property,
    "properties": parse_class_properties,
    "super_class": parse_prefixed_iri,
}


def parse_class_definition_file(
    path: str, properties: Optional[dict] = None
) -> dict[IRI, dict]:
    """Parse Class definition file into Python dictionary.

        Args:
            path (str):
                Path to Class definition file to parse.
            properties (dict | None, optional):
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
            for property_iri, property_constraint in class_constraints.items()
        }

        # If properties are specified
        if properties is not None:
            # Pop class's properties (if any)
            class_properties = class_definition.pop("properties", [])

            # Add class's properties constraints, as defined in properties
            # and update them with class's constraints (if any)
            for property_iri in class_properties:
                class_constraints[property_iri] = (
                    class_constraints[property_iri]
                    if property_iri in class_constraints
                    else properties[property_iri].get("constraints", {})
                )

        # Update class's property constraints
        class_definition["constraints"] = class_constraints

    return classes
