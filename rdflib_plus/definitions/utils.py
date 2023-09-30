"""Functions to parse definition files"""

from typing import Callable, Optional

from langcodes import standardize_tag
from rdflib import URIRef as IRI

from rdflib_plus.namespaces import PREFIX_TO_NAMESPACE
from rdflib_plus.utils.load import parse_yaml


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


def parse_prefixed_iri(prefixed_iri: str) -> IRI:
    """Parse prefixed IRI into full IRI.

    Args:
        prefixed_iri (str):
            Prefixed IRI to parse.

    Returns:
        IRI: Full IRI.
    """

    # Add default (empty) namespace if none is specified
    if ":" not in prefixed_iri:
        prefixed_iri = f":{prefixed_iri}"

    # Parse prefix and label
    prefix, label = prefixed_iri.split(":")

    # Build full IRI
    namespace = PREFIX_TO_NAMESPACE(prefix)
    iri = namespace[label]

    return iri


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
        for field, process in definition_fields:
            copy_key_value_if_exists(
                field, values, values_parsed, process=process
            )

        # Add parsed value
        dictionary_parsed[iri] = values_parsed

    return dictionary_parsed
