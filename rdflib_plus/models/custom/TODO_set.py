"""Custom Set constructor"""

import random as rd
from typing import Optional

from rdflib_plus.models.rdf.rdfs_container import Container
from rdflib_plus.models.rdf.rdfs_resource import ObjectType, ResourceOrIri
from rdflib_plus.namespaces import DEFAULT_NAMESPACE

# TODO
# __and__
# __iand__
# __rand_
# __or__
# __ior__
# __ror__
# __sub__
# __isub__
# __rsub__
# __xor__
# __ixor__
# __rxor__
# difference
# difference_update
# intersection
# intersection_update
# isdisjoint
# issubset
# issuperset
# symetric_difference
# symmetric_difference_update
# union
# update


class Set(Container):
    """Custom Set constructor"""

    # Set's custom type
    _type: ResourceOrIri = DEFAULT_NAMESPACE["Set"]

    def _append(self, element: ObjectType) -> None:
        """Add element to Set.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to add to Set.
        """

        try:
            # Try to find element among Set's elements
            _ = self._index(element)

        # Otherwise
        except ValueError:
            # Add element
            super()._append(element)

    def add_element(self, element: ObjectType) -> None:
        """Add an element to Set.

        Args:
            element (Resource | IRI | Literal | Any):
                New element to add to Set.
        """
        self._append(element)

    def any(self) -> Optional[ObjectType]:
        """Return any of Set's elements.

        Returns:
            Resource | IRI | Literal | Any | None:
                If any, random alternative from Set. Otherwise, None.
        """

        # If Bag does not have any elements, return None
        if not self._elements:
            return None

        # Randomly pick element
        element = rd.choice(self._elements)

        return element
