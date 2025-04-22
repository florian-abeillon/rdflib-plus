"""RDF Alt constructor"""

import random as rd
import warnings
from typing import Optional

from rdflib import RDF, Graph, Namespace

from rdflib_plus.config import DEFAULT_CHECK_TRIPLES
from rdflib_plus.models.rdf.rdfs_container import Container
from rdflib_plus.models.rdf.rdfs_resource import ObjectType, ResourceOrIri
from rdflib_plus.models.utils.collection import Collection
from rdflib_plus.namespaces import stringify_iri

# Define specific custom type
CollectionType = list[ObjectType] | set[ObjectType] | Collection


class Alt(Container):
    """RDF Alt constructor"""

    # Alt's RDF type
    _type: ResourceOrIri = RDF.Alt

    @property
    def alternatives(self) -> list[ObjectType]:
        """Alternatives to default of Alt."""
        return self._elements[1:] if self._elements else []

    @property
    def default(self) -> Optional[ObjectType]:
        """Default element of Alt."""
        return self._elements[0] if self._elements else None

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
        # Remember whether default was already set
        self._was_default_set = self.default is not None
        self.elements = self._build_elements(self.default, new_alternatives)

    @default.setter
    def default(self, new_default: ObjectType) -> None:
        """Set a new default element to Alt.

        Args:
            new_default (Resource | IRI | Literal | Any):
                New default element of Alt.
        """

        # If duplicated elements are not allowed
        if not self._allow_duplicates:

            # If new default is the same as before, do not do anything
            try:
                _ = self._index(new_default, end=0)
                return
            except ValueError:
                pass

            # Otherwise, remove new default element from Alt
            # if it was already included
            self.discard_element(new_default)

        # Insert new default at the start of element list
        self._insert(0, new_default)

    def __init__(
        self,
        graph: Graph,
        default: Optional[ObjectType] = None,
        alternatives: Optional[CollectionType] = None,
        elements: Optional[CollectionType] = None,
        allow_duplicates: bool = True,
        namespace: Optional[Namespace] = None,
        local: bool = False,
        check_triples: bool = DEFAULT_CHECK_TRIPLES,
    ) -> None:
        """Initialize Alt.

        Args:
            graph (Graph):
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
            elements (
                list[Resource | IRI | Literal | Any]
                | set[Resource | IRI | Literal | Any]
                | Collection
                | None,
                optional
            ):
                Elements to put in Alt at its creation.
                Defaults to None.
            allow_duplicates (bool, optional):
                Whether to allow duplicated alternatives. Defaults to True.
            namespace (Namespace | None, optional):
                Namespace to search or create Alt into. Defaults to None.
            local (bool, optional):
                Whether Alt only appears in the specified namespace.
                Defaults to False.
            check_triples (bool, optional):
                Whether to check triples that are added or set.
                Defaults to DEFAULT_CHECK_TRIPLES.
        """

        # Remember whether to allow duplicated elements
        self._allow_duplicates = allow_duplicates

        # TODO: Not very elegant
        # Remember whether a default was specified
        self._was_default_set = default is not None

        # If not elements are specified
        if elements is None:
            # Build element list from default and alternatives
            elements = self._build_elements(default, alternatives)

        # Otherwise
        else:
            # Make sure that no default nor alternatives were specified
            assert default is None, (
                f"{stringify_iri(self._type)}: Cannot specify default element "
                "when specifying elements. Use 'alternatives' kwarg instead."
            )
            assert alternatives is None, (
                f"{stringify_iri(self._type)}: Cannot specify alternatives "
                "when specifying elements. Use either 'elements' or "
                "'alternatives' kwarg."
            )

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

        # If duplicated elements are allowed, add element
        if self._allow_duplicates:
            super()._append(element)

        # Otherwise, try to find element among Alt's elements
        else:
            try:
                index = self._index(element)

                # TODO: Test for warnings
                # If success, raise a warning
                if index == 0:
                    warnings.warn(
                        f"{self}': Trying to set new alternative '{element}' "
                        "to Alt, but it is already its default element. "
                        "Not adding it again."
                    )
                else:
                    warnings.warn(
                        f"{self}': Trying to set new alternative '{element}' "
                        "to Alt, but it is already in Alt. "
                        "Not adding it again."
                    )

            # Otherwise, add element
            except ValueError:
                super()._append(element)

    def _build_elements(
        self, default: ObjectType, alternatives: list[ObjectType] | Collection
    ) -> list[ObjectType]:
        """Build element list from default object and alternatives list.

        Args:
            default (Resource | IRI | Literal | Any]):
                Dfault of Alt.
            alternatives (
                list[Resource | IRI | Literal | Any]
                | Collection
            ):
                Alternatives of Alt.

        Returns:
            list[Resource | IRI | Literal | Any]:
                List of elements of Alt.
        """

        # If no alternatives are specified
        if alternatives is None or not alternatives:
            # Alt's element list consists of default element (if specified)
            # otherwise empty list
            return [default] if default is not None else []

        # Otherwise, if alternatives is a Collection object
        if isinstance(alternatives, Collection):
            alternatives = alternatives.elements

        # If no default element is specified
        if default is None:
            # Take the first alternative as default
            default, *alternatives = alternatives

        # Build full elements list
        elements = [default] + alternatives

        return elements

    def _extend(self, new_elements: list[ObjectType] | Collection) -> None:
        """Extend Alt with new elements.

        Args:
            new_elements (
                list[Resource | IRI | Literal | Any]
                | Collection
            ):
                New elements to add to Alt.
        """

        # Check whether Alt was empty before
        was_alt_empty = len(self) == 0

        # Extend Alt
        super()._extend(new_elements)

        # If Alt was empty, and was extended with new elements
        if not self._was_default_set and was_alt_empty and new_elements:
            # TODO: Raises warning even if initializing element with default
            # Raise warning to notify about the choice of default element
            warnings.warn(
                f"{stringify_iri(self._type)}: Using element "
                f"'{self.default}' as default."
            )
            self._was_default_set = False

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

        # If Alt does not have any alternatives, return None
        if len(self._elements) < 2:
            return None

        # Randomly pick an alternative
        element = rd.choice(self.elements[1:])

        return element

    def copy(self) -> "Alt":
        """Return a shallow copy of Alt."""

        kwargs = {
            "allow_duplicates": self._allow_duplicates,
            "check_triples": self._check_triples,
        }
        if self._elements:
            kwargs["default"] = self.default
            kwargs["alternatives"] = self.alternatives

        return self.__class__(self.graph, **kwargs)

    def count(self, element: ObjectType) -> int:
        """Count the number of times element appears in Alt.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to look for in Alt.

        Returns:
            int: Number of times element appears in Alt.
        """

        # If duplicates are not allowed, raise a warning
        if not self._allow_duplicates:
            # TODO: Test for warning
            warnings.warn(
                f"{self}: Calling Alt's 'count()' method does not make sense, "
                "as Alt does not allow duplicated values. "
                "Prefer using the 'in' operator instead."
            )

        return super().count(element)

    def remove_element(self, element: ObjectType) -> None:
        """Remove element from Alt,
           and raise an error if it was not present.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to remove from Alt.
        """

        # Remember default before discarding element
        default_before = self.default

        # Discard element
        super().remove_element(element)

        # If element to remove is Alt's default
        if self.default != default_before:
            # TODO: Test for warning
            # Raise a warning
            warnings.warn(
                f"{self}: Default element removed. New default set to "
                f"'{self.default}'."
            )
