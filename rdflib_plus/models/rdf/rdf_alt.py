"""RDF Alt constructor"""

import warnings
from typing import Optional

from rdflib import RDF, Namespace

from rdflib_plus.config import DEFAULT_CHECK_TRIPLES
from rdflib_plus.models.rdf.rdf_bag import Bag, CollectionType
from rdflib_plus.models.rdf.rdfs_resource import ObjectType, ResourceOrIri
from rdflib_plus.models.utils.decorator import warning_remove_default
from rdflib_plus.models.utils.types import GraphType


class Alt(Bag):
    """RDF Alt constructor"""

    # Alt's RDF type
    _type: ResourceOrIri = RDF.Alt

    @property
    def default(self) -> Optional[ObjectType]:
        """Default element of Alt."""

        return self._elements[0] if self._elements else None

    @default.setter
    def default(self, new_default: ObjectType, keep: bool = True) -> None:
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
            _ = self._pop(0)

        # Remove new default element from Alt
        self.discard_element(new_default)

        # Insert new default element
        self._insert(0, new_default)

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
        if alternatives is None or len(alternatives) == 0:
            # Alt's elements list consists of default element (if specified)
            # otherwise nothing
            elements = [default] if default is not None else []

        # Otherwise, if alternatives are specified
        else:
            # If no default element is specified
            if default is None:
                # Randomly pick an index
                index_default = self._any_index(alternatives)

                # Pop element out of alternatives
                default = alternatives.pop(index_default)

                # Raise warning to notify about the choice of default element
                warnings.warn(f"Using element {default} as Alt's default.")

            # Build full elements list
            elements = [default] + alternatives

        super().__init__(
            graph,
            elements=elements,
            namespace=namespace,
            local=local,
            check_triples=check_triples,
        )

    @warning_remove_default
    def discard_element(
        self, element: ObjectType, n: Optional[int] = None
    ) -> None:
        """Remove element from Alt,
           without raising error if it was not present.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to remove from Alt.
            n (int | None, optional): Max number of elements to remove from Alt.
        """

        super().discard_element(element, n=n)

    @warning_remove_default
    def remove_element(
        self, element: ObjectType, n: Optional[int] = None
    ) -> None:
        """Remove element from Alt,
           and raise an error if it was not present.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to remove from Alt.
            n (int | None, optional): Max number of elements to remove from Alt.
        """

        super().remove_element(element, n=n)
