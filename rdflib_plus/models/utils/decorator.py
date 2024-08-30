"""Decorator for RDF Alt"""

import warnings
from typing import Callable

from rdflib_plus.models.rdf.rdfs_resource import ObjectType


def warning_remove_default(method: Callable) -> Callable:
    """Raise a warning if default element is removed.

    Args:
        method (Callable): Alt's method.

    Returns:
        Callable: Alt's method with warning.
    """

    def method_with_warning(self, element: ObjectType):
        # Note whether element to remove is Alt's default
        removing_default = element == self.default

        # Run method
        method(self, element)

        # If element to remove is Alt's default
        if removing_default:
            # Raise a warning
            warnings.warn(
                f"{self}: Default element removed. "
                f"New default set to '{self.default}'."
            )

    return method_with_warning
