"""Ordered object constructor"""

from typing import Optional, Union

from rdflib import Namespace
from rdflib import URIRef as IRI

from rdflib_plus.models.rdf.rdfs_resource import ObjectType, Resource
from rdflib_plus.models.utils.types import GraphType


class OrderedObject(Resource):
    """Ordered object constructor"""

    @property
    def elements(self) -> list[IRI]:
        """List of elements contained in OrderedObject."""

        return self._elements

    @elements.setter
    def elements(self, new_elements: list[ObjectType]) -> None:
        """Replace all the elements contained in OrderedObject.

        Args:
            new_elements (list[Resource | IRI | Literal | Any]):
                New set of elements to put in OrderedObject.
        """

        # Clear elements list, and remove them from graph
        self.clear()

        # Add new elements to elements list
        self._extend(new_elements)

    def __init__(
        self,
        graph: GraphType,
        elements: Optional[list[ObjectType]] = None,
        namespace: Optional[Namespace] = None,
    ) -> None:
        """Initialize OrderedObject.

        Args:
            graph (Graph | MultiGraph):
                Graph to search or create OrderedObject into.
            elements (
                Optional[list[
                    Resource | IRI | Literal | Any
                ]],
                optional
            ):
                Elements to put in OrderedObject at its creation. Defaults to None.
            namespace (Optional[Namespace], optional):
                Namespace to search or create Resource into. Defaults to None.
        """

        # Create OrderedObject
        super().__init__(graph, namespace=namespace)

        # Initialize elements list
        self._elements: list[ObjectType] = []

        # If some elements are specified
        if elements is not None:
            # Add them as attribute, and set them in the graph at the same time
            self.elements = elements

    def __len__(self) -> int:
        """Returns the number of elements in OrderedObject.

        Returns:
            int: Number of elements in OrderedObject.
        """

        return len(self._elements)

    def __str__(self) -> str:
        """Human-readable string representation of OrderedObject"""

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
            raise ValueError(f"Provided index '{index}' is not valid.")

        return index

    def _extend(
        self, new_elements: Union["OrderedObject", list[ObjectType]]
    ) -> None:
        """Extend OrderedObject with new elements.

        Args:
            new_elements (
                OrderedObject |
                list[Resource | IRI | Literal | Any]
            ):
                New elements to add to OrderedObject.
        """

        # If new_elements is a OrderedObject, get its elements
        if isinstance(new_elements, OrderedObject):
            new_elements = new_elements.elements

        # For every new element
        for new_element in new_elements:
            # Append it to OrderedObject
            self._append(new_element)

    def _index(
        self, element: ObjectType, start: int = 0, end: int = -1
    ) -> int:
        """Get index of element in OrderedObject.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to look for in OrderedObject.
            start (int, optional):
                Index from which to look for element.
            end (int, optional):
                Index until which to look for element.

        Returns:
            int: Index of element in OrderedObject.
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

    def count(self, element: ObjectType) -> int:
        """Count the number of times element appears in OrderedObject.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to look for in OrderedObject.

        Returns:
            int: Number of times element appears in OrderedObject.
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

    # def remove(self, element: ObjectType) -> None:
    def remove_item(self, element: ObjectType) -> None:
        """Remove element from Container,
           and raise an error if it was not present.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to remove from Container.
        """

        # Get index of element in Container
        index = self._index(element)

        # Remove it from Container
        _ = self.pop(index=index)

    def discard(self, element: ObjectType) -> None:
        """Remove element from Container,
           without raising error if it was not present.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to remove from Container.
        """

        try:
            # Get index of element in Container
            index = self._index(element)
        except ValueError:
            # If element was not in Container, do nothing
            return

        # Otherwise, remove it from Container
        _ = self.pop(index=index)

    def _append(self, element: ObjectType) -> None:
        """Append element to the end of OrderedObject."""
        raise NotImplementedError

    def clear(self) -> None:
        """Remove all elements of OrderedObject."""
        raise NotImplementedError

    def pop(self, index: int = 0) -> ObjectType:
        """Delete and return element of Container at given index."""
        raise NotImplementedError
