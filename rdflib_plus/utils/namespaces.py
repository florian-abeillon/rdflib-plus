"""Initialize custom and adapt standard namespaces"""

import re

from inflection import dasherize
from rdflib import DCTERMS, OWL, RDF, RDFS, SKOS, XSD, Namespace

from rdflib_plus.models.namespace import CustomNamespace
from rdflib_plus.utils import format_text, legalize_iri
from rdflib_plus.utils.config import (
    AUTHORITY_DEFAULT,
    FLAVOUR_DEFAULT,
    FLAVOUR_SHAPES,
)


def build_custom_namespace(
    authority: str = AUTHORITY_DEFAULT,
    flavour: str = FLAVOUR_DEFAULT,
    path: str = "",
    shape: bool = False,
) -> Namespace:
    """To build custom namespaces for each homemade task

    Args:
        authority (str): Authority in custom namespace's IRI
        path (str, optional): Path in custom namespace's IRI. Defaults to "".

    Returns:
        Namespace: Custom namespace, with appropriate IRI
    """

    assert re.match(
        r"\d+\.\d{2, 3}$", authority
    ), "authority should be of the form 'abcde.fg' or 'abcdef.ghi'"

    # Get and format authority and flavour
    authority = legalize_iri(dasherize(format_text(authority)))
    if shape and flavour == FLAVOUR_DEFAULT:
        flavour = FLAVOUR_SHAPES

    # Build IRI from authority
    iri = f"http://{flavour}.{authority}"

    # If any, add path to IRI
    if path:
        path = legalize_iri(dasherize(format_text(path)))
        iri += f"/{path}"

    # Create namespace from IRI, and return it
    return Namespace(iri)


NS_DEFAULT = build_custom_namespace()
NS_SHAPES = build_custom_namespace(shape=True)


PREFIXES = {
    NS_DEFAULT: "",
    DCTERMS: "dcterms",
    OWL: "owl",
    RDF: "rdf",
    RDFS: "rdfs",
    SKOS: "skos",
    XSD: "xsd",
}

# Change type of namespaces without a fragment #
# to CustomNamespace, to return fragment anyway
PREFIXES = {
    ns if str(ns)[-1] == "#" else CustomNamespace(ns): prefix
    for ns, prefix in PREFIXES.items()
}
