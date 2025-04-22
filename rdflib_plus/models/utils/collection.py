"""Object collection constructor"""

from typing import Iterable, Optional, Union

from rdflib import Graph, Namespace
from rdflib import URIRef as IRI

from rdflib_plus.config import DEFAULT_CHECK_TRIPLES, SEPARATOR, THRESHOLD_STR
from rdflib_plus.models.rdf.rdfs_resource import ObjectType, Resource
from rdflib_plus.models.utils.utils import format_index, trim_str_list


class Collection(Resource):
    """Object collection constructor"""

    @property
    def elements(self) -> list[IRI]:
        """List of elements contained in Collection."""
        return self._elements

    @elements.setter
    def elements(
        self, new_elements: Union["Collection", list[ObjectType]]
    ) -> None:
        """Replace all the elements contained in Collection.

        Args:
            new_elements (Collection | list[Resource | IRI | Literal | Any]):
                New set of elements to put in Collection.
        """

        # Clear elements list, and remove them from graph
        self.clear()

        # Add new elements to elements list
        self._extend(new_elements)

    def __init__(
        self,
        graph: Graph,
        elements: Union[list[ObjectType], "Collection", None] = None,
        namespace: Optional[Namespace] = None,
        local: bool = False,
        check_triples: bool = DEFAULT_CHECK_TRIPLES,
    ) -> None:
        """Initialize Collection.

        Args:
            graph (Graph):
                Graph to search or create Collection into.
            elements (
                list[Resource | IRI | Literal | Any]
                | Collection
                | None,
                optional
            ):
                Elements to put in Collection at its creation.
                Defaults to None.
            namespace (Namespace | None, optional):
                Namespace to search or create Collection into.
                Defaults to None.
            local (bool, optional):
                Whether Collection only appears in the specified
                namespace. Defaults to False.
            check_triples (bool, optional):
                Whether to check triples that are added or set.
                Defaults to DEFAULT_CHECK_TRIPLES.
        """

        # Create Collection
        super().__init__(
            graph,
            namespace=namespace,
            local=local,
            check_triples=check_triples,
        )

        # Initialize lists of elements, and their formatted form
        self._elements = []
        self._elements_formatted = []

        # If some elements are specified, set them as a property
        if elements is not None:
            self.elements = elements

    def __add__(
        self,
        sequence: Union[list[ObjectType], set[ObjectType], "Collection"],
    ) -> "Collection":
        """Returns the result of the addition to a sequence.

        Args:
            sequence (
                list[Resource | IRI | Literal | Any]
                | set[Resource | IRI | Literal | Any]
                | Collection
            ):
                Sequence of elements that must be added.

        Returns:
            Collection: New Collection object, containing elements from self
                        and sequence.
        """

        # If sequence is a Collection, get its elements
        if isinstance(sequence, Collection):
            sequence = sequence.elements

        # Return a new Collection object, with elements from self and sequence
        return self.__class__(
            self.graph,
            elements=self._elements + sequence,
            check_triples=self._check_triples,
        )

    def __contains__(self, element: ObjectType) -> bool:
        """Check wether element is already in Collection.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to look for in Collection.

        Returns:
            bool: Whether element is already in Collection.
        """

        try:
            # Try to find element
            _ = self._index(element)

            # If success, return True
            return True

        # If fail, return False
        except ValueError:
            return False

    def __iadd__(
        self,
        sequence: Union[list[ObjectType], set[ObjectType], "Collection"],
    ) -> "Collection":
        """Returns the result of the addition of a sequence.

        Args:
            sequence (
                list[Resource | IRI | Literal | Any]
                | set[Resource | IRI | Literal | Any]
                | Collection
            ):
                Sequence of elements that must be added.

        Returns:
            Collection: Current Collection object, extended with the specified
                        elements.
        """
        self._extend(sequence)
        return self

    def __iter__(self) -> Iterable:
        """Returns an iterator on the elements of Collection.

        Returns:
            Iterable: Iterator on elements of Collection.
        """
        return iter(self._elements)

    def __len__(self) -> int:
        """Returns the number of elements in Collection.

        Returns:
            int: Number of elements in Collection.
        """
        return len(self._elements)

    def __str__(self) -> str:
        """Human-readable string representation of Collection"""

        # Get type of Collection, and its elements' string representation
        type_ = self.__class__.__name__
        elements = list(map(str, self._elements))

        # Build list of elements' string representations
        str_elements = SEPARATOR.join(elements)

        # It this list is too long
        if len(str_elements) > THRESHOLD_STR:

            # Trim the first and last elements
            first_elements = trim_str_list(elements)
            last_elements = trim_str_list(elements[::-1])

            # Join them with an ellipsis in between
            str_elements = SEPARATOR.join(
                first_elements + ["... "] + last_elements[::-1]
            )

        # Build Collection's string representation
        return f"{type_}({str_elements})"

    def _append(self, element: ObjectType) -> None:
        """Append element to the end of Collection."""
        raise NotImplementedError

    def _extend(
        self, new_elements: Union[list[ObjectType], "Collection"]
    ) -> None:
        """Extend Collection with new elements.

        Args:
            new_elements (
                list[Resource | IRI | Literal | Any]
                | Collection
            ):
                New elements to append to Collection.
        """
        for new_element in new_elements:
            self._append(new_element)

    # TODO: Un-protect method to use in decorator?
    # def _format_index(self, index: int, inserting: bool = False) -> int:
    #     """Turn negative indices into "real" (positive) index.

    #     Args:
    #         index (int):
    #             Index to format.
    #         inserting (bool, optional):
    #             Whether the index is used in insert() method.
    #             Defaults to False.

    #     Returns:
    #         int: Formatted index (integer between 0 and
    #              the number of elements).
    #     """

    #     # If the index is used in insert() method
    #     if inserting:

    #         # Restrain index if its too big or too small
    #         if index > len(self) - 1:
    #             index = len(self)
    #         elif index <= -len(self):
    #             index = 0

    #     # Otherwise, if index is not valid given the length of element list,
    #     # raise an error
    #     elif self and not -len(self) <= index < len(self):
    #         raise IndexError(
    #             f"Index '{index}' is not valid with object of length "
    #             f"{len(self)}."
    #         )

    #     # If index is negative, turn it into a "real", positive index
    #     if index < 0:
    #         index += len(self)

    #     return index

    def _index(
        self, element: ObjectType, start: int = 0, end: int = -1
    ) -> int:
        """Get index of first instance of element (if any) in Collection.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to look for in Collection.
            start (int, optional):
                Index from which to look for element (included). Defaults to 0.
            end (int, optional):
                Index until which to look for element (included).
                Defaults to -1.

        Returns:
            int: Index of element in Collection.
        """

        # TODO: What if Collection does contain None?
        # Format element for graph input
        element_formatted = self._format_object(element)

        # Format end index
        start = format_index(start, len(self))
        end = format_index(end, len(self))

        # Try to find element between start and end indices
        index = self._elements_formatted[start : end + 1].index(
            element_formatted
        )

        # If success, return index of element
        return start + index

    def _pop(self, index: int) -> ObjectType:
        """Delete and return element of Collection at given index."""
        raise NotImplementedError

    def clear(self) -> None:
        """Remove all elements of Collection."""
        raise NotImplementedError

    def copy(self) -> "Collection":
        """Return a shallow copy of Collection."""
        return self.__class__(
            self.graph,
            elements=self._elements,
            check_triples=self._check_triples,
        )

    def count(self, element: ObjectType) -> int:
        """Count the number of times element appears in Collection.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to look for in Collection.

        Returns:
            int: Number of times element appears in Collection.
        """
        element_formatted = self._format_object(element)
        return self._elements_formatted.count(element_formatted)

    def discard_element(self, element: ObjectType) -> None:
        """Remove the first instance of an element from Collection,
           without raising error if it was not present.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to remove from Collection.
        """

        # Try to remove element
        try:
            self.remove_element(element)

        # If no element with this value is in Collection,
        # do nothing
        except ValueError:
            pass

    def remove_element(self, element: ObjectType) -> None:
        """Remove the first instance of an element from Collection,
           and raise an error if it was not present.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to remove from Collection.
        """

        # Get index of element in Collection
        index = self._index(element)

        # Remove it from Collection
        _ = self._pop(index)
