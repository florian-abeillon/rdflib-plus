"""Useful function to load data files into Python"""

from pathlib import Path

import yaml
from yaml.loader import Loader


def get_path_to_dir(file: str) -> str:
    """Get absolute path to file's parent directory.

    Args:
        file (str):
            File in the target directory.

    Returns:
        str: Absolute path to file's parent directory.
    """

    return Path(file).parent.resolve()


def parse_yaml(path_to_file: str) -> dict:
    """Parse YAML file into Python dict.

    Args:
        path_to_file (str):
            Path to the YAML file to parse.

    Returns:
        dict: Parsed YAML file.
    """

    # Parse YAML file
    with open(path_to_file, encoding="utf-8") as f:
        dictionary = yaml.load(f, Loader=Loader)

    return dictionary
