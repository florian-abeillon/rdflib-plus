"""RDF Alt constructor"""

import random as rd
import warnings
from typing import Optional

from rdflib import RDF, Namespace

from rdflib_plus.config import DEFAULT_CHECK_TRIPLES
from rdflib_plus.models.rdf.rdfs_container import Container
from rdflib_plus.models.rdf.rdfs_resource import ObjectType, ResourceOrIri
from rdflib_plus.models.utils.collection import Collection
from rdflib_plus.models.utils.types import GraphType
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
        self.elements = self._build_elements(self.default, new_alternatives)

        # # If new_alternatives is a Collection, extract its elements
        # if isinstance(new_alternatives, Collection):
        #     new_alternatives = new_alternatives.elements

        # # If necessary, remove default from new_alternatives
        # default = self.default
        # # TODO
        # if default in new_alternatives:
        #     new_alternatives = new_alternatives.remove(default)

        # # Set new_alternatives
        # self.elements = [default] + new_alternatives

    @default.setter
    def default(self, new_default: ObjectType) -> None:
        """Set a new default element to Alt.

        Args:
            new_default (Resource | IRI | Literal | Any):
                New default element of Alt.
        """

        # Remove new default element from Alt, if it was already included
        self.discard_element(new_default)

        # Insert new default element
        self._insert(0, new_default)

    def __init__(
        self,
        graph: GraphType,
        default: Optional[ObjectType] = None,
        alternatives: Optional[CollectionType] = None,
        elements: Optional[CollectionType] = None,
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
            elements (
                list[Resource | IRI | Literal | Any]
                | Collection
                | None,
                optional
            ):
                Elements to put in Alt at its creation.
                Defaults to None.
            namespace (Namespace | None, optional):
                Namespace to search or create Alt into. Defaults to None.
            local (bool, optional):
                Whether Alt only appears in the specified namespace.
                Defaults to False.
            check_triples (bool, optional):
                Whether to check triples that are added or set.
                Defaults to DEFAULT_CHECK_TRIPLES.
        """

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

        # # If no alternatives are specified
        # if alternatives is None or not alternatives:
        #     # Alt's elements list consists of default element (if specified)
        #     # otherwise nothing
        #     element_list = [default] if default is not None else []

        # # Otherwise, if alternatives are specified
        # else:
        #     # If alternatives is a Collection, extract its elements
        #     if isinstance(alternatives, Collection):
        #         alternatives = alternatives.elements

        #     # If no default element is specified
        #     if default is None:
        #         # Take the first alternative as default
        #         default, *alternatives = alternatives

        #         # Raise warning to notify about the choice of default element
        #         warnings.warn(
        #             f"{stringify_iri(self._type)}: Using first element "
        #             f"'{default}' as default."
        #         )

        #     # Build full elements list
        #     element_list = [default] + alternatives

        # # Format all elements as they would be in the graph
        # element_list_formatted = [
        #     self._format_object(element) for element in element_list
        # ]

        # # For every element of the list
        # elements = []
        # self._elements_formatted = []
        # for i, (element, element_formatted) in enumerate(
        #     zip(element_list, element_list_formatted)
        # ):
        #     # If element is default, or if its formatted form did not appear yet
        #     if (
        #         i < 1
        #         or element_formatted not in element_list_formatted[: i - 1]
        #     ):
        #         # Add it and its formatted form to the lists
        #         elements.append(element)
        #         self._elements_formatted.append(element_formatted)

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

        try:
            # Try to find element among Alt's elements
            index = self._index(element)

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
                    "to Alt, but it is already in Alt. Not adding it again."
                )

        # Otherwise
        except ValueError:
            # Add element
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

        # If no default element is specified
        if default is None:
            # Take the first alternative as default
            default, *alternatives = alternatives

            # Raise warning to notify about the choice of default element
            warnings.warn(
                f"{stringify_iri(self._type)}: Using first element "
                f"'{default}' as default."
            )

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
        if was_alt_empty and new_elements:
            # Raise warning to notify about the choice of default element
            warnings.warn(
                f"{stringify_iri(self._type)}: Using element "
                f"'{self.default}' as default."
            )

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

        if self._elements:
            return self.__class__(
                self.graph,
                default=self._elements[0],
                alternatives=self._elements[1:],
                check_triples=self._check_triples,
            )
        return self.__class__(
            self.graph,
            check_triples=self._check_triples,
        )

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

    def discard_element(self, element: ObjectType) -> None:
        """Remove element from Alt,
           without raising error if it was not present.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to remove from Alt.
        """

        # Check whether element to remove is Alt's default
        element_formatted = self._format_object(element)
        removing_default = element_formatted == self._elements_formatted[0]

        # Discard element
        super().discard_element(element)

        # If element to remove is Alt's default
        if removing_default:
            # Raise a warning
            warnings.warn(
                f"{self}: Default element removed. New default set to "
                f"'{self.default}'."
            )

    def remove_element(self, element: ObjectType) -> None:
        """Remove element from Alt,
           and raise an error if it was not present.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to remove from Alt.
        """

        # Check whether element to remove is Alt's default
        element_formatted = self._format_object(element)
        removing_default = element_formatted == self._elements_formatted[0]

        # Discard element
        super().remove_element(element)

        # If element to remove is Alt's default
        if removing_default:
            # Raise a warning
            warnings.warn(
                f"{self}: Default element removed. New default set to "
                f"'{self.default}'."
            )
