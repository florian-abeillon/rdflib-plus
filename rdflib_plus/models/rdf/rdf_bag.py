"""RDF Bag constructor"""

import random as rd
from typing import Optional

from rdflib import RDF

from rdflib_plus.models.rdf.rdfs_container import Collection, Container
from rdflib_plus.models.rdf.rdfs_resource import ObjectType, ResourceOrIri


class Bag(Container):
    """RDF Bag constructor"""

    # Bag's RDF type
    _type: ResourceOrIri = RDF.Bag

    def add_element(self, element: ObjectType) -> None:
        """Add element to Bag.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to add to Bag.
        """
        super()._append(element)

    def any(self) -> Optional[ObjectType]:
        """Return any of Bag's elements.

        Returns:
            Resource | IRI | Literal | Any | None:
                If any, random element from Bag. Otherwise, None.
        """

        # If Bag does not have any elements, return None
        if not self._elements:
            return None

        # Randomly pick element
        element = rd.choice(self._elements)

        return element

    def extend(self, new_elements: list[ObjectType] | Collection) -> None:
        """Extend Bag with new elements.

        Args:
            new_elements (
                list[Resource | IRI | Literal | Any]
                | Collection
            ):
                New elements to append to Bag.
        """
        super()._extend(new_elements)
