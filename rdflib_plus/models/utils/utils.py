"""Useful functions"""

from rdflib_plus.config import SEPARATOR, THRESHOLD_TRIMMED_STR


def format_index(index: int, length: int, inserting: bool = False) -> int:
    """Turn negative indices into "real", (positive) indices.

    Args:
        index (int):
            Index to format.
        length (int):
            Number of elements in collection.
        inserting (bool, optional):
            Whether the index is used in insert() method.
            Defaults to False.

    Returns:
        int: Formatted index (integer between 0 and the number of elements).
    """

    # If the index is used in insert() method
    if inserting:

        # If index is too big or too small, restrain it
        if index > length - 1:
            index = length
        elif index <= -length:
            index = 0

    # Otherwise, if index is not valid given length, raise an error
    elif length and not -length <= index < length:
        raise IndexError(
            f"Index '{index}' is not valid with object of length " f"{length}."
        )

    # If index is negative, turn it into a "real", positive index
    if index < 0:
        index += length

    return index


def trim_str_list(
    elements: list[str], threshold: int = THRESHOLD_TRIMMED_STR
) -> list[str]:
    """Trim list of string elements, to not exceed a certain length.

    Args:
        elements (list[str]):
            List of string elements to trim.
        threshold (int, optional):
            Maximum number of characters after trimming.
            Defaults to THRESHOLD_TRIMMED_STR.

    Returns:
        list[str]: Trimmed list.
    """

    # Always include first element
    elements_trimmed = [elements[0]]

    # Initialize character counts
    count = len(elements[0])
    len_sep = len(SEPARATOR)

    # For every subsequent element
    for el in elements[1:]:

        # Compute the length of characters if it is added to the trimmed list
        count += len(el) + len_sep

        # If the character count is longer than the threshold, stop
        if count > threshold:
            break

        # Otherwise, add element to the trimmed list
        elements_trimmed.append(el)

    return elements_trimmed
