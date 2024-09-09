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
from rdflib_plus.models.utils.collection import Collection
from rdflib_plus.models.utils.types import ConstraintsType, GraphType


class List(Collection):
    """RDF List constructor"""

    # List's RDF type
    _type: ResourceOrIri = RDF.List

    # List's property constraints
    _constraints: ConstraintsType = Collection.update_constraints(
        RDFS_CLASSES[_type]["constraints"]
    )

    def __init__(
        self,
        graph: GraphType,
        elements: Optional[list[ObjectType] | Collection] = None,
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
                ]
                | Collection
                | None,
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
        _ = self._pop(index)

    def __getitem__(self, index: int) -> ObjectType:
        """Return element of List at given index.

        Args:
            index (int):
                Index of element in List. Can be negative.

        Returns:
            Resource | IRI | Literal | Any: Element at given index.
        """
        return self._elements[index]

    def __reversed__(self) -> "List":
        """Reverse order of elements of List, and returns self.

        Returns:
            List: Reversed List.
        """

        self.reverse()
        return self

    def __setitem__(self, index: int, element: ObjectType) -> None:
        """Replace element of List at given index.

        Args:
            index (int):
                Index of element to change in List. Can be negative.
            element (Resource | IRI | Literal | Any):
                New value of element.
        """

        # Update value and its formatted form in elements lists
        self._elements[index] = element
        self._elements_formatted[index] = self._format_object(element)

        # Update value in graph
        sublist = self._sublists[index]
        sublist.replace(RDF.first, element)

    def _append(self, element: ObjectType) -> None:
        """Append element to the end of List.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to append to List.
        """

        # If there are already elements in List
        if len(self) > 0:
            # Create a new sublist, but do not fill it with the elements
            # (it would not be efficient)
            new_sublist = self.__class__(self._graph)

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

        # Append element and its formatted form to elements lists
        self._elements.append(element)
        self._elements_formatted.append(self._format_object(element))
        # Append new sublist to sublists list
        self._sublists.append(new_sublist)

    def _pop(self, index: int) -> ObjectType:
        """Delete and return element of List at given index.

        Args:
            index (int):
                Index of element to delete and return in List.
                Can be negative.

        Returns:
            Resource | IRI | Literal | Any: Removed element.
        """

        # Format index
        index = self._format_index(index)

        # Pop sublist, and completely remove sublist's blank node
        sublist = self._sublists.pop(index)

        # If List is now empty
        if len(self) == 0:
            # Only remove RDF.first and RDF.rest
            sublist.remove(RDF.first)
            sublist.remove(RDF.rest)

        # Otherwise, if there are other elements
        else:
            # Completely remove the subist from the graph
            sublist.remove(None)

            # If popping the first element, the first sublist
            # (ie. the List itself) needs to be removed
            if index == 0:
                # Change List's identifiers into the first sublist's
                first_sublist = self._sublists[0]
                self._id = first_sublist.id
                self._identifier = first_sublist.iri

            # Otherwise
            else:
                # Get previous and nex sublists (or RDF.nil if last element)
                prev_sublist = self._sublists[index - 1]
                next_sublist = (
                    self._sublists[index] if index < len(self) - 1 else RDF.nil
                )

                # Link previous sublist with next one
                prev_sublist.replace(RDF.rest, next_sublist)

        # Delete respective element
        element = self._elements[index]
        del self._elements_formatted[index]

        return element

    def append(self, element: ObjectType) -> None:
        """Append element to the end of List.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to append to List.
        """
        self._append(element)

    def clear(self) -> None:
        """Remove all elements of List."""

        # If List is already empty, do nothing
        if not self._sublists:
            return

        # Only remove RDF.first and RDF.rest from the first sublist
        self._sublists[0].remove(RDF.first)
        self._sublists[0].remove(RDF.rest)

        # For every sublist
        for sublist in self._sublists[1:]:
            # Completely remove the sublist from the graph
            sublist.remove(None)

        # Clear elements and sublists lists
        self._elements.clear()
        self._elements_formatted.clear()
        self._sublists.clear()

    def extend(self, new_elements: list[ObjectType] | Collection) -> None:
        """Extend List with new elements.

        Args:
            new_elements (
                list[Resource | IRI | Literal | Any]
                | Collection
            ):
                New elements to append to List.
        """
        super()._extend(new_elements)

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

    def insert(self, index: int, element: ObjectType) -> None:
        """Insert element at index-th position of List.

        Args:
            index (int):
                Index to insert element at.
            element (ObjectType):
                Element to insert into List.
        """

        index = self._format_index(index)
        if index > len(self) - 1:
            self._append(element)

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
        self._elements_formatted.insert(index, self._format_object(element))
        self._sublists.insert(index, new_sublist)

    def pop(self, index: int = -1) -> ObjectType:
        """Delete and return element of List at given index.

        Args:
            index (int, optional):
                Index of element to delete and return in List.
                Can be negative. Defaults to -1.

        Returns:
            Resource | IRI | Literal | Any: Removed element.
        """
        return self._pop(index)

    def reverse(self) -> None:
        """Reverse order of elements of List."""
        self.elements = reversed(self.elements)

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
