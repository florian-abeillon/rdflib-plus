"""Define test parameters for namespaces"""

from rdflib import Namespace

# 0 - Input namespace (Namespace)
PARAMETERS_NAMESPACES: list[Namespace] = [
    Namespace("http://subdomain.domain.io/"),
    Namespace("http://no.trailing.slash"),
    Namespace("/wrong.n@mespace[format]:but_whatever!"),
]
