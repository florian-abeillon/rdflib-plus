"""RDF List constructor"""

from typing import Callable, Optional

from rdflib import RDF, Namespace

from rdflib_plus.config import DEFAULT_CHECK_TRIPLES
from rdflib_plus.definitions import RDFS_CLASSES
from rdflib_plus.models.rdf.rdfs_resource import (
    ObjectType,
    Resource,
    ResourceOrIri,
)
from rdflib_plus.models.utils.Collection import Collection
from rdflib_plus.models.utils.types import ConstraintsType, GraphType


class List(Collection):
    """RDF List constructor"""

    # List's RDF type
    _type: ResourceOrIri = RDF.List

    # List's property constraints
    _constraints: ConstraintsType = Resource.update_constraints(
        RDFS_CLASSES[_type]["constraints"]
    )

    def __init__(
        self,
        graph: GraphType,
        elements: Optional[list[ObjectType]] = None,
        namespace: Optional[Namespace] = None,
        local: bool = False,
        check_triples: bool = DEFAULT_CHECK_TRIPLES,
    ) -> None:
        """Initialize List.

        Args:
            graph (Graph | MultiGraph):
                Graph to search or create List into.
            elements (
                list[
                    Resource | IRI | Literal | Any
                ] | None,
                optional
            ):
                Elements to put in List at its creation. Defaults to None.
            namespace (Namespace | None, optional):
                Namespace to search or create List into. Defaults to None.
            local (bool, optional):
                Whether List only appears in the specified namespace.
                Defaults to False.
            check_triples (bool, optional):
                Whether to check triples that are added or set.
                Defaults to DEFAULT_CHECK_TRIPLES.
        """

        # Initialize sublists list
        self._sublists: list[Resource] = []

        # Create List
        super().__init__(
            graph,
            elements=elements,
            namespace=namespace,
            local=local,
            check_triples=check_triples,
        )

    def __delitem__(self, index: int) -> None:
        """Delete element of List at given index.

        Args:
            index (int):
                Index of element to delete in List. Can be negative.
        """

        # Pop element at given index
        self._pop(index=index)

    def __getitem__(self, index: int) -> ObjectType:
        """Return element of List at given index.

        Args:
            index (int):
                Index of element in List. Can be negative.

        Returns:
            Resource | IRI | Literal | Any: Element at given index.
        """

        return self._elements[index]

    def __setitem__(self, index: int, element: ObjectType) -> None:
        """Replace element of List at given index.

        Args:
            index (int):
                Index of element to change in List. Can be negative.
            element (Resource | IRI | Literal | Any):
                New value of element.
        """

        # Update value in elements list
        self._elements[index] = element

        # Get replaced sublist
        sublist = self._sublists[index]

        # Update value in graph
        sublist.replace(RDF.first, element)

    def _pop(self, index: int = 0) -> ObjectType:
        """Delete and return element of List at given index.

        Args:
            index (int, optional):
                Index of element to delete and return in List.
                Can be negative. Defaults to 0.

        Returns:
            Resource | IRI | Literal | Any: Removed element.
        """

        # Pop sublist, and completely remove sublist's blank node
        sublist = self._sublists.pop(index)
        sublist.remove(None)

        # If popped element is not the first one
        if index > 0:
            # Get previous sublist
            prev_sublist = self._sublists[index - 1]

            # If popped element is not the last one either
            if index < len(self) - 1:
                # Get next sublist, and link the previous one to it
                next_sublist = self._sublists[index]
                prev_sublist.set(RDF.rest, next_sublist)

            # Otherwise
            else:
                # Specify that previous sublist is now the last one
                prev_sublist.set(RDF.rest, RDF.nil)

        # Delete respective element
        del self._elements[index]

    def append(self, element: ObjectType) -> None:
        """Append element to the end of List.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to append to List.
        """

        # If there are already elements in List
        if len(self) != 0:
            # Create a new sublist
            new_sublist = List(self._graph)

            # Get last sublist, and replace its 'rest' attribute
            last_sublist = self._sublists[-1]
            last_sublist.replace(RDF.rest, new_sublist)

        # Otherwise, if element is the first of List
        else:
            # Set current list as new sublist
            new_sublist = self

        # Set new value of element in graph
        new_sublist.set(RDF.first, element)
        new_sublist.set(RDF.rest, RDF.nil)

        # Append element to elements list
        # and new sublist to sublists list
        self._elements.append(element)
        self._sublists.append(new_sublist)

    def clear(self) -> None:
        """Remove all elements of List."""

        # For every sublist
        for sublist in self._sublists:
            # If sublist is List
            if sublist == self:
                # Only remove List's "first" and "rest" attributes
                self.remove(RDF.first)
                self.remove(RDF.rest)

            # Otherwise
            else:
                # Completely remove sublist's blank node
                sublist.remove(None)

        # Clear elements and sublists lists
        self._elements.clear()
        self._sublists.clear()

    def insert(self, index: int, element: ObjectType) -> None:
        """Insert element at index-th position of List.

        Args:
            index (int):
                Index to insert element at.
            element (ObjectType):
                Element to insert into List.
        """

        # Create a new sublist, and initialize it with element
        new_sublist = List(self._graph, elements=[element])

        # Get next sublist, and set new sublist's "rest" attribute
        next_sublist = self._sublists[index]
        new_sublist.set(RDF.rest, next_sublist)

        # If there is another element before new element
        if index > 0:
            # Get previous sublist, and replace its "rest" attribute
            prev_sublist = self._sublists[index - 1]
            prev_sublist.replace(RDF.rest, new_sublist)

        # Insert new sublist into the elements and sublists lists
        self._elements.insert(index, element)
        self._sublists.insert(index, new_sublist)

    def pop(self, index: int = 0) -> ObjectType:
        """Delete and return element of List at given index.

        Args:
            index (int, optional):
                Index of element to delete and return in List.
                Can be negative. Defaults to 0.

        Returns:
            Resource | IRI | Literal | Any: Removed element.
        """

        return self._pop(index=index)

    def index(self, element: ObjectType, start: int = 0, end: int = -1) -> int:
        """Get index of element in List.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to look for in List.
            start (int, optional):
                Index from which to look for element.
            end (int, optional):
                Index until which to look for element.

        Returns:
            int: Index of element in List.
        """

        return self._index(element, start=start, end=end)

    def reverse(self) -> None:
        """Reverse order of elements of List."""

        self.elements = reversed(self._elements)

    def sort(
        self, key: Optional[Callable] = None, reverse: bool = False
    ) -> None:
        """Sort elements of List.

        Args:
            key (Callable | None, optional):
                Key to use for sorting the elements. Defaults to None.
            reverse (bool, optional):
                Whether to sort in reverse (ie. descending) order.
                Defaults to False.
        """

        self.elements = sorted(self._elements, key=key, reverse=reverse)
