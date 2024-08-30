"""RDF Bag constructor"""

import random as rd
from typing import Optional

from rdflib import RDF, Namespace

from rdflib_plus.config import DEFAULT_CHECK_TRIPLES
from rdflib_plus.models.rdf.rdfs_container import Container
from rdflib_plus.models.rdf.rdfs_resource import ObjectType, ResourceOrIri
from rdflib_plus.models.utils.collection import Collection
from rdflib_plus.models.utils.types import GraphType

# TODO: Implement, if not allow_duplicates?
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


class Bag(Container):
    """RDF Bag constructor"""

    # Bag's RDF type
    _type: ResourceOrIri = RDF.Bag

    def __init__(
        self,
        graph: GraphType,
        elements: Optional[list[ObjectType] | Collection] = None,
        allow_duplicates: bool = True,
        namespace: Optional[Namespace] = None,
        local: bool = False,
        check_triples: bool = DEFAULT_CHECK_TRIPLES,
    ) -> None:
        """Initialize Bag.

        Args:
            graph (Graph | MultiGraph):
                Graph to search or create Bag into.
            elements (
                list[
                    Resource | IRI | Literal | Any
                ]
                | Collection
                | None,
                optional
            ):
                Elements to put in Bag at its creation.
                Defaults to None.
            allow_duplicates (bool):
                Whether to allow duplicated elements. Defaults to True.
            namespace (Namespace | None, optional):
                Namespace to search or create Bag into.
                Defaults to None.
            local (bool, optional):
                Whether Bag only appears in the specified
                namespace. Defaults to False.
            check_triples (bool, optional):
                Whether to check triples that are added or set.
                Defaults to DEFAULT_CHECK_TRIPLES.
        """

        # Set allow_duplicates
        self._allow_duplicates = allow_duplicates

        # If duplicated elements are not allowed
        if not allow_duplicates:
            # If elements is a Collection, extract its elements
            if isinstance(elements, Collection):
                elements = elements.elements

            # Remove any duplicates
            elements = list(set(elements))

        super().__init__(
            graph,
            elements=elements,
            namespace=namespace,
            local=local,
            check_triples=check_triples,
        )

    def _append(self, element: ObjectType) -> None:
        """Add element to Bag.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to add to Bag.
        """
        if self._allow_duplicates or element not in self._elements:
            super()._append(element)

    # def add(self, element: ObjectType) -> None:
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

    def copy(self) -> "Bag":
        """Return a shallow copy of Bag.

        Returns:
            Bag: Shallow copy of Bag.
        """

        return self.__class__(
            self.graph,
            elements=self._elements,
            check_triples=self._check_triples,
            allow_duplicates=self._allow_duplicates,
        )

    def count(self, element: ObjectType) -> int:
        """Count the number of times element appears in Bag.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to look for in Bag.

        Returns:
            int: Number of times element appears in Bag.
        """

        # If duplicates are not allowed, value is 1 or 0
        if not self._allow_duplicates:
            return int(element in self)

        return super().count(element)
