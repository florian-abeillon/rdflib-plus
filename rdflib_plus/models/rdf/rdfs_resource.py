"""RDFS Resource constructor"""

import warnings
from typing import Optional

from langcodes import standardize_tag
from langcodes.tag_parser import LanguageTagError
from rdflib import DCTERMS, RDF, RDFS, SKOS
from rdflib import ConjunctiveGraph as MultiGraph
from rdflib import Literal, Namespace
from rdflib import URIRef as IRI
from rdflib.resource import Resource as RdflibResource
from rdflib.term import _serial_number_generator

from rdflib_plus.config import DEFAULT_CHECK_TRIPLES, DEFAULT_LANGUAGE
from rdflib_plus.definitions import RDFS_CLASSES
from rdflib_plus.namespaces import DEFAULT_NAMESPACE
from rdflib_plus.utils import (
    ConstraintsType,
    GraphType,
    IdentifierPropertyType,
    IdentifierType,
    LangType,
    ObjectType,
    ResourceOrIri,
    legalize_for_iri,
)


class Resource(RdflibResource):
    """RDFS Resource constructor"""

    # Resource's RDF type
    _type: ResourceOrIri = RDFS.Resource

    # Property that links Resource to its identifier
    _identifier_property: IdentifierPropertyType = RDFS_CLASSES[_type][
        "identifier_property"
    ]

    # Resource's property constraints
    _constraints: ConstraintsType = RDFS_CLASSES[_type]["constraints"]

    @classmethod
    def update_constraints(
        cls, constraints: ConstraintsType
    ) -> ConstraintsType:
        """Combine Resource's child class's constraints with Resource's.
           Not to be used within the 'Resource' constructor.

        Args:
            constraints (dict[IRI, dict[str, Any]]):
                Constraints specific to child class.

        Returns:
            PropertyConstraintsType: Resource constraints, updated with
                                     child class's specific constraints.
        """
        return {**cls._constraints, **constraints}

    @property
    def iri(self) -> IRI:
        """Return Resource's IRI.

        Returns:
            IRI: Resource '_identifier' attribute.
        """

        return self._identifier

    def __str__(self) -> str:
        """Human-readable string representation of Resource"""

        return str(self.iri)

    def __init__(
        self,
        graph: GraphType,
        identifier: Optional[IdentifierType] = None,
        label: Optional[str] = None,
        iri: Optional[IRI] = None,
        path: Optional[list[str]] = None,
        namespace: Optional[Namespace] = None,
        lang: LangType = DEFAULT_LANGUAGE,
        check_triples: bool = DEFAULT_CHECK_TRIPLES,
    ) -> None:
        """Initialize Resource.

        Args:
            graph (Graph | MultiGraph):
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
                Resource's language. Defaults to DEFAULT_LANGUAGE.
            check_triples (bool, optional):
                Whether to check triples that are added or set using Resource.
                Defaults to DEFAULT_CHECK_TRIPLES.
        """

        # Format and set language
        self.lang = None
        if lang is not None:
            try:
                self.lang = standardize_tag(lang)
            except LanguageTagError:
                warnings.warn(
                    f"Language code '{lang}' could not be parsed "
                    "according to BCP 47. Setting Resource "
                    f"""'{
                        iri if iri is not None
                        else identifier if identifier is not None
                        else label
                    }' as None."""
                )

        # Set path and check_triples
        self.path = path if path is not None else [self._type.fragment]
        self.check_triples = check_triples

        # If an IRI is directly specified
        if iri is not None:
            # Just create a Resource using IRI
            super().__init__(graph, iri)
            return

        # Strip label
        if label is not None:
            label = label.strip()

        # If no iri nor label nor identifier is specified,
        # create Resource as blank node
        elif identifier is None:
            identifier = _serial_number_generator()()

        # If no identifier is specified
        if identifier is None:
            # Use label as identifier
            identifier = label

            # Get appropriate label ID given lang
            if isinstance(self._identifier_property, dict):
                self._identifier_property = self._identifier_property[
                    self.lang
                ]

        # Format identifier
        self.id_ = self._format_identifier(identifier)

        # Build IRI
        iri = self._build_iri(self.id_)

        # If Resource was never initialized before,
        # Add type and identifier to the specified graph
        if not (iri, None, None) in graph:
            self._initialize_resource(graph, iri, label)

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

            # Get specified subgraph
            if isinstance(graph, MultiGraph):
                graph = graph.get_context(namespace)
            else:
                # If graph does not support subgraphs,
                # raise a warning
                warnings.warn(
                    f"{iri}: Namespace '{namespace}' provided, but specified "
                    "graph does not support subgraphs "
                    "(use rdflib.ConjunctiveGraph instead of rdflib.Graph)."
                )

        # Create Resource in appropriate graph
        super().__init__(graph, iri)

    @staticmethod
    def _format_identifier(identifier: IdentifierType) -> str:
        """Format Resource's identifier.

        Args:
            identifier (str | int):
                Resource's identifier.

        Returns:
            str: Formatted Resource's identifier.
        """

        return str(identifier)

    def _build_iri(
        self,
        identifier: IdentifierType,
        namespace: Namespace = DEFAULT_NAMESPACE,
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

        # Format identifier for use in IRI
        identifier = legalize_for_iri(identifier)

        # Build path, and then its IRI from it
        path = self._build_path(identifier)
        iri = namespace[path]

        return iri

    def _build_path(self, identifier: str) -> str:
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
        #       Prepending "self._identifier_property.fragment"
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

    def _initialize_resource(
        self, graph: GraphType, iri: IRI, label: Optional[str]
    ) -> None:
        """Create RDFS Resource

        Args:
            graph (Graph | MultiGraph):
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
        resource.set(self._identifier_property, self.id_)

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

    @staticmethod
    def _format_resource(
        resource: ObjectType, is_object: bool = False
    ) -> IRI | Literal:
        """Format resource for graph input.

        Args:
            resource (Resource | IRI | Literal | Any):
                Resource to format.
            is_object (bool, optional):
                Whether resource is object of a triple. Defaults to False

        Returns:
            IRI | Literal: IRI of resource, or value of attribute.
        """

        # If resource is a Resource, return its IRI
        if isinstance(resource, Resource):
            return resource.iri

        # If resource is not the object of a triple
        if not is_object:
            # Check that it is indeed an IRI (and not a Literal)
            assert isinstance(
                resource, IRI
            ), f"Resource {resource} is not an IRI nor a rdflib_plus.Resource."

        return resource

    def _format_p_o(
        self,
        p: ResourceOrIri,
        o: ObjectType,
        lang: LangType = DEFAULT_LANGUAGE,
        check_triple: bool = False,
    ) -> tuple[IRI, IRI | Literal]:
        """Prepare predicate and object, to be added to triplestore.

        Args:
            p (Resource | IRI):
                Predicate of triple.
            o (Resource | IRI | Literal | Any):
                Object of triple.
            lang (Optional[str], optional):
                Language of object. Defaults to DEFAULT_LANGUAGE.
            check_triple (bool, optional):
                Whether to check the added triple. Defaults to False.

        Returns:
            tuple[IRI, IRI | Literal]: Prepared predicate and object.
        """

        if check_triple:
            # Check that p and o are not None
            assert p is not None, "Trying to add triple with null predicate."
            assert o is not None, "Trying to add triple with null object."

        # Format p for graph input
        p = self._format_resource(p, is_object=False)

        if check_triple:
            # Make sure p is valid with Resource
            assert (
                p in self._constraints
            ), f"{self.iri}: Property '{p}' is not valid with this class."

            # Get constraints of property p
            constraints = self._constraints[p]

        # # If o is a Resource, and has a 'class' constraint
        # if check_triple and isinstance(o, Resource) and "class" in constraints:
        #     # TODO: Unsatisfying solution, as it uses the '_type'
        #     #       protected attribute, and does not check for
        #     #       parent/super-classes.
        #     # Check that o is of valid type
        #     assert o._type == constraints["class"]

        # Format o for graph input
        o = self._format_resource(o, is_object=True)

        # Otherwise, if o is neither a plain IRI nor a Literal
        if not isinstance(o, (IRI, Literal)):
            # If o is an empty string, raise warning
            if o == "":
                warnings.warn(
                    f"{self.iri}: Empty string is trying to be set or "
                    f"added using predicate '{p}'"
                )

            # Format o into a Literal
            if lang is None:
                lang = self.lang
            o = Literal(o, lang=lang)

        if check_triple:
            assert isinstance(o, Literal) and isinstance(
                o.datatype, constraints["datatype"]
            ), (
                f"{self.iri}: Object '{o}' does not have valid datatype "
                "with Property '{p}'."
            )

        return p, o

    def add(
        self,
        p: ResourceOrIri,
        o: ObjectType,
        lang: LangType = DEFAULT_LANGUAGE,
        check_triple: Optional[bool] = None,
    ) -> None:
        """Add triple to self._graph.

        Args:
            p (Resource | IRI):
                Predicate of triple.
            o (Resource | IRI | Any):
                Object of triple.
            lang (Optional[str], optional):
                Language of object. Defaults to DEFAULT_LANGUAGE.
            check_triple (Optional[bool], optional):
                Whether to check the added triple. Defaults to None.
        """

        # If check_triple is not specified, use Class's value
        if check_triple is None:
            check_triple = self.check_triples

        # Prepare predicate and object
        p, o = self._format_p_o(p, o, lang=lang, check_triple=check_triple)

        if check_triple:
            # If there is a 'maxCount' constraint of 1
            # and the value is trying to be added
            if self._constraints[p].get("maxCount") == 1:
                # Raise a warning
                warnings.warn(
                    f"{self.iri}: Adding value of Property '{p}' with "
                    "the add() method, instead of setting it with set()."
                )

        # Add object o to Resource, using predicate p
        super().add(p, o)

    def set(
        self,
        p: ResourceOrIri,
        o: ObjectType,
        lang: LangType = DEFAULT_LANGUAGE,
        check_triple: Optional[bool] = None,
    ) -> None:
        """Set triple in self._graph.

        Args:
            p (Resource | IRI):
                Predicate of triple.
            o (Resource | IRI | Any):
                Object of triple.
            lang (Optional[str], optional):
                Language of object. Defaults to DEFAULT_LANGUAGE.
            check_triple (Optional[bool], optional):
                Whether to check the added triple. Defaults to None.
        """

        # If check_triple is not specified, use Class's value
        if check_triple is None:
            check_triple = self.check_triples

        # Prepare predicate and object
        p, o = self._format_p_o(p, o, lang=lang, check_triple=check_triple)

        # If attribute was already set to another value
        if check_triple and p in self._graph.predicates(
            self._identifier, unique=True
        ):
            # If the value is the same, do not do anything
            value = self.get_attribute(p)
            if value == o:
                return

            # Otherwise, raise warning
            warnings.warn(
                f"{self.iri}: Overwriting unique attribute "
                f"'{p}' of value '{value}', with value '{o}'."
            )

        # Set attribute o to Resource, using predicate p
        super().set(p, o)

    def replace(
        self,
        p: ResourceOrIri,
        o: ObjectType,
        lang: LangType = DEFAULT_LANGUAGE,
        check_triple: Optional[bool] = None,
    ) -> None:
        """Replace an attribute with another value.

        Args:
            p (Resource | IRI):
                Predicate of triple.
            o (Resource | IRI | Any):
                Object of triple.
            lang (Optional[str], optional):
                Language of object. Defaults to DEFAULT_LANGUAGE.
            check_triple (Optional[bool], optional):
                Whether to check the added triple. Defaults to None.
        """

        # Remove old value of attribute
        self.remove(p)

        # Set its new value
        self.set(p, o, lang=lang, check_triple=check_triple)

    def add_or_set(
        self,
        p: ResourceOrIri,
        o: ObjectType,
        lang: LangType = DEFAULT_LANGUAGE,
        check_triple: Optional[bool] = None,
    ) -> None:
        """Add or set triple depending on p having a 'unique' constraint.

        Args:
            p (Resource | IRI):
                Predicate of triple.
            o (Resource | IRI | Any):
                Object of triple.
            lang (Optional[str], optional):
                Language of object. Defaults to DEFAULT_LANGUAGE.
            check_triple (Optional[bool], optional):
                Whether to check the added triple. Defaults to None.
        """

        constraints = self._constraints.get(p, {})
        if (
            constraints.get("minCount") == 1
            and constraints.get("maxCount") == 1
        ):
            # ) or constraints.get("unique", False):
            self.set(p, o, lang=lang, check_triple=check_triple)
        else:
            self.add(p, o, lang=lang, check_triple=check_triple)

    def add_alt_label(
        self,
        alt_label: str,
        lang: LangType = DEFAULT_LANGUAGE,
        check_triple: Optional[bool] = None,
    ) -> None:
        """Add a SKOS.altLabel to Resource.

        Args:
            alt_label (str):
                Alternative label.
            lang (Optional[str], optional):
                Language of label. Defaults to DEFAULT_LANGUAGE.
            check_triple (Optional[bool], optional):
                Whether to check the added triple. Defaults to None.
        """

        # If check_triple is not specified, use Class's value
        if check_triple is None:
            check_triple = self.check_triples

        if check_triple:
            # If altLabel to be added is already prefLabel, do nothing
            if self.get_attribute(SKOS.prefLabel) == alt_label:
                warnings.warn(
                    f"{self.iri}: SKOS.altLabel '{str(alt_label)}' is "
                    "already the SKOS.prefLabel. "
                    "Not adding it to altLabel list."
                )
                return

        # Add alt_label to Resource's SKOS.altLabel list
        self.add(
            SKOS.altLabel, alt_label, lang=lang, check_triple=check_triple
        )

    def set_pref_label(
        self,
        pref_label: str,
        lang: LangType = DEFAULT_LANGUAGE,
        check_triple: Optional[bool] = None,
    ) -> None:
        """Set Resource's SKOS.prefLabel.

        Args:
            pref_label (str):
                Preferred label.
            lang (Optional[str], optional):
                Language of label. Defaults to DEFAULT_LANGUAGE.
            check_triple (Optional[bool], optional):
                Whether to check the added triple. Defaults to None.
        """

        # If check_triple is not specified, use Class's value
        if check_triple is None:
            check_triple = self.check_triples

        # Set pref_label as Resource's SKOS.prefLabel
        self.set(
            SKOS.prefLabel, pref_label, lang=lang, check_triple=check_triple
        )

        if check_triple:
            # If pref_label was already added as a SKOS.altLabel
            if pref_label in self.objects(SKOS.altLabel):
                warnings.warn(
                    f"{self.iri}: SKOS.prefLabel '{str(pref_label)}' "
                    "is already a SKOS.altLabel. "
                    "Removing it from altLabel list."
                )

                # Remove pref_label from SKOS.altLabel list
                self.remove(SKOS.altLabel, o=pref_label)
