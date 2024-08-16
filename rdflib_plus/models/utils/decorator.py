"""Decorator for RDF Alt"""

import warnings
from typing import Callable, Optional

from rdflib_plus.models.rdf.rdfs_resource import ObjectType


def warning_remove_default(method: Callable) -> Callable:
    """Raise a warning if default element is removed.

    Args:
        method (Callable): Alt's method.

    Returns:
        Callable: Alt's method with warning.
    """

    def method_with_warning(
        self, element: ObjectType, n: Optional[int] = None
    ):
        # Note whether element to remove is Alt's default
        remove_default = element == self.default

        # Run method
        method(self, element, n=n)

        # If element to remove is Alt's default
        if remove_default:
            # Raise a warning
            warnings.warn(
                f"{self}: Default element removed. "
                f"New default: '{self.default}'."
            )

    return method_with_warning
