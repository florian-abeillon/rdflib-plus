"""Useful functions to parse data files"""

from pathlib import Path

import yaml
from yaml.loader import Loader


def parse_yaml(path_to_file: str) -> dict:
    """Parse yaml file into Python dict.

    Args:
        path_to_file (str):
            Path to the yaml file to parse.

    Returns:
        dict: Parsed yaml file.
    """

    # Parse yaml file
    with open(path_to_file, encoding="utf-8") as f:
        dictionary = yaml.load(f, Loader=Loader)

    return dictionary


def parse_local_yaml(filename: str) -> dict:
    """Parse yaml file into Python dict.

    Args:
        filename (str):
            Name of the yaml file to parse.

    Returns:
        dict: Parsed yaml file.
    """

    # Get absolute path to file
    path = Path(filename).resolve()

    return parse_yaml(path)
