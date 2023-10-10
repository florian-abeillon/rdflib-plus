"""Functions to parse definition files"""

from typing import Callable, Optional

from langcodes import standardize_tag
from rdflib import URIRef as IRI

from rdflib_plus.namespaces import parse_prefixed_iri
from rdflib_plus.utils import parse_yaml


def copy_key_value_if_exists(
    key: str,
    dict_from: dict,
    dict_to: dict,
    process: Optional[Callable] = None,
) -> None:
    """Copy (processed) value from dict_from to dict_to,
       if dict_from has key.

    Args:
        key (str):
            Key to look for.
        dict_from (dict):
            Dictionary in which to look key in.
        dict_to (dict):
            Dictionary where key-value should be added.
        process (Optional[Callable], optional):
            Process to apply to value. Defaults to None.
    """

    # Look for key in dict_from
    try:
        value = dict_from[key]
    except KeyError:
        return None

    # Add processed value to dict_to, with te same key
    dict_to[key] = process(value) if process is not None else value

    return None


def parse_identifier_property(
    identifier_property: str | dict[str, str]
) -> IRI | dict[str, IRI]:
    """Parse classes' specified identifier property.

    Args:
        identifier_property (str | dict[str, str]):
            Property (or dictionary of language code to property) that links
            Class to its identifier.

    Returns:
        IRI | dict[str, IRI]: Parsed property or dictionary of properties.
    """

    # If identifier_property is a single property, parse it as IRI
    if isinstance(identifier_property, str):
        return parse_prefixed_iri(identifier_property)

    # Otherwise, format each language code
    # and parse their respective values as IRI
    return {
        standardize_tag(lang): parse_prefixed_iri(property_)
        for lang, property_ in identifier_property.items()
    }


def parse_definition_file(
    path: str, definition_fields: dict[str, Optional[Callable]]
) -> dict[IRI, dict]:
    """Parse definition dictionary.

        Args:
            path (str):
                Path to definition file to parse.
            definition_fields (dict[str, Optional[Callable]]):
                Possible definition fields, and their associated process
                to apply to their values.

    Returns:
        dict[IRI, dict]: Parsed definition dictionary.
    """

    # Parse file
    dictionary = parse_yaml(path)

    # Initialize parsed dictionary
    dictionary_parsed = {}

    for prefixed_iri, values in dictionary.items():
        # Parse IRI of RDFS Class
        iri = parse_prefixed_iri(prefixed_iri)

        # Initialize parsed values dictionary
        values_parsed = {}

        # Add possible key-values (if exist)
        for field, process in definition_fields.items():
            copy_key_value_if_exists(
                field, values, values_parsed, process=process
            )

        # Add parsed value
        dictionary_parsed[iri] = values_parsed

    return dictionary_parsed


def parse_constraints(
    constraints: dict[str, str | int],
    is_class: bool = False,
    constraint_processes: Optional[dict[str, Callable]] = None,
) -> dict[str, IRI | int]:
    """Parse constraints, as defined in YAML file.

    Args:
        constraints (dict[str, str | int]):
            Constraints to parse.
        is_class (bool, optional):
            Whether constraints are a class's. Defaults to False.
        constraint_processes (Optional[dict[str, Callable]], optional):
            Dictionary of constraints to their associated process.

    Returns:
        dict[str, IRI | int]: Parsed constraints.
    """

    # Initialize parsed constraints
    constraints_parsed = {}

    # TODO: Necessary for SHACL graph construction?
    # def parse_add_constraint(constraint: str, value: str | int) -> None:
    #     """Parse and add constraint to constraints_parsed.

    #     Args:
    #         constraint (str):
    #             Name of the constraint to parse and add.
    #         value (str | int):
    #             Value of the constraint.
    #     """

    #     # Get its associated process to apply to value
    #     process = CONSTRAINTS_OBJECTS[constraint]

    #     # Add it to the parsed constraints dictionary
    #     constraints_parsed[constraint] = (
    #         process(value) if process is not None else value
    #     )

    # # For every constraint
    # for constraint, value in constraints.items():
    #     # If constraint is 'unique'
    #     # Translate it into 'minCount'/'maxCount'
    #     if constraint == "unique" and value is True:
    #         parse_add_constraint("minCount", 1)
    #         parse_add_constraint("maxCount", 1)

    #     # Otherwise, parse and add constraint
    #     else:
    #         parse_add_constraint(constraint, value)

    # For every constraint
    for constraint, values in constraints.items():
        # If constraint has only one value
        if not isinstance(values, list):
            # Turn value into a list
            values = [values]

        # If constraints to parse are classes'
        if is_class:
            # Parse constraint into IRI
            constraint = parse_prefixed_iri(constraint)
            # Define process to parse values
            process = parse_prefixed_iri

        # Otherwise, if constraints to parse are properties'
        else:
            # Get its associated process to apply to value
            process = constraint_processes[constraint]

        # If a process is specified
        if process is not None:
            # Apply process to every value
            values = [process(value) for value in values]

        # Add it to the parsed constraints dictionary
        constraints_parsed[constraint] = values

    return constraints_parsed
