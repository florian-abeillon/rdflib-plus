"""Get environment variables"""

import os

VERSION = os.getenv("VERSION", "0.1.0")

AUTHORITY_DEFAULT = os.getenv("AUTHORITY_DEFAULT", "example.com")

FLAVOUR_DEFAULT = os.getenv("FLAVOUR_DEFAULT", "default")
FLAVOUR_SHAPES = os.getenv("FLAVOUR_SHAPES", "shape")
