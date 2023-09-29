"""Function to build namespaces"""

from typing import Optional

from rdflib import Namespace

from rdflib_plus.config import (
    DEFAULT_AUTHORITY,
    DEFAULT_SCHEME,
    SHAPE_AUTHORITY,
)
from rdflib_plus.utils import legalize_for_iri


def create_namespace(
    scheme: str = DEFAULT_SCHEME,
    authority: Optional[str] = None,
    path: str = "",
    shape: bool = False,
) -> Namespace:
    """Build namespace, given the specified IRI parts.

    Args:
        scheme (str, optional):
            IRI's scheme. Defaults to DEFAULT_SCHEME.
        authority (Optional[str], optional):
            IRI's authority. Defaults to None.
        path (str, optional):
            IRI's path. Defaults to "".
        shape (bool, optional):
            Whether the namespace corresponds to shapes. Defaults to False.

    Returns:
        Namespace: Namespace corresponding to the IRI built.
    """

    # If no authority is specified, get appropriate default value
    if authority is None:
        authority = SHAPE_AUTHORITY if shape else DEFAULT_AUTHORITY

    # Format every part of the IRI
    scheme = legalize_for_iri(scheme)
    authority = legalize_for_iri(authority)
    path = legalize_for_iri(path)

    # Build IRI from its parts
    iri = f"{scheme}://{authority}/{path}"

    # Create namespace from IRI
    namespace = Namespace(iri)

    return namespace
