"""Define useful functions"""

import re
import urllib.parse

from inflection import underscore

ILLEGAL_CHARS = '<>" {}|\\^`#/:@'
ILLEGAL_CHARS_TO_PERCENT_ENCODED_CHARS = {
    char: urllib.parse.quote(char) for char in ILLEGAL_CHARS
}


def legalize_iri(text: str) -> str:
    """Make text legal for IRI use.

    Args:
        text (str):
            Text to be used in its IRI.

    Returns:
        str: Percent-encoded text, thus cleaned from any illegal character.
    """

    # Percent-encode illegal chars
    for char, char_encoded in ILLEGAL_CHARS_TO_PERCENT_ENCODED_CHARS.items():
        text = text.replace(char, char_encoded)

    return text


def format_text(text: str) -> str:
    """Format text with underscores.

    Args:
        text (str):
            Text to format.

    Returns:
        str: Formatted text.
    """

    # Ensure all-capitalized texts remain that way
    text = re.sub(r"(?<=[A-Z])(?=[A-Z])", "_", text)

    # Turn punctuation into underscore
    # And remove punctuation as first character
    text = re.sub(r"^[\s_-]", "", underscore(text))

    return text


def check_lang(lang: str) -> bool:
    """Check format of language.

    Args:
        lang (str):
            Language code.

    Returns:
        bool: Whether language code is appropriately formatted.
    """

    return re.match(r"[a-z]{2}(\-[a-z]{2})?$", lang)  # TODO: Right?


#     return re.match(r"[a-z]+(\-[a-z0-9]+)$", lang)
