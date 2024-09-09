"""RDF Seq constructor"""

from typing import Callable, Optional

from rdflib import RDF

from rdflib_plus.models.rdf.rdfs_container import Collection, Container
from rdflib_plus.models.rdf.rdfs_resource import ObjectType, ResourceOrIri


class Seq(Container):
    """RDF Seq constructor"""

    # Seq's RDF type
    _type: ResourceOrIri = RDF.Seq

    def __delitem__(self, index: int) -> None:
        """Delete element of Seq at given index.

        Args:
            index (int):
                Index of element to delete in Seq. Can be negative.
        """
        _ = self._pop(index)

    def __getitem__(self, index: int) -> ObjectType:
        """Return element of Seq at given index.

        Args:
            index (int):
                Index of element in Seq. Can be negative.

        Returns:
            Resource | IRI | Literal | Any: Element at given index.
        """
        return self._elements[index]

    def __reversed__(self) -> "Seq":
        """Reverse order of elements of Seq, and returns self.

        Returns:
            Seq: Reversed Seq.
        """
        self.reverse()
        return self

    def __setitem__(self, index: int, element: ObjectType) -> None:
        """Replace element of Seq at given index.

        Args:
            index (int):
                Index of element to change in Seq. Can be negative.
            element (Resource | IRI | Literal | Any):
                New value of element.
        """

        # Update value and its formatted form in elements lists
        self._elements[index] = element
        self._elements_formatted[index] = self._format_object(element)

        # Update value in graph
        predicate = self._get_predicate(index)
        self.replace(predicate, element)

    def append(self, element: ObjectType) -> None:
        """Append element to the end of Seq.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to append to Seq.
        """
        self._append(element)

    def extend(self, new_elements: list[ObjectType] | Collection) -> None:
        """Extend Seq with new elements.

        Args:
            new_elements (
                list[Resource | IRI | Literal | Any]
                | Collection
            ):
                New elements to append to Seq.
        """
        super()._extend(new_elements)

    def index(self, element: ObjectType, start: int = 0, end: int = -1) -> int:
        """Get index of element in Seq.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to look for in Seq.
            start (int, optional):
                Index from which to look for element.
            end (int, optional):
                Index until which to look for element.

        Returns:
            int: Index of element in Seq.
        """
        return self._index(element, start=start, end=end)

    def insert(self, index: int, element: ObjectType) -> None:
        """Insert element at index-th position of Seq.

        Args:
            index (int):
                Index to insert element at.
            element (ObjectType):
                Element to insert into Seq.
        """
        super()._insert(index, element)

    def pop(self, index: int = -1) -> ObjectType:
        """Delete and return element of Seq at given index.

        Args:
            index (int, optional):
                Index of element to delete and return in Seq.
                Can be negative. Defaults to -1.

        Returns:
            Resource | IRI | Literal | Any: Removed element.
        """
        return super()._pop(index)

    def reverse(self) -> None:
        """Reverse order of elements of Seq."""
        self.elements = reversed(self.elements)

    def sort(
        self, key: Optional[Callable] = None, reverse: bool = False
    ) -> None:
        """Sort elements of Seq.

        Args:
            key (Callable | None, optional):
                Key to use for sorting the elements. Defaults to None.
            reverse (bool, optional):
                Whether to sort in reverse (ie. descending) order.
                Defaults to False.
        """
        self.elements = sorted(self._elements, key=key, reverse=reverse)
