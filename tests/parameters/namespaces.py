"""Define test parameters for namespaces"""

from rdflib import DCTERMS, OWL, RDF, RDFS, SKOS, XSD, Namespace

from rdflib_plus import DEFAULT_NAMESPACE

# 0 - Input namespace (Namespace)
PARAMETERS_NAMESPACES: list[Namespace] = [
    # DEFAULT_NAMESPACE,
    Namespace("http://subdomain.domain.io/"),
    Namespace("http://no.trailing.slash"),
    Namespace("/wrong.n@mespace[format]:but_whatever!"),
]

# # Define some custom Namespaces
# custom_namespaces: list[Namespace] = [
#     Namespace("http://subdomain.domain.io/"),
#     Namespace("http://no.trailing.slash"),
#     Namespace("/wrong.n@mespace[format]:but_whatever!"),
# ]

# # 0 - Input namespace (Namespace)
# PARAMETERS_NAMESPACES_PREFIXES = {
#     DEFAULT_NAMESPACE: ":",
#     DCTERMS: "dcterms",
#     OWL: "owl",
#     RDF: "rdf",
#     RDFS: "rdfs",
#     SKOS: "skos",
#     XSD: "xsd",
#     **{namespace: str(namespace) for namespace in custom_namespaces}
# }
