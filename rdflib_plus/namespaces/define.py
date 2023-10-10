"""Standard and custom namespaces"""

from rdflib import DCTERMS, OWL, RDF, RDFS, SKOS, XSD

from rdflib_plus.config import DEFAULT_PREFIX
from rdflib_plus.namespaces.build import create_namespace

# Define default namespaces
DEFAULT_NAMESPACE = create_namespace()
SHAPES_NAMESPACE = create_namespace(shape=True)

# Define namespaces' prefixes
PREFIX_TO_NAMESPACE = {
    DEFAULT_PREFIX: DEFAULT_NAMESPACE,
    "dcterms": DCTERMS,
    "owl": OWL,
    "rdf": RDF,
    "rdfs": RDFS,
    "skos": SKOS,
    "xsd": XSD,
}

# Create inverse dictionary,
# with namespaces as strings for convenience
NAMESPACE_TO_PREFIX = {
    str(namespace): prefix for prefix, namespace in PREFIX_TO_NAMESPACE.items()
}
