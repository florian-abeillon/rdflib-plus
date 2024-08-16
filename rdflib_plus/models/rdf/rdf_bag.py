"""RDF Bag constructor"""

import random
from typing import Optional

from rdflib import RDF

from rdflib_plus.models.rdf.rdfs_container import Container
from rdflib_plus.models.rdf.rdfs_resource import ObjectType, ResourceOrIri

# Define specific custom type
CollectionType = list[ObjectType] | set[ObjectType]


class Bag(Container):
    """RDF Bag constructor"""

    # Bag's RDF type
    _type: ResourceOrIri = RDF.Bag

    def _any_index(
        self,
        elements: Optional[list[ObjectType]] = None,
        include_default: bool = True,
    ) -> int:
        """Return any element of elements.

        Args:
            elements (
                list[Resource | IRI | Literal | Any] | None,
                optional
            ):
                Elements list to pick element from. Defaults to None.
            include_default (bool, optional):
                Whether to consider default element. Defaults to True.

        Returns:
            int: Index of element randomly picked from Bag.
        """

        # If no elements list is specified
        if elements is None:
            # Use Bag's elements list
            elements = self.elements

        # Include default element or not
        start = 0 if include_default else 1

        # Randomly choose index of element ot pick
        index = random.randint(start, len(elements) - 1)

        return index

    def any(self, include_default: bool = True) -> Optional[ObjectType]:
        """Return any element of Bag.

        Args:
            include_default (bool, optional):
                Whether to consider default element. Defaults to True.

        Returns:
            Resource | IRI | Literal | Any | None:
                If any, random element from Bag. Otherwise, None.
        """

        # If Bag does not have any elements, return None
        if not self._elements:
            return None

        # Randomly pick index
        index = self._any_index(
            self._elements, include_default=include_default
        )

        # Get associated element
        element = self._elements[index]

        return element
