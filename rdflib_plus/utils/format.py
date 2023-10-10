"""Functions to format labels and identifiers"""

import re
import urllib.parse

from inflection import underscore

# TODO: Find a better way, than hard-coding it here
# Source: https://datatracker.ietf.org/doc/html/rfc3986#section-2.2
ILLEGAL_CHARS_OFFICIAL = ":/?#[]@!$&'()*+,;="
# Source: https://afs.github.io/rdf-iri-syntax.html#notes-iris
ILLEGAL_CHARS_UNOFFICIAL = " {}<>"
ILLEGAL_CHARS_IN_AUTHORITY_ONLY = "@():"

# Get the percent-encoding of URI/IRI illegal characters
ILLEGAL_CHARS_PERCENT_ENCODED = {
    char: urllib.parse.quote(char)
    for char in ILLEGAL_CHARS_OFFICIAL + ILLEGAL_CHARS_UNOFFICIAL
}


def legalize_for_iri(text: str, authority: bool = False) -> str:
    """Make text legal for IRI use.

    Args:
        text (str):
            Text to be used in IRI.
        authority (bool, optional):
            Whether text will be used as authority of an IRI.

    Returns:
        str: Text where any illegal character is percent-encoded.
    """

    # For every IRI illegal character
    for char, char_encoded in ILLEGAL_CHARS_PERCENT_ENCODED.items():
        # If text will not be used as authority
        # And character is legal in path, query and fragment
        # Do not do anything
        if not authority and char in ILLEGAL_CHARS_IN_AUTHORITY_ONLY:
            continue

        # Replace the character by its percent-encoding
        text = text.replace(char, char_encoded)

    return text


def format_label(label: str) -> str:
    """Format label with underscores.

    Args:
        label (str):
            Label to format.

    Returns:
        str: Formatted label.
    """

    # Add underscores between consecutive capitalized letters
    # To ensure all-capitalized words remain that way
    # Even after calling camelize()
    label = re.sub(r"(?<=[A-Z])(?=[A-Z])", "_", label)

    # Remove punctuation as first character
    label = re.sub(r"^[\s\_\-]", "", label)

    # Turn punctuation into underscores
    label = underscore(label)

    return label
