"""Function to build namespaces"""

import re
from pathlib import Path
from typing import Optional

from rdflib import Namespace

from rdflib_plus.config import (
    DEFAULT_DOMAIN,
    DEFAULT_SCHEME,
    DEFAULT_SUBDOMAIN,
    SHAPES_SUBDOMAIN,
)
from rdflib_plus.utils import legalize_for_iri


def create_namespace(
    scheme: str = DEFAULT_SCHEME,
    domain: str = DEFAULT_DOMAIN,
    subdomain: Optional[str] = None,
    authority: Optional[str] = None,
    path: Optional[str] = None,
    shape: bool = False,
) -> Namespace:
    """Build namespace, given the specified IRI parts.

    Args:
        scheme (str, optional):
            IRI's scheme. Defaults to DEFAULT_SCHEME.
        domain (str, optional):
            IRI's domain. Defaults to DEFAULT_DOMAIN.
        subdomain (str | None, optional):
            IRI's subdomain. Defaults to None.
        authority (str | None, optional):
            IRI's authority; if specified, overrules domain and subdomain.
            Defaults to None.
        path (str | None, optional):
            IRI's path. Defaults to None.
        shape (bool, optional):
            Whether the namespace corresponds to shapes. Defaults to False.

    Returns:
        Namespace: Namespace corresponding to the IRI built.
    """

    # If no authority is specified
    if authority is None:
        # If no subdomain is specified
        if subdomain is None:
            # Get appropriate default subdomain
            subdomain = SHAPES_SUBDOMAIN if shape else DEFAULT_SUBDOMAIN

        # Reconstruct authority from domain and subdomain
        authority = f"{subdomain}.{domain}"

    # Format every part of the IRI
    scheme = legalize_for_iri(scheme)
    authority = legalize_for_iri(authority)

    # If any, remove trailing slash(es)
    assert authority, "Please provide an authority."
    if authority[-1] in ["/", "#"]:
        authority = re.sub(r"[\/\#]*$", "", authority)

    # Build IRI from its parts
    iri = f"{scheme}://{authority}"

    # If a path is specified
    if path is not None:
        # Clean it, then add it to IRI
        path = legalize_for_iri(path)
        iri += f"/{Path(path)}"

    # Create namespace from IRI
    namespace = Namespace(iri)

    return namespace
