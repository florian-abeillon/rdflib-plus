"""Object collection constructor"""

from typing import Optional, Union

from rdflib import Namespace
from rdflib import URIRef as IRI

from rdflib_plus.config import DEFAULT_CHECK_TRIPLES
from rdflib_plus.models.rdf.rdfs_resource import ObjectType, Resource
from rdflib_plus.models.utils.types import GraphType


class Collection(Resource):
    """Object collection constructor"""

    @property
    def elements(self) -> list[IRI]:
        """List of elements contained in Collection."""

        return self._elements

    @elements.setter
    def elements(self, new_elements: list[ObjectType]) -> None:
        """Replace all the elements contained in Collection.

        Args:
            new_elements (list[Resource | IRI | Literal | Any]):
                New set of elements to put in Collection.
        """

        # Clear elements list, and remove them from graph
        self.clear()

        # Add new elements to elements list
        self.extend(new_elements)

    def __init__(
        self,
        graph: GraphType,
        elements: Optional[list[ObjectType]] = None,
        namespace: Optional[Namespace] = None,
        local: bool = False,
        check_triples: bool = DEFAULT_CHECK_TRIPLES,
    ) -> None:
        """Initialize Collection.

        Args:
            graph (Graph | MultiGraph):
                Graph to search or create Collection into.
            elements (
                list[
                    Resource | IRI | Literal | Any
                ] | None,
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

        # Initialize elements list
        self._elements: list[ObjectType] = []

        # If some elements are specified
        if elements is not None:
            # Add them as attribute, and set them in the graph at the same time
            self.elements = elements

    def __len__(self) -> int:
        """Returns the number of elements in Collection.

        Returns:
            int: Number of elements in Collection.
        """

        return len(self._elements)

    def __str__(self) -> str:
        """Human-readable string representation of Collection"""

        type_ = self.__class__.__name__
        elements = [str(element) for element in self._elements]
        elements = ", ".join(elements)
        return f"{type_}({elements})"

    def _format_index(self, index: int) -> int:
        """Turn negative indices into "real" (positive) index.

        Args:
            index (int):
                Index to format.

        Returns:
            int: Formatted index (integer between 0 and
                 the number of elements).
        """

        # If index is negative
        if index < 0:
            # Turn it into "real" positive index
            index += len(self)

        # If index is not in range
        if not 0 <= index < len(self):
            # If index is still negative, set it back to its original value
            if index < 0:
                index -= len(self)

            # Raise an error
            raise ValueError(f"Index '{index}' is not valid.")

        return index

    def _index(
        self, element: ObjectType, start: int = 0, end: int = -1
    ) -> int:
        """Get index of element in Collection.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to look for in Collection.
            start (int, optional):
                Index from which to look for element. Defaults to 0.
            end (int, optional):
                Index until which to look for element. Defaults to -1.

        Returns:
            int: Index of element in Collection.
        """

        # Format element for graph input
        element = self._format_resource(element, is_object=True)

        # Increment end, so that end-th element is also considered
        end += 1

        # For every element in elements list
        for i, element_contained in enumerate(self._elements[start:end]):
            # Update index
            i += start

            # Format it for graph input
            element_contained = self._format_resource(
                element_contained, is_object=True
            )

            # If formatted elements are the same
            if element == element_contained:
                # Return index of element
                return i

        # If element is not found in the list, raise an error
        raise ValueError(f"{element} is not in List")

    def _pop(self, index: int = 0) -> ObjectType:
        """Delete and return element of Collection at given index."""
        raise NotImplementedError

    def append(self, element: ObjectType) -> None:
        """Append element to the end of Collection."""
        raise NotImplementedError

    def clear(self) -> None:
        """Remove all elements of Collection."""
        raise NotImplementedError

    def count(self, element: ObjectType) -> int:
        """Count the number of times element appears in Collection.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to look for in Collection.

        Returns:
            int: Number of times element appears in Collection.
        """

        # Initialize count
        count = 0

        # Format element for graph input
        element = self._format_resource(element, is_object=True)

        # For every element in elements list
        for element_contained in self._elements:
            # Format it for graph input
            element_contained = self._format_resource(
                element_contained, is_object=True
            )

            # If formatted elements are the same
            if element == element_contained:
                # Increment count
                count += 1

        return count

    def discard_element(
        self, element: ObjectType, n: Optional[int] = None
    ) -> None:
        """Remove element from Collection,
           without raising error if it was not present.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to remove from Collection.
            n (int | None, optional):
                Max number of elements to remove from Collection.
        """

        # If n was not specified
        if n is None:
            # Set it as the number of elements in Collection
            n = len(self._elements)

        # As long as there are elements with this value in Collection
        for _ in range(n):
            try:
                # Get index of element, and remove it
                index = self._index(element)
                _ = self._pop(index=index)

            except ValueError:
                # If no element with this value is in Collection,
                # break out from loop
                break

    def extend(
        self, new_elements: Union["Collection", list[ObjectType]]
    ) -> None:
        """Extend Collection with new elements.

        Args:
            new_elements (
                Collection |
                list[Resource | IRI | Literal | Any]
            ):
                New elements to add to Collection.
        """

        # If new_elements is a Collection, get its elements
        if isinstance(new_elements, Collection):
            new_elements = new_elements.elements

        # For every new element
        for new_element in new_elements:
            # Append it to Collection
            self.append(new_element)

    # def remove(self, element: ObjectType) -> None:
    def remove_element(
        self, element: ObjectType, n: Optional[int] = None
    ) -> None:
        """Remove element from Collection,
           and raise an error if it was not present.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to remove from Collection.
            n (int | None, optional):
                Max number of elements to remove from Collection.
        """

        # Get index of element in Collection
        index = self._index(element)

        # Remove it from Collection
        _ = self._pop(index=index)

        # If n was specified, decrement it
        if n is not None:
            n -= 1

        # Try to remove other instances of element, until none are left
        self.discard_element(element, n=n)
