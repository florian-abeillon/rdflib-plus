"""Define functions and classes useful for model definition"""

from rdflib_plus.models.utils.define import (
    define_class,
    define_property,
    define_resource,
)
from rdflib_plus.models.utils.ordered_object import OrderedObject

__all__ = [
    "define_class",
    "define_property",
    "define_resource",
    "OrderedObject",
]
