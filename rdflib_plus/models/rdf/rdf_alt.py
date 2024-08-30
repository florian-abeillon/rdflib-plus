"""RDF Alt constructor"""

import random as rd
import warnings
from typing import Optional

from rdflib import RDF, Namespace

from rdflib_plus.config import DEFAULT_CHECK_TRIPLES
from rdflib_plus.models.rdf.rdfs_container import Container
from rdflib_plus.models.rdf.rdfs_resource import ObjectType, ResourceOrIri
from rdflib_plus.models.utils.collection import Collection
from rdflib_plus.models.utils.decorator import warning_remove_default
from rdflib_plus.models.utils.types import GraphType
from rdflib_plus.namespaces import stringify_iri

# Define specific custom type
CollectionType = list[ObjectType] | set[ObjectType] | Collection


class Alt(Container):
    """RDF Alt constructor"""

    # Alt's RDF type
    _type: ResourceOrIri = RDF.Alt

    @property
    def default(self) -> Optional[ObjectType]:
        """Default element of Alt."""

        return self._elements[0] if self._elements else None

    @default.setter
    def default(self, new_default: ObjectType) -> None:
        """Set a new default element to Alt.

        Args:
            new_default (Resource | IRI | Literal | Any):
                New default element of Alt.
        """

        # Remove new default element from Alt
        self.discard_element(new_default)

        # Insert new default element
        self._insert(0, new_default)

    @property
    def alternatives(self) -> list[ObjectType]:
        """Alternatives to default of Alt."""

        return self._elements[1:] if self._elements else []

    @alternatives.setter
    def alternatives(
        self, new_alternatives: list[ObjectType] | Collection
    ) -> None:
        """Set new alternatives to Alt.

        Args:
            new_alternatives (
                list[Resource | IRI | Literal | Any]
                | Collection
            ):
                New alternatives to Alt.
        """

        # If new_alternatives is a Collection, extract its elements
        if isinstance(new_alternatives, Collection):
            new_alternatives = new_alternatives.elements

        # If necessary, remove default from new_alternatives
        default = self.default
        if default in new_alternatives:
            new_alternatives = new_alternatives.remove(default)

        # Set new_alternatives
        self.elements = [default] + new_alternatives

    def __init__(
        self,
        graph: GraphType,
        default: Optional[ObjectType] = None,
        alternatives: Optional[CollectionType] = None,
        namespace: Optional[Namespace] = None,
        local: bool = False,
        check_triples: bool = DEFAULT_CHECK_TRIPLES,
    ) -> None:
        """Initialize Alt.

        Args:
            graph (Graph | MultiGraph):
                Graph to search or create Alt into.
            default (Resource | IRI | Literal | Any | None):
                Default element of Alt. Defaults to None.
            alternatives (
                list[Resource | IRI | Literal | Any]
                | set[Resource | IRI | Literal | Any]
                | Collection
                | None,
                optional
            ):
                Alternatives to put in Alt at its creation. Defaults to None.
            namespace (Namespace | None, optional):
                Namespace to search or create Alt into. Defaults to None.
            local (bool, optional):
                Whether Alt only appears in the specified namespace.
                Defaults to False.
            check_triples (bool, optional):
                Whether to check triples that are added or set.
                Defaults to DEFAULT_CHECK_TRIPLES.
        """

        # If no alternatives are specified
        if alternatives is None or not alternatives:
            # Alt's elements list consists of default element (if specified)
            # otherwise nothing
            elements = [default] if default is not None else []

        # Otherwise, if alternatives are specified
        else:
            # If alternatives is a Collection, extract its elements
            if isinstance(alternatives, Collection):
                alternatives = alternatives.elements

            # If no default element is specified
            if default is None:
                # Take the first alternative as default
                default, *alternatives = alternatives

                # Raise warning to notify about the choice of default element
                warnings.warn(
                    f"{stringify_iri(self._type)}: Using first element "
                    f"'{default}' as default."
                )

            # Build full elements list, removing any duplicates
            elements = [default] + [
                alternative
                for alternative in set(alternatives)
                if alternative != default
            ]

        super().__init__(
            graph,
            elements=elements,
            namespace=namespace,
            local=local,
            check_triples=check_triples,
        )

    def _append(self, element: ObjectType) -> None:
        """Add alternative to Alt.

        Args:
            element (Resource | IRI | Literal | Any):
                Alternative to add to Alt.
        """

        # If the new alternative is already in Alt, raise a warning
        if element == self.default:
            warnings.warn(
                f"{self}': Trying to set new alternative '{element}' "
                "to Alt, but it is already its default element. Not adding it "
                "again."
            )
        elif element in self.alternatives:
            warnings.warn(
                f"{self}': Trying to set new alternative '{element}' "
                "to Alt, but it is already in Alt. Not adding it again."
            )

        # Otherwise, add it
        else:
            super()._append(element)

    def add_alternative(self, element: ObjectType) -> None:
        """Add an alternative to Alt.

        Args:
            element (Resource | IRI | Literal | Any):
                New alternative to add to Alt.
        """
        self._append(element)

    def any_alternative(self) -> Optional[ObjectType]:
        """Return any alternative of Alt.

        Returns:
            Resource | IRI | Literal | Any | None:
                If any, random alternative from Alt. Otherwise, None.
        """

        # If Alt does not have any elements, return None
        if len(self._elements) < 2:
            return None

        # Randomly pick element
        element = rd.choice(self.elements[1:])

        return element

    def copy(self, **kwargs) -> "Alt":
        """Return a shallow copy of Alt."""

        if self._elements:
            return self.__class__(
                self.graph,
                default=self._elements[0],
                alternatives=self._elements[1:],
                **kwargs,
            )
        return self.__class__(self.graph, **kwargs)

    def count(self, element: ObjectType) -> int:
        """Count the number of times element appears in Alt.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to look for in Alt.

        Returns:
            int: Number of times element appears in Alt.
        """

        warnings.warn(
            f"{self}: Calling Alt's 'count()' method does not make sense, as "
            "Alt does not allow duplicated values. Prefer using the 'in' "
            "operator."
        )

        # Duplicated values are not allowed in Alt, value is 1 or 0
        return int(element in self)

    @warning_remove_default
    def discard_element(self, element: ObjectType) -> None:
        """Remove element from Alt,
           without raising error if it was not present.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to remove from Alt.
        """
        super().discard_element(element)

    @warning_remove_default
    def remove_element(self, element: ObjectType) -> None:
        """Remove element from Alt,
           and raise an error if it was not present.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to remove from Alt.
        """
        super().remove_element(element)
