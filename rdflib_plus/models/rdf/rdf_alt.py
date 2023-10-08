"""RDF Alt constructor"""

import random
from typing import Optional

from rdflib import RDF, Namespace

from rdflib_plus.models.rdf.rdfs_container import Container
from rdflib_plus.utils import GraphType, ObjectType, ResourceOrIri

# Define specific custom type
AlternativesType = list[ObjectType] | set[ObjectType]


class Alt(Container):
    """RDF Alt constructor"""

    # Alt's RDF type
    _type: ResourceOrIri = RDF.Alt

    @property
    def default(self) -> ObjectType:
        """Default element of Alt."""

        return self._elements[0]

    def __init__(
        self,
        graph: GraphType,
        default: Optional[ObjectType] = None,
        alternatives: Optional[AlternativesType] = None,
        namespace: Optional[Namespace] = None,
    ) -> None:
        """Initialize Alt.

        Args:
            graph (Graph | MultiGraph):
                Graph to search or create Container into.
            default (Optional[Resource | IRI | Literal | Any]):
                Default element of Alt. Defaults to None.
            alternatives (
                Optional[
                    list[Resource | IRI | Literal | Any] |
                    set[Resource | IRI | Literal | Any] |
                ],
                optional
            ):
                Alternatives to put in Alt at its creation. Defaults to None.
            namespace (Optional[Namespace], optional):
                Namespace to search or create Resource into. Defaults to None.
        """

        # Remove duplicates from alternative
        # then turn it into list
        alternatives = list(set(alternatives))

        # If no default element is specified
        if default is None:
            # Randomly pick an index
            index_default = self._any_index(alternatives)

            # Pop element out of alternatives
            default = alternatives.pop(index=index_default)

        # Otherwise, if default is also in alternatives
        else:
            if self.default in alternatives:
                # Remove it from alternatives
                alternatives.remove(default)

        # Build full elements list
        elements = [default] + alternatives

        super().__init__(graph, elements=elements, namespace=namespace)

    def _any_index(
        self,
        elements: Optional[list[ObjectType]] = None,
        include_default: bool = True,
    ) -> int:
        """Return any element of elements.

        Args:
            elements (
                Optional[list[Resource | IRI | Literal | Any]],
                optional
            ):
                Elements list to pick element from. Defaults to None.
            include_default (bool, optional):
                Whether to consider default element. Defaults to True.

        Returns:
            int: Index of element randomly picked from Alt.
        """

        # If no elements list is specified
        if elements is None:
            # Use Alt's elements list
            elements = self.elements

        # Include default element or not
        start = 0 if include_default else 1

        # Randomly choose index of element ot pick
        index = random.randint(start, len(elements))

        return index

    def _append(self, element: ObjectType) -> None:
        """Add element as an alternative to Alt.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to add to Alt as an alternative.
        """

        # Check if element is already in elements list
        try:
            _ = self._index(element)
        # If not
        except ValueError:
            # Append element
            super()._append(element)

    def any(self, include_default: bool = True) -> ObjectType:
        """Return any element of Alt.

        Args:
            include_default (bool, optional):
                Whether to consider default element. Defaults to True.

        Returns:
            Resource | IRI | Literal | Any: Random element from Alt.
        """

        # Randomly pick index
        index = self._any_index(
            self._elements, include_default=include_default
        )

        # Get associated element
        element = self._elements[index]

        return element

    def set_default(self, new_default: ObjectType, keep: bool = True) -> None:
        """Set a new default element to Alt.

        Args:
            new_default (Resource | IRI | Literal | Any):
                New default element of Alt.
            keep (bool, optional):
                Whether to keep old default element in alternatives.
                Defaults to True.
        """

        # If old default element should not be kept
        if not keep:
            # Remove it
            _ = self.pop(0)

        # Remove new default element from Alt
        self.discard(new_default)

        # Insert new default element
        self._insert(0, new_default)

    def add_alternative(self, element: ObjectType) -> None:
        """Add element as an alternative to Alt.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to add to Alt as an alternative.
        """

        self._append(element)

    def add_alternatives(
        self, new_elements: list[ObjectType] | set[ObjectType]
    ) -> None:
        """Add new elements to Alt as alternatives.

        Args:
            new_elements (
                list[Resource | IRI | Literal | Any] |
                set[Resource | IRI | Literal | Any]
            ):
                New elements to add to Alt.
        """

        # Remove duplicates
        new_elements = list(set(new_elements))

        # For every new element
        for new_element in new_elements:
            # Add it to Alt as an alternative
            self.add_alternative(new_element)
