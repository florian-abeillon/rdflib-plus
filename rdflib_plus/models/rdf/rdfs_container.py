"""RDFS Container constructor"""

from rdflib import RDF, RDFS
from rdflib import URIRef as IRI

from rdflib_plus.definitions import RDFS_CLASSES
from rdflib_plus.models.rdf.rdfs_resource import (
    ObjectType,
    Resource,
    ResourceOrIri,
)
from rdflib_plus.models.utils.Collection import Collection
from rdflib_plus.models.utils.types import ConstraintsType


class Container(Collection):
    """RDFS Container constructor"""

    # Container's RDF type
    _type: ResourceOrIri = RDFS.Container

    # Specify that object is a RDFS Container
    # (for triple checking, among other things)
    _is_container: bool = True

    # Container's property constraints
    _constraints: ConstraintsType = Resource.update_constraints(
        RDFS_CLASSES[_type]["constraints"]
    )

    def _get_predicate(self, index: int) -> IRI:
        """Return predicate corresponding to the index-th element.

        Args:
            index (int):
                Index of element (starting at 0, not 1). Can be negative.

        Returns:
            IRI: Predicate linking Container to index-th element.
        """

        # Format index, and update it to start at 1 (not 0)
        index = self._format_index(index)
        index += 1

        # Build predicate
        predicate = RDF[f"_{index}"]

        return predicate

    def _insert(self, index: int, element: ObjectType) -> None:
        """Insert element at index-th position of Container.

        Args:
            index (int):
                Index to insert element at.
            element (ObjectType):
                Element to insert into Seq.
        """

        # Format index, so that it is positive
        index = self._format_index(index)

        # Insert element into elements list
        self._elements.insert(index, element)

        # For every element, from index-th
        for i in range(index, len(self)):
            # If i is not the last element
            if i < len(self) - 1:
                # Remove value in graph
                predicate = self._get_predicate(index)
                self.remove(predicate)

            # Get i-th element
            element = self._elements[i]

            # Update value in graph
            self.set(predicate, element)

    def _pop(self, index: int = 0) -> ObjectType:
        """Delete and return element of Container at given index.

        Args:
            index (int, optional):
                Index of element to delete and return in Container.
                Can be negative. Defaults to 0.

        Returns:
            Resource | IRI | Literal | Any: Removed element.
        """

        # Format index, and update it to start at 1 (not 0)
        index = self._format_index(index)

        # For every element from index
        for i in range(index, len(self)):
            # Remove value in graph
            predicate = self._get_predicate(i)
            self.remove(predicate)

            # If there is another element left in the Container afterwards
            if i < len(self) - 1:
                # Get next formatted element
                next_element = self._elements[i + 1]

                # Update value in graph
                self.set(predicate, next_element)

        # Get the removed element
        element = self._elements[index]

        # Remove element from elements lists
        del self._elements[index]

        return element

    def append(self, element: ObjectType) -> None:
        """Append element to the end of Container.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to append to Container.
        """

        # Append element to the elements list
        self._elements.append(element)

        # Set element's value in graph, with appropriate index
        index = len(self) - 1
        predicate = self._get_predicate(index)
        self.set(predicate, element)

    def clear(self) -> None:
        """Remove all elements of Container."""

        # For every element
        for i in range(len(self)):
            # Remove value in graph
            predicate = self._get_predicate(i)
            self.remove(predicate)

        # Empty element lists
        self._elements.clear()
