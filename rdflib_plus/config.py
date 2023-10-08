"""Default variables"""

from typing import Optional

# Whether to check all added and set triples by default
DEFAULT_CHECK_TRIPLES: bool = True
# Whether to include super-classes/properties in a resource's IRI
DEFAULT_HIERARCHICAL_PATH: bool = True
# Default language to use
DEFAULT_LANGUAGE: Optional[str] = None
# Prefix to use for default namespace
DEFAULT_PREFIX: str = ""

# Scheme of the default namespaces
DEFAULT_SCHEME = "http"
# Default subdomains of the default and shape namespaces
DEFAULT_SUBDOMAIN: str = "default"
SHAPES_SUBDOMAIN: str = "shapes"
# Default domain of the default and shape namespaces
DEFAULT_DOMAIN: str = "example.com"
