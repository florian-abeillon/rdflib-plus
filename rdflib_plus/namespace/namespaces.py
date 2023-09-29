"""Standard and custom namespaces"""

from rdflib import DCTERMS, OWL, RDF, RDFS, SKOS, XSD

from rdflib_plus.namespace.utils import create_namespace

# Define default namespaces
DEFAULT_NAMESPACE = create_namespace()
SHAPES_NAMESPACE = create_namespace(shape=True)

# Define namespaces' prefixes
NAMESPACE_PREFIXES = {
    DEFAULT_NAMESPACE: "",
    DCTERMS: "dcterms",
    OWL: "owl",
    RDF: "rdf",
    RDFS: "rdfs",
    SKOS: "skos",
    XSD: "xsd",
}

# TODO: Needed?
# from rdflib_plus.utils.namespace import CustomNamespace
# # Change type of namespaces without a fragment #
# # to CustomNamespace, to return fragment anyway
# NAMESPACE_PREFIXES = {
#     namespace
#     if str(namespace)[-1] == "#"
#     else CustomNamespace(namespace): prefix
#     for namespace, prefix in NAMESPACE_PREFIXES.items()
# }
