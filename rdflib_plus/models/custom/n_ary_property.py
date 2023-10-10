"""n-ary Property constructor"""

from typing import Optional

from rdflib import Namespace
from rdflib import URIRef as IRI

from rdflib_plus.config import (
    DEFAULT_CHECK_TRIPLES,
    DEFAULT_HIERARCHICAL_PATH,
    DEFAULT_LANGUAGE,
)
from rdflib_plus.models.rdf.rdf_property import Property
from rdflib_plus.models.rdf.rdfs_class import Class
from rdflib_plus.models.rdf.rdfs_resource import (
    ObjectType,
    Resource,
    ResourceOrIri,
)
from rdflib_plus.models.utils.types import ConstraintsType, GraphType, LangType
from rdflib_plus.namespaces import stringify_iri

# Define specific custom types
SuperPropertyType = Property | IRI | list[Property | IRI]
ParsedPairType = tuple[ResourceOrIri, ObjectType, bool]
UnparsedPairType = tuple[ResourceOrIri, ObjectType] | ParsedPairType
UnparsedPairListType = list[UnparsedPairType]


class ResourcePair(tuple):
    """Useful class for arguments of NaryProperty.__call__()"""

    def __new__(
        cls,
        resource_1: ResourceOrIri,
        resource_2: ObjectType,
        to_set: bool = False,
    ):
        """Initialize ResourcePair.

        Args:
            resource_1 (Resource | IRI):
                First resource (either the triple subject or predicate).
            resource_2 (Resource | IRI | Literal | Any):
                Second resource (either the triple predicate if resource_1
                is the subject, or the triple object if resource_1 is
                the predicate).
            to_set (bool, optional):
                Whether the triple should be set (instead of added).
                Defaults to False.
        """

        args = (resource_1, resource_2, to_set)
        return super().__new__(cls, args)


class NaryProperty(Property):
    """n-ary Property constructor"""

    def __init__(
        self,
        graph: GraphType,
        label: str,
        namespace: Optional[Namespace] = None,
        super_property: Optional[SuperPropertyType] = None,
        hierarchical_path: bool = DEFAULT_HIERARCHICAL_PATH,
        lang: LangType = DEFAULT_LANGUAGE,
        check_triples: bool = DEFAULT_CHECK_TRIPLES,
        constraints: Optional[ConstraintsType] = None,
    ) -> None:
        """Initialize Property.

        Args:
            graph (Graph | MultiGraph):
                Graph to search or create Property into.
            label (str):
                Property's label.
            namespace (Optional[Namespace], optional):
                Namespace to search or create Property into. Defaults to None.
            super_property (Optional[Property | IRI | list[Property | IRI]],
                            optional):
                Property's super-property. Defaults to None.
            hierarchical_path (bool, optional):
                Whether to include Class's parent hierarchy in its path.
                Defaults to DEFAULT_HIERARCHICAL_PATH.
            lang (Optional[str], optional):
                Property's language. Defaults to DEFAULT_LANGUAGE.
            check_triples (bool, optional):
                Whether to check triples that are added or set using Property.
                Defaults to DEFAULT_CHECK_TRIPLES.
            constraints (Optional[dict[IRI, dict[str, Any]]], optional):
                Class's specific constraints.
                Defaults to None.
        """

        super().__init__(
            graph,
            label,
            namespace=namespace,
            super_property=super_property,
            hierarchical_path=hierarchical_path,
            lang=lang,
            check_triples=check_triples,
            constraints=constraints,
        )

        # n-ary Property has instances, encoded as blank nodes
        self.bnode = True

    def _get_label_inverse(self) -> None:
        """Null function, as n-ary Property cannot have an inverse.

        Returns:
            None: None.
        """

        return None

    def __call__(
        self,
        incoming: Optional[UnparsedPairListType] = None,
        outgoing: Optional[UnparsedPairListType] = None,
        graph: Optional[GraphType] = None,
        check_triples: Optional[bool] = None,
    ) -> Resource:
        """Create instance of n-ary property

        Args:
            incoming (
                Optional[list[
                    tuple[Resource | IRI, Resource | IRI | Literal | Any] |
                    tuple[Resource | IRI, Resource | IRI | Literal | Any, bool]
                ]],
                optional
            ):
                Subject and predicate of triple to add to instance,
                with indication whether to add (default behavior) or to set it.
                Defaults to None.
            outgoing (
                Optional[list[
                    tuple[Resource | IRI, Resource | IRI | Literal | Any] |
                    tuple[Resource | IRI, Resource | IRI | Literal | Any, bool]
                ]],
                optional
            ):
                Predicate and object of triple to add from instance,
                with indication whether to add (default behavior) or to set it.
                Defaults to None.
            graph (Optional[Graph | MultiGraph], optional):
                Graph to search or create instance into. Defaults to None.
            check_triples (Optional[bool], optional):
                Whether to check triples that are added or set using Resource.
                Defaults to None.

        Returns:
            Resource: Instance of n-ary property
        """

        # If associated property does not allow blank nodes
        if not self.bnode:
            # Raise an error
            raise ValueError(
                f"{stringify_iri(self.iri)}: Trying to create instance of "
                "non-n-ary property. Please use Property as is to link resources "
                "(no need to create an instance of it)."
            )

        Class.__call__(self, graph=graph, check_triples=check_triples)

        # Initialize list of triples to add or set
        triples = []

        # If incoming resource-property pairs are specified
        if incoming is not None:
            # For every resource-property pair
            for s_p in incoming:
                # Parse the pair
                s, p, to_set = ResourcePair(*s_p)

                # Add them to triples
                triples.append((s, p, self, to_set))

        # If outgoing property-object pairs are specified
        if outgoing is not None:
            # For every property-object pair
            for p_o in outgoing:
                # Parse the pair
                p, o, to_set = ResourcePair(*p_o)

                # Add them to triples
                triples.append((self, p, o, to_set))

        # For every triple to add or set
        for s, p, o, to_set in triples:
            # Set it
            if to_set:
                s.set(p, o)
            # Or add it
            else:
                s.add(p, o)
