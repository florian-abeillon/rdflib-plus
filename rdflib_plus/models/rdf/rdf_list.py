"""RDF List constructor"""

from typing import Callable, Iterable, Optional, Union

from rdflib import RDF, Graph, Namespace
from rdflib import URIRef as IRI

from rdflib_plus.config import DEFAULT_CHECK_TRIPLES
from rdflib_plus.definitions import RDFS_CLASSES
from rdflib_plus.models.rdf.rdfs_resource import ObjectType, ResourceOrIri
from rdflib_plus.models.utils.collection import Collection
from rdflib_plus.models.utils.decorators import formatted_index
from rdflib_plus.models.utils.types import ConstraintsType


class List(Collection):
    """RDF List constructor"""

    # List's RDF type
    _type: ResourceOrIri = RDF.List

    # TODO: No label, blank node
    # List's property constraints
    _constraints: ConstraintsType = Collection.update_constraints(
        RDFS_CLASSES[_type]["constraints"]
    )

    def __init__(
        self,
        graph: Graph,
        elements: Optional[list[ObjectType] | Collection] = None,
        namespace: Optional[Namespace] = None,
        local: bool = False,
        check_triples: bool = DEFAULT_CHECK_TRIPLES,
    ) -> None:
        """Initialize List.

        Args:
            graph (Graph):
                Graph to search or create List into.
            elements (
                list[Resource | IRI | Literal | Any] | Collection | None,
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
        self._sublists: list[List] = []

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
            Resource | IRI | Literal | Any:
                Element at given index.
        """
        return self._elements[index]

    def __reversed__(self) -> Iterable[ObjectType]:
        """Returns elements of List in reverse order.

        Returns:
            Iterable[IRI | Literal | Any]:
                Iterable over elements of List in reverse order .
        """
        return iter(self.elements[::-1])

    def __setitem__(self, index: int, element: ObjectType) -> None:
        """Replace element of List at given index.

        Args:
            index (int):
                Index of element to change in List. Can be negative.
            element (Resource | IRI | Literal | Any):
                New value of element.
        """

        # Update value in graph
        sublist = self._sublists[index]
        sublist.replace(RDF.first, element)

        # Update value and its formatted form in elements lists
        self._elements[index] = element
        self._elements_formatted[index] = sublist.get_value(RDF.first)

    def _append(self, element: ObjectType) -> None:
        """Append element to the end of List.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to append to List.
        """

        # Create new Sublist
        new_sublist = self._build_sublist(element)

        # If List is not empty, get last sublist and link it to new one
        if self:
            last_sublist = self._sublists[-1]
            last_sublist.replace(RDF.rest, new_sublist)

        # Append element and its formatted form to element lists
        self._elements.append(element)
        self._elements_formatted.append(new_sublist.get_value(RDF.first))
        # Append new sublist to sublist list
        self._sublists.append(new_sublist)

    def _build_sublist(
        self, first: ObjectType, rest: Union["List", IRI] = RDF.nil
    ) -> "List":
        """Create new Sublist.

        Args:
            first (Resource | IRI | Literal | Any):
                Element to initialize List with.
            rest (List | IRI, optional):
                Rest to initialize List with. Defaults to RDF.nil.

        Returns:
            List: New sublist.
        """

        # Create new sublist, or use List if it is empty
        sublist = (
            List(self._graph, check_triples=self._check_triples)
            if self
            else self
        )

        # Set RDF.first and RDF.rest properties
        sublist.set(RDF.first, first)
        sublist.set(RDF.rest, rest)

        return sublist

    @formatted_index()
    def _pop(self, index: int) -> ObjectType:
        """Delete and return element of List at given index.

        Args:
            index (int):
                Index of element to delete and return in List.
                Can be negative.

        Returns:
            Resource | IRI | Literal | Any:
                Removed element.
        """

        # If popping the first element while there are others,
        # just replace the first value by the second,
        # then remove the second element
        if index == 0 and len(self) > 1:

            # Replace first element with new value
            old_first_element = self[0]
            self[0] = self[1]

            # Remove duplicated value at second position
            del self[1]

            # Return the old first value
            return old_first_element

        # Otherwise, pop sublist from list, and delete respective element
        sublist = self._sublists.pop(index)
        element = self._elements.pop(index)
        del self._elements_formatted[index]

        # If List is now empty, just clear the sublist
        # (keep the other properties)
        if not self:
            sublist.remove(RDF.first)
            sublist.remove(RDF.rest)

        # Otherwise, if List still has other elements
        else:

            # Delete the popped sublist whatsoever
            sublist.remove(None)

            # Get previous sublist and rest
            prev_sublist = self._sublists[index - 1]
            rest = RDF.nil if index == len(self) else self._sublists[index]

            # Link previous sublist with next one
            prev_sublist.replace(RDF.rest, rest)

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

        # For every sublist
        for i, sublist in enumerate(self._sublists):

            # If first sublist, just empty it
            if i == 0:
                sublist.remove(RDF.first)
                sublist.remove(RDF.rest)

            # Otherwise, delete it whatsoever
            else:
                sublist.remove(None)

        # Clear elements and sublists lists
        self._elements.clear()
        self._elements_formatted.clear()
        self._sublists.clear()

    def extend(self, new_elements: list[ObjectType] | Collection) -> None:
        """Extend List with new elements.

        Args:
            new_elements (list[Resource | IRI | Literal | Any] | Collection):
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

    @formatted_index(inserting=True)
    def insert(self, index: int, element: ObjectType) -> None:
        """Insert element at index-th position of List.

        Args:
            index (int):
                Index to insert element at.
            element (ObjectType):
                Element to insert into List.
        """

        # If inserting at or after the end of List, just append element
        if index > len(self) - 1:
            self._append(element)
            return

        # If inserting a new first element
        if index == 0:

            # Replace first element with new value
            old_first_element = self[0]
            self[0] = element

            # Insert old value at second position
            self.insert(1, old_first_element)
            return

        # Otherwise, initialize new sublist
        rest = self._sublists[index] if self else RDF.nil
        new_sublist = self._build_sublist(element, rest=rest)

        # Get previous sublist and replace its "rest" attribute
        prev_sublist = self._sublists[index - 1]
        prev_sublist.replace(RDF.rest, new_sublist)

        # Insert new element into the elements lists,
        # and new sublist into the sublists list
        self._elements.insert(index, element)
        self._elements_formatted.insert(
            index, new_sublist.get_value(RDF.first)
        )
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
        self.elements = list(reversed(self.elements))

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
        self.elements = list(sorted(self._elements, key=key, reverse=reverse))
