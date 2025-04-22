"""RDFS Container constructor"""

from rdflib import RDF, RDFS
from rdflib import URIRef as IRI

from rdflib_plus.definitions import RDFS_CLASSES
from rdflib_plus.models.rdf.rdfs_resource import ObjectType, ResourceOrIri
from rdflib_plus.models.utils.collection import Collection
from rdflib_plus.models.utils.decorators import formatted_index
from rdflib_plus.models.utils.types import ConstraintsType


class Container(Collection):
    """RDFS Container constructor."""

    # Container's RDF type
    _type: ResourceOrIri = RDFS.Container

    # Specify that object is a RDFS Container
    # (for triple checking, among other things)
    _is_container: bool = True

    # Container's property constraints
    _constraints: ConstraintsType = Collection.update_constraints(
        RDFS_CLASSES[_type]["constraints"]
    )

    def _append(self, element: ObjectType) -> None:
        """Append element to the end of Container.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to append to Container.
        """

        # Append element to the elements list
        self._elements.append(element)

        # Set element's value in graph, with appropriate index
        predicate = self._get_predicate(len(self) - 1)
        self.set(predicate, element)

        # Append element's formatted form to the elements list
        self._elements_formatted.append(self.get_value(predicate))

    def _get_predicate(self, index: int) -> IRI:
        """Return predicate corresponding to the index-th element.

        Args:
            index (int):
                Index of element (starting at 0, not 1). Can be negative.

        Returns:
            IRI: Predicate linking Container to index-th element.
        """
        return RDF[f"_{index + 1}"]

    @formatted_index(inserting=True)
    def _insert(self, index: int, new_element: ObjectType) -> None:
        """Insert element at index-th position of Container.

        Args:
            index (int):
                Index to insert element at.
            new_element (ObjectType):
                Element to insert into Container.
        """

        # Insert new element into elements list
        self._elements.insert(index, new_element)

        # For every element from index-th on
        for i, element in enumerate(self._elements[index:]):
            # Update value in graph
            predicate = self._get_predicate(index + i)
            self.set(predicate, element, replace=True)

        # Insert its formatted form into elements list
        predicate = self._get_predicate(index)
        self._elements_formatted.insert(index, self.get_value(predicate))

    @formatted_index()
    def _pop(self, index: int) -> ObjectType:
        """Delete and return element of Container at given index.

        Args:
            index (int):
                Index of element to delete and return in Container.
                Can be negative.

        Returns:
            Resource | IRI | Literal | Any: Removed element.
        """

        # For every element from index on
        for i, element in enumerate(self._elements[index + 1 :]):
            # Update value in graph
            predicate = self._get_predicate(index + i)
            self.replace(predicate, element)

        # Remove link to element in graph
        predicate = self._get_predicate(len(self) - 1)
        self.remove(predicate)

        # Pop the element to be removed
        element = self._elements.pop(index)
        del self._elements_formatted[index]

        return element

    def clear(self) -> None:
        """Remove all elements of Container."""

        # For every element, remove value in graph
        for i in range(len(self)):
            predicate = self._get_predicate(i)
            self.remove(predicate)

        # Empty element lists
        self._elements.clear()
        self._elements_formatted.clear()
