"""Base Resource class"""

import warnings
from typing import Any, Optional

from rdflib import (
    DCTERMS,
    RDF,
    RDFS,
    SKOS,
    ConjunctiveGraph,
    Literal,
    Namespace,
)
from rdflib import URIRef as IRI
from rdflib.resource import Resource as RdfsResource

from ..utils import NS_DEFAULT, legalize_iri
from .types import GraphType, IdentifierType, LangType
from .utils import DEFAULT_IDENTIFIER_PROPERTY

ResourceOrIri = "Resource" | IRI
ObjectType = "Resource" | IRI | Literal | Any


class Resource(RdfsResource):
    """Base triplestore resource"""

    # Property that links Resource to its identifier
    _identifier_property: IRI | dict[str, IRI] = DEFAULT_IDENTIFIER_PROPERTY

    # Resource's RDFS type
    _type: ResourceOrIri = RDFS.Resource

    def __init__(
        self,
        graph: GraphType,
        identifier: Optional[IdentifierType] = None,
        label: Optional[str] = None,
        iri: Optional[IRI] = None,
        path: Optional[list[str]] = None,
        namespace: Optional[Namespace] = None,
        lang: LangType = None,
    ):
        """Initialize Resource.

        Args:
            graph (Graph | ConjunctiveGraph):
                Graph to search or create Resource into.
            identifier (Optional[str | int], optional):
                Resource's identifier. Defaults to None.
            label (Optional[str], optional):
                Resource's label. Defaults to None.
            iri (Optional[IRI], optional):
                Resource's IRI. Defaults to None.
            path (Optional[list[str]], optional):
                Resource's base path. Defaults to None.
            namespace (Optional[Namespace], optional):
                Namespace to search or create Resource into. Defaults to None.
            lang (Optional[str], optional):
                Resource's language. Defaults to None.
        """

        assert identifier is not None or label is not None or iri is not None

        # Set language and path
        self.lang = lang
        self.path = path if path is not None else [self._type.fragment]

        # If an IRI is directly specified
        if iri is not None:
            # Just create a RdfsResource using IRI
            super().__init__(graph, iri)
            return

        # Strip label
        if label is not None:
            label = label.strip()

        # If no identifier is specified
        if identifier is None:
            # Use label as identifier
            identifier = label

            # Get appropriate label ID given lang
            if isinstance(self._identifier_property, dict):
                self._identifier_property = self._identifier_property[
                    self.lang
                ]

        # Build Resource's IRI
        iri = self.build_iri(identifier)

        # If Resource was never initialized before,
        # Add type and identifier to the specified graph
        if not (iri, None, None) in graph:
            self.initialize_resource(graph, iri, label)

        # Set entire graph as an attribute
        # ie. not just subgraph, if applicable
        self._graph_full = graph

        # If a namespace is specified
        if namespace is not None:
            # If Resource is not linked to its namespace in the graph
            if not (iri, DCTERMS.source, namespace) in graph:
                # Add Resource's source namespace
                resource = Resource(graph, iri=iri)
                resource.add(DCTERMS.source, IRI(namespace))

            # If ConjunctiveGraph, get specified subgraph
            if isinstance(graph, ConjunctiveGraph):
                graph = graph.get_context(namespace)

        # Create RdfsResource in appropriate graph
        super().__init__(graph, iri)

    @staticmethod
    def format_identifier(identifier: IdentifierType) -> str:
        """Format Resource's identifier.

        Args:
            identifier (str | int):
                Resource's identifier.

        Returns:
            str: Formatted Resource's identifier.
        """

        return str(identifier)

    def build_iri(
        self, identifier: IdentifierType, namespace: Namespace = NS_DEFAULT
    ) -> IRI:
        """Build Resource's IRI from its identifier.

        Args:
            identifier (str | int):
                Resource's identifier.
            namespace (Namespace, optional):
                Resource's namespace. Defaults to NS_DEFAULT.

        Returns:
            IRI: Resource's IRI.
        """

        # Format Resource's identifier, and create its fragment from it
        identifier = self.format_identifier(identifier)
        self.identifier = legalize_iri(identifier)

        # Build Resource's path, and then its IRI from it
        path = self.build_path(self.identifier)
        iri = namespace[path]

        return iri

    def build_path(self, identifier: str) -> str:
        """Add Resource's identifier to IRI path.

        Args:
            identifier (str):
                Resource's identifier.

        Returns:
            str: Full Resource's IRI path.
        """

        # Build Resource's base path
        path = "/".join(self.path)

        # TODO: When different identifier properties are used
        #       with the same type of resources, as two different
        #       resources may have the same fragment.
        #       HPrepending "self._identifier_property.fragment"
        #       to the fragment solves the problem, but resources
        #       become harder to fetch, as one needs the resource's
        #       own identifier property to find it.
        #
        # identifier_property = self._identifier_property.fragment
        # fragment = f"{identifier_property}={identifier}"
        # path = f"{path}#{fragment}"

        # Add identifier to path as a fragment
        path = f"{path}#{identifier}"

        return path

    def initialize_resource(
        self, graph: GraphType, iri: IRI, label: Optional[str]
    ) -> None:
        """Create RDFS Resource

        Args:
            graph (Graph | ConjunctiveGraph):
                Graph to search or create Resource into.
            iri (IRI):
                Resource's IRI.
            label (Optional[str]):
                Resource's label.
        """

        # Create resource
        resource = Resource(graph, iri=iri)

        # Add its type and identifier
        resource.add(RDF.type, self._type)
        resource.set(self._identifier_property, self.identifier)

        # If a label is specified
        if label is not None:
            # Add it as SKOS.prefLabel
            resource.set_pref_label(label, lang=self.lang)

    def get_attribute(self, predicate: ResourceOrIri) -> IRI | Literal:
        """Get value of (unique) attribute.

        Args:
            predicate (Resource | IRI):
                Predicate that links to target attribute.

        Returns:
            IRI | Literal: Target attribute value.
        """

        return self._graph_full.value(self._identifier, predicate, any=False)

    def prepare_p_o(
        self,
        p: ResourceOrIri,
        o: ObjectType,
        lang: LangType = None,
    ) -> tuple[IRI, IRI | Literal]:
        """Prepare predicate and object, to be added to triplestore.

        Args:
            p (Resource | IRI):
                Predicate of triple.
            o (Resource | IRI | Literal | Any):
                Object of triple.
            lang (Optional[str], optional):
                Language of object. Defaults to None.

        Returns:
            tuple[IRI, IRI | Literal]: Prepared predicate and object.
        """

        # If p is a Resource, get its IRI
        if isinstance(p, Resource):
            p = p.identifier

        # If o is a Resource, get its IRI
        if isinstance(o, Resource):
            o = o.identifier

        # Otherwise, if o is neither a plain IRI nor a Literal
        elif not isinstance(o, (IRI, Literal)):
            # If o is an empty string, raise warning
            if o == "":
                warnings.warn(
                    f"{self._identifier}: Empty string is trying to be set or "
                    f"added using predicate '{p}'"
                )

            # Format o into a Literal
            if lang is None:
                lang = self.lang
            o = Literal(o, lang=lang)

        return p, o

    def add(
        self,
        p: ResourceOrIri,
        o: ObjectType,
        lang: LangType = None,
    ) -> None:
        """Add triple to self._graph.

        Args:
            p (Resource | IRI):
                Predicate of triple.
            o (Resource | IRI | Any):
                Object of triple.
            lang (Optional[str], optional):
                Language of object. Defaults to None.
        """

        # Prepare predicate and object
        p, o = self.prepare_p_o(p, o, lang=lang)

        # Add object o to Resource, using predicate p
        super().add(p, o)

    def set(
        self,
        p: ResourceOrIri,
        o: ObjectType,
        lang: LangType = None,
        force: bool = False,
    ) -> None:
        """Set triple to self._graph.

        Args:
            p (Resource | IRI):
                Predicate of triple.
            o (Resource | IRI | Any):
                Object of triple.
            lang (Optional[str], optional):
                Language of object. Defaults to None.
            force (bool, optional):
                Whether to force the setting of triple (eg. if there was
                one already). Defaults to False.
        """

        # Prepare predicate and object
        p, o = self.prepare_p_o(p, o, lang=lang)

        # If attribute was already set to another value
        if p in self._graph.predicates(self._identifier, unique=True):
            # If force, remove previously set value
            if force:
                self._graph.remove((self._identifier, p, None))

            else:
                # If the value is the same, do not do anything
                value = self.get_attribute(p)
                if value == o:
                    return

                # Otherwise, raise warning
                warnings.warn(
                    f"{self._identifier}: Overwriting unique attribute "
                    f"'{p}' of value '{value}', with value '{o}'."
                )

        # Set attribute o to Resource, using predicate p
        super().set(p, o)

    def add_alt_label(self, alt_label: str, lang: LangType = None) -> None:
        """Add a SKOS.altLabel to Resource.

        Args:
            alt_label (str):
                Alternative label.
            lang (Optional[str], optional):
                Language of label. Defaults to None.
        """

        alt_label = Literal(alt_label, lang=lang)

        # If altLabel to be added is already prefLabel, do nothing
        if self.get_attribute(SKOS.prefLabel) == alt_label:
            warnings.warn(
                f"{self._identifier}: SKOS.altLabel '{str(alt_label)}' is "
                "already the SKOS.prefLabel. Not adding it to altLabel list."
            )
            return

        # Add alt_label to Resource's SKOS.altLabel list
        self.add(SKOS.altLabel, alt_label)

    def set_pref_label(self, pref_label: str, lang: LangType = None) -> None:
        """Set Resource's SKOS.prefLabel.

        Args:
            pref_label (str):
                Preferred label.
            lang (Optional[str], optional):
                Language of label. Defaults to None.
        """

        # Set pref_label as Resource's SKOS.prefLabel
        pref_label = Literal(pref_label, lang=lang)
        self.set(SKOS.prefLabel, pref_label)

        # If pref_label was already added as a SKOS.altLabel
        if pref_label in self.objects(SKOS.altLabel):
            warnings.warn(
                f"{self._identifier}: SKOS.prefLabel '{str(pref_label)}' "
                "is already a SKOS.altLabel. Removing it from altLabel list."
            )

            # Remove pref_label from SKOS.altLabel list
            self.remove(SKOS.altLabel, pref_label)
