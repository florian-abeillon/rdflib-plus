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
# Separator to use in IRI between the path and the identifier
DEFAULT_SEPARATOR: str = "#"

# Scheme of the default namespaces
DEFAULT_SCHEME: str = "http"
# Default subdomains of the default and shape namespaces
DEFAULT_SUBDOMAIN: str = "default"
SHAPES_SUBDOMAIN: str = "shapes"
# Default domain of the default and shape namespaces
DEFAULT_DOMAIN: str = "example.com"

# Define default file formats for SimpleGraph
DEFAULT_FORMAT_FAST_SIMPLEGRAPH = "ntriples"
DEFAULT_FORMAT_READABLE_SIMPLEGRAPH = "turtle"
# Define default file formats for MultiGraph
DEFAULT_FORMAT_FAST_MULTIGRAPH = "nquads"
DEFAULT_FORMAT_READABLE_MULTIGRAPH = "trig"

# Illegal characters in various parts of IRI
# Source: https://datatracker.ietf.org/doc/html/rfc3986#section-2.2
ILLEGAL_CHARS_OFFICIAL: str = ":/?#[]@!$&'()*+,;="
# Source: https://afs.github.io/rdf-iri-syntax.html#notes-iris
ILLEGAL_CHARS_UNOFFICIAL: str = " {}<>"
ILLEGAL_CHARS_IN_AUTHORITY_ONLY: str = "@():"

# Maximum length of character in Collections' string representation
THRESHOLD_STR: int = 60
# Maximum length of character in Collections' trimmed string representation
THRESHOLD_TRIMMED_STR: int = 30
# Separator between elements in Collections' string representation
SEPARATOR: str = ", "
