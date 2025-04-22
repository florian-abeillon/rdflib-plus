"""Parse IRI with prefixes"""

import re

from rdflib import URIRef as IRI
from rdflib.resource import Resource as RdflibResource

from rdflib_plus.namespaces.define import (
    NAMESPACE_TO_PREFIX,
    PREFIX_TO_NAMESPACE,
)


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
    namespace = PREFIX_TO_NAMESPACE[prefix]
    iri = namespace[label]

    return iri


def stringify_iri(iri: IRI | RdflibResource) -> str:
    """Add prefix to IRI.

    Args:
        iri (Resource | IRI):
            IRI to add prefix to.

    Returns:
        str: Prefixed IRI.
    """

    # Stringify Resource (into its IRI) or IRI
    iri = str(iri)

    # TODO: Use NamespaceManager.normalizeUri() ?
    # For every known namespace
    for namespace, prefix in NAMESPACE_TO_PREFIX.items():
        # Look for namespace in iri
        res = re.match(namespace, iri)

        # If namespace is found
        if res is not None:
            # Only get fragment
            index = res.end()
            fragment = iri[index:]

            # Replace namespace by prefix
            iri = f"{prefix}:{fragment}"

            # Stop loop
            break

    return iri
