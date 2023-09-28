"""rdflib_plus/utils/parse.py"""

import os
from typing import Any, Optional

import yaml
from rdflib import Literal, Namespace, URIRef
from yaml.loader import Loader

from .namespaces import PREFIXES


def normalize_value(
    value: dict | list | Any,
    normalize_keys: bool = False,
    namespace: Optional[Namespace] = None,
) -> dict | list | URIRef | Literal:
    """
    Replace potential prefix into full namespace IRIs
    """

    # If dict, normalize (keys and) values
    if isinstance(value, dict):
        return {
            normalize_value(key, namespace=namespace)
            if normalize_keys
            else key: normalize_value(v, namespace=namespace)
            for key, v in value.items()
        }

    # If list, normalize each element
    if isinstance(value, list):
        return [normalize_value(v, namespace=namespace) for v in value]

    if isinstance(value, str) and ":" in value:
        for ns, prefix in PREFIXES.items():
            # If a prefix is found
            if value.startswith(f"{prefix}:"):
                # Replace it by full namespace IRI
                value = value[len(prefix) + 1 :]
                return ns[value]

        # If IRI
        if value.startswith("http://"):
            return URIRef(value)

    # If a namespace is specified
    if namespace:
        return namespace[value]

    return Literal(value)


def parse_yaml(
    filename: str,
    __file__: str,
    normalize: bool = False,
    normalize_keys: bool = False,
    namespace: Optional[Namespace] = None,
) -> dict:
    """
    Parse yaml into dict
    """

    # Get current directory
    path = os.path.dirname(__file__)
    path_to_file = os.path.join(path, filename)

    # Parse yaml
    with open(path_to_file) as f:
        d = yaml.load(f, Loader=Loader)

    # Replace prefixes by full namespace IRIs, if required
    if normalize:
        d = normalize_value(
            d, normalize_keys=normalize_keys, namespace=namespace
        )

    return d
