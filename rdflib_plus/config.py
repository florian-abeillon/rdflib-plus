"""Environment and default variables"""

import os

# Version of the graph
VERSION = os.getenv("VERSION", "0.1.0")

# Scheme of the default namespaces
DEFAULT_SCHEME = os.getenv("DEFAULT_SCHEME", "http")

# Authority of the default and shape namespaces
DEFAULT_AUTHORITY = os.getenv("DEFAULT_AUTHORITY")
SHAPE_AUTHORITY = os.getenv("SHAPE_AUTHORITY")

# If no default authority is specified
if DEFAULT_AUTHORITY is None:
    # Subdomain of the default and shape namespaces
    DEFAULT_SUBDOMAIN = os.getenv("DEFAULT_SUBDOMAIN", "default")
    SHAPES_SUBDOMAIN = os.getenv("SHAPES_SUBDOMAIN", "shapes")
    # Second-level domain of the default and shape namespaces
    DEFAULT_SECOND_LEVEL_DOMAIN = os.getenv(
        "DEFAULT_SECOND_LEVEL_DOMAIN", "example"
    )
    # Top-level domain of the default and shape namespaces
    DEFAULT_TOP_LEVEL_DOMAIN = os.getenv("DEFAULT_TOP_LEVEL_DOMAIN", "com")

    # Build the authority of the default namespaces
    # From their domain components
    DEFAULT_AUTHORITY = ".".join(
        [
            DEFAULT_SUBDOMAIN,
            DEFAULT_SECOND_LEVEL_DOMAIN,
            DEFAULT_TOP_LEVEL_DOMAIN,
        ]
    )
    SHAPE_AUTHORITY = ".".join(
        [
            SHAPES_SUBDOMAIN,
            DEFAULT_SECOND_LEVEL_DOMAIN,
            DEFAULT_TOP_LEVEL_DOMAIN,
        ]
    )
