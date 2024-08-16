"""RDFS Resource constructor"""

import copy
import re
import warnings
from typing import Any, Optional, Union

from langcodes import standardize_tag
from langcodes.tag_parser import LanguageTagError
from rdflib import (
    DCTERMS,
    RDF,
    RDFS,
    SKOS,
    XSD,
    ConjunctiveGraph,
    Graph,
    Literal,
    Namespace,
)
from rdflib import URIRef as IRI
from rdflib.resource import Resource as RdflibResource
from rdflib.term import _serial_number_generator

from rdflib_plus.config import (
    DEFAULT_CHECK_TRIPLES,
    DEFAULT_LANGUAGE,
    DEFAULT_SEPARATOR,
)
from rdflib_plus.definitions import RDFS_CLASSES
from rdflib_plus.models.utils.types import (
    ConstraintsType,
    GraphType,
    IdentifierType,
    LangType,
)
from rdflib_plus.namespaces import DEFAULT_NAMESPACE, stringify_iri
from rdflib_plus.utils import legalize_for_iri

# Define specific custom types
ResourceOrIri = Union["Resource", IRI]
ObjectType = ResourceOrIri | Literal | Any
IdentifierPropertyType = ResourceOrIri | list[ResourceOrIri]


class Resource(RdflibResource):
    """RDFS Resource constructor"""

    # Resource's RDF type
    _type: ResourceOrIri = RDFS.Resource

    # Separating character in IRI between path and identifier
    _sep: str = DEFAULT_SEPARATOR

    # Resource is a priori not a RDFS Container
    _is_container: bool = False

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

    @property
    def path(self) -> list[str]:
        """Return Resource's path.

        Returns:
            list[str]: Resource '_path' attribute.
        """

        return self._path

    @property
    def identifier_property(self) -> ResourceOrIri:
        """Return Resource's identifier property.

        Returns:
            ResourceOrIri: Resource '_identifier_property' attribute.
        """

        return self._identifier_property

    @property
    def id(self) -> IdentifierType:
        """Return Resource's identifier.

        Returns:
            str | int: Resource '_id' attribute.
        """

        return self._id

    @property
    def type(self) -> ResourceOrIri:
        """Return Resource's type.

        Returns:
            ResourceOrIri: Resource's '_type' attribute.
        """

        return self._type

    @property
    def properties(self) -> set[IRI]:
        """Return Resource's allowed properties.

        Returns:
            set[IRI]: Resource's allowed properties.
        """

        return set(self._constraints.keys())

    def __str__(self) -> str:
        """Human-readable string representation of Resource"""

        return stringify_iri(self._identifier)

    def __init__(
        self,
        graph: GraphType,
        identifier: Optional[IdentifierType] = None,
        label: Optional[str] = None,
        iri: Optional[IRI] = None,
        path: Optional[list[str]] = None,
        identifier_property: Optional[ResourceOrIri] = None,
        namespace: Optional[Namespace] = None,
        local: bool = False,
        lang: LangType = DEFAULT_LANGUAGE,
        type_in_iri: bool = True,
        check_triples: bool = DEFAULT_CHECK_TRIPLES,
    ) -> None:
        """Initialize Resource.

        Args:
            graph (Graph | MultiGraph):
                Graph to search or create Resource into.
            identifier (str | int | None, optional):
                Resource's identifier. Defaults to None.
            label (str | None, optional):
                Resource's label. Defaults to None.
            iri (IRI | None, optional):
                Resource's IRI. Defaults to None.
            path (list[str] | None, optional):
                Resource's base path. Defaults to None.
            identifier_property (Resource | IRI | None, optional):
                Resource's identifier property. Defaults to None.
            namespace (Namespace | None, optional):
                Namespace to search or create Resource into. Defaults to None.
            local (bool, optional):
                Whether Resource only appears in the specified namespace.
                Defaults to False.
            lang (str | None, optional):
                Resource's language. Defaults to DEFAULT_LANGUAGE.
            type_in_iri (bool, optional):
                Whether to include Resource's type in IRI. Defaults to True.
            check_triples (bool, optional):
                Whether to check triples that are added or set.
                Defaults to DEFAULT_CHECK_TRIPLES.
        """

        # Resource is a priori not a blank node, so
        # it uses the base DCTERMS.identifier property
        bnode = False

        # Strip label
        if label is not None:
            label = label.strip()

        # If no label nor identifier is specified,
        # create Resource as blank node
        elif identifier is None:
            # Generate arbitrary identifier
            identifier = _serial_number_generator()()

            # Specify it is a blank node
            bnode = True

        # If no identifier is specified, but a label is
        if identifier is None:
            # Use label as identifier
            identifier = label

        # If identifier is an empty string
        if identifier == "":
            # Raise error
            raise ValueError(
                "Resource is trying to be initialized with empty string as "
                "identifier. If you want to create a blank node, set "
                "'identifier' to None and 'bnode' to True."
            )

        # Set Resource's attributes
        self._path = copy.deepcopy(path) if path is not None else []
        if type_in_iri:
            self._path.append(self._type.fragment)
        self._identifier_property = self._format_identifier_property(
            identifier_property, identifier
        )
        self._lang = self._format_lang(lang, identifier)
        self._check_triples = check_triples
        self._id = self._format_identifier(identifier)

        # Keep track of full graph
        full_graph = graph

        # If a namespace is specified
        if namespace is not None:
            # Format namespace
            namespace = self._format_namespace(namespace)

            # If graph supports subgraphs
            # Type: Should be rdflib_plus.MultiGraph
            if isinstance(graph, ConjunctiveGraph):
                # Get specified subgraph
                graph = graph.get_subgraph(namespace)

                # If Resource only appears in namespace
                if local:
                    full_graph = graph

            # Otherwise
            else:
                # Raise a warning
                warnings.warn(
                    f"{self}: Namespace '{namespace}' provided, but "
                    "specified graph does not support subgraphs (use "
                    "rdflib_plus.MultiGraph instead of rdflib_plus.Graph)."
                )

        # If no IRI is specified
        if iri is None:
            # Build IRI
            iri = self._build_iri(namespace, local)

        # Create Resource in appropriate graph
        super().__init__(graph, iri)

        # If Resource was never initialized before,
        # proceed in the full graph
        if not (iri, None, None) in full_graph:
            self._initialize_resource(label, bnode, full_graph)

        # If a namespace is specified
        if namespace is not None:
            # If Resource was not already linked to its source namespace
            if (iri, DCTERMS.source, IRI(namespace)) not in full_graph:
                # Make the link
                self.add(DCTERMS.source, IRI(namespace), graph=full_graph)

    def _format_lang(
        self,
        lang: Optional[str],
        identifier: IdentifierType,
    ) -> Optional[str]:
        """Set Resource's '_lang' attribute."""

        # If a language is specified
        if lang is not None:
            # Otherwise, if a lang is specified
            try:
                # Standardize lang
                lang = standardize_tag(lang)

            # If lang is not in the right format
            except LanguageTagError:
                # Raise a warning
                warnings.warn(
                    f"{stringify_iri(self._type)} '{identifier}': Language "
                    f"code '{lang}' could not be parsed according to BCP-47. "
                    "Setting language to None."
                )

        return lang

    def _format_identifier_property(
        self,
        identifier_property: Optional[ResourceOrIri],
        identifier: IdentifierType,
    ) -> ResourceOrIri:
        """Set Resource's '_identifier_property' attribute."""

        # If an identifier property is specified
        if identifier_property is not None:
            # If class's identifier property is unique
            if not isinstance(self._identifier_property, list):
                # If class's and specified identifier property are not the same
                if identifier_property != self._identifier_property:
                    # Raise an error
                    raise ValueError(
                        f"{stringify_iri(self._type)} '{identifier}': "
                        "Identifier property "
                        f"'{stringify_iri(identifier_property)}' is not "
                        "valid (it should be "
                        f"'{stringify_iri(self._identifier_property)}' for "
                        f"objects of type '{stringify_iri(self.type)}'."
                    )

                # Otherwise if they are the same,
                # raise a warning
                warnings.warn(
                    f"{stringify_iri(self._type)} '{identifier}': "
                    "Specifying identifier property "
                    f"'{stringify_iri(identifier_property)}', but it is "
                    "already the default one for objects of type "
                    f"'{stringify_iri(self.type)}'."
                )

            # Otherwise, if class has several identifier properties
            # and specified identifier property is not among them
            elif identifier_property not in self._identifier_property:
                # Stringify identifier properties for better readability
                identifier_properties = [
                    stringify_iri(property_)
                    for property_ in self._identifier_property
                ]

                # Raise an error
                raise ValueError(
                    f"{stringify_iri(self._type)} '{identifier}': Specified "
                    "identifier property is not valid "
                    f"('{stringify_iri(identifier_property)}' not in "
                    f"{identifier_properties})."
                )

        # Otherwise, if class's identifier property is a list
        elif isinstance(self._identifier_property, list):
            # Get the first one by default
            identifier_property = self._identifier_property[0]

            # Raise a warning
            warnings.warn(
                f"{stringify_iri(self._type)} '{identifier}': Identifier "
                "property was not specified, using "
                f"{stringify_iri(self._type)}'s default identifier property "
                f"('{stringify_iri(identifier_property)}')."
            )

        # Otherwise, if no identifier property is specified
        else:
            # Use Resource's one
            identifier_property = self._identifier_property

        return identifier_property

    @staticmethod
    def _format_identifier(identifier: IdentifierType) -> IdentifierType:
        """Format Resource's identifier.

        Args:
            identifier (str | int):
                Resource's identifier.

        Returns:
            str | int: Formatted Resource's identifier.
        """

        return identifier

    @staticmethod
    def _format_namespace(namespace: Namespace) -> Namespace:
        """Format Resource's namespace.

        Args:
            namespace (Namespace):
                Namespace to format.

        Returns:
            Namespace: Formatted namespace.
        """

        # If namespace does not finish by a trailing slash
        if str(namespace)[-1] != "/":
            # Append a trailing slash to it
            namespace = Namespace(f"{namespace}/")

        return namespace

    def _build_path(self, identifier: str) -> str:
        """Add Resource's identifier to IRI path.

        Args:
            identifier (str):
                Resource's identifier.

        Returns:
            str: Full Resource's IRI path.
        """

        # Build Resource's base path
        path = "/".join(self._path)

        # If class's identifier property is a list
        if isinstance(self.__class__.identifier_property, list):
            # Add Resource's identifier property to path
            # as several Resources may have the same identifier,
            # but linked with a different property
            identifier_property = (
                self._identifier_property.id
                if isinstance(self._identifier_property, Resource)
                else self._identifier_property.fragment
            )
            path += f"/{identifier_property}"

        # If a path is specified
        if path:
            # Add a slash before it
            path = "/" + path

        # Add identifier to path as a fragment
        path_and_identifier = f"{path}{self._sep}{identifier}"

        return path_and_identifier

    def _build_iri(self, namespace: Namespace, local: bool) -> IRI:
        """Build Resource's IRI from its identifier.

        Args:
            namespace (Namespace):
                Resource's namespace.
            local (bool):
                Whether Resource only appears in the specified namespace.

        Returns:
            IRI: Resource's IRI.
        """

        # Format identifier for use in IRI
        identifier = legalize_for_iri(self._id)

        # Build path
        path = self._build_path(identifier)

        # If no namespace is specified
        if namespace is None or not local:
            # Use default namespace
            namespace = DEFAULT_NAMESPACE

        # Build IRI from namespace and path
        iri = namespace[path]

        return iri

    def _initialize_resource(
        self,
        label: Optional[str],
        bnode: bool,
        graph: Graph,
    ) -> None:
        """Initialize RDFS Resource in graph.

        Args:
            label (str | None):
                Resource's label.
            bnode (bool):
                Whether Resource is a blank node.
            graph (Graph):
                Graph where to add/set triples in.
        """

        # Add Resource's type
        self.add(RDF.type, self._type, graph=graph)

        # If Resource is not a blank node
        if not bnode:
            # Set its identifier in graph
            self.set(self._identifier_property, self._id, graph=graph)

            # If a label is specified
            if label is not None:
                # If label is an empty string
                if label == "":
                    # Raise warning
                    warnings.warn(
                        f"{self}: Trying to set label to empty string. "
                        "Thus, no label set."
                    )

                # Otherwise
                else:
                    # Add it as SKOS.prefLabel
                    self.set_pref_label(label, lang=self._lang, graph=graph)

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

        # If resource is not the object of a triple,
        # and is not an IRI (nor a Literal)
        if not is_object and not isinstance(resource, IRI):
            # Raise an error
            raise TypeError(
                f"'{resource}' is trying to be used as predicate in a triple, "
                "but it is neither an IRI nor a rdflib_plus.Resource."
            )

        return resource

    def _format_p_o(
        self,
        p: ResourceOrIri,
        o: Optional[ObjectType],
        lang: LangType = DEFAULT_LANGUAGE,
        check_triple: bool = False,
    ) -> tuple[IRI, IRI | Literal]:
        """Prepare predicate and object, to be added to triplestore.

        Args:
            p (Resource | IRI):
                Predicate of triple.
            o (Resource | IRI | Literal | Any | None):
                Object of triple.
            lang (str | None, optional):
                Language of object. Defaults to DEFAULT_LANGUAGE.
            check_triple (bool, optional):
                Whether to check the added triple. Defaults to False.

        Returns:
            tuple[IRI, IRI | Literal]: Prepared predicate and object.
        """

        if check_triple:
            # If p is None
            if p is None:
                raise ValueError("Triple cannot have None as predicate.")

            # If o is None
            if o is None and p != RDF.rest:
                raise ValueError("Triple cannot have None as object.")

        # Format p for graph input
        p = self._format_resource(p, is_object=False)

        if check_triple:
            # If p is valid with Resource
            if p in self._constraints:
                # Get constraints of property p
                constraints = self._constraints[p]

            else:
                # If p is RDFS.member property
                # TODO: Use RDFS.member?
                if (
                    self._is_container
                    and isinstance(p, IRI)
                    and p.defrag() + DEFAULT_SEPARATOR == IRI(RDF)
                    and re.match(r"\_\d+", p.fragment)
                ):
                    # Get constraints of RDFS.member property
                    constraints = self._constraints[RDFS.member]

                # Otherwise, if p is not valid with Resource
                else:
                    # Raise an error
                    raise ValueError(
                        f"{self}: Property '{stringify_iri(p)}' is not valid "
                        f"with objects of type {stringify_iri(self._type)}."
                    )

            # # TODO: Unsatisfying solution, as it does not check for
            # #       parent/super-classes.
            # # If o is a Resource, predicate has a 'class' constraint
            # # and o's type is not valid
            # if (
            #     isinstance(o, Resource)
            #     and "class" in constraints
            #     and o.type not in constraints["class"]
            # ):
            #     # Stringify IRIs
            #     constraints = [
            #         stringify_iri(type_) for type_ in constraints["datatype"]
            #     ]

            #     # Raise an error
            #     raise TypeError(
            #         f"{self}: Object '{stringify_iri(o)}' does not have "
            #         f"valid type ({stringify_iri(o.type)} not in "
            #         f"{constraints}) with predicate '{stringify_iri(p)}'."
            #     )

        # Format o for graph input
        o = self._format_resource(o, is_object=True)

        # Otherwise, if o is neither a plain IRI nor a Literal
        if not isinstance(o, (IRI, Literal)) and o is not None:
            # If o is an empty string, raise warning
            if o == "":
                warnings.warn(
                    f"{self}: Empty string is used as object in triple with "
                    f"predicate '{stringify_iri(p)}'."
                )

            # If no language is specified
            if lang is None:
                # Use Resource's language
                lang = self._lang

            # If o is a string, and no language is specified

            if isinstance(o, str) and lang is None:
                # Specify datatype
                datatype = XSD.string
            # Otherwise
            else:
                # Do not specify datatype (rdflib.Literal() will guess it)
                datatype = None

            # Format o into a Literal
            o = Literal(o, datatype=datatype, lang=lang)

        # If o is a Literal, predicate has a "datatype" constraint
        if (
            check_triple
            and isinstance(o, Literal)
            and "datatype" in constraints
        ):
            # Specify o's datatype in case a language was specified
            # (rdflib.Literal has no datatype if o is a string)
            datatype = o.datatype if o.datatype is not None else XSD.string

            # If o's datatype is not valid
            if datatype not in constraints["datatype"]:
                # Stringify IRIs
                constraints = [
                    stringify_iri(type_) for type_ in constraints["datatype"]
                ]

                # Check that it has a valid datatype for
                # the property in question
                raise TypeError(
                    f"{self}: Object '{o}' does not have valid datatype "
                    f"('{stringify_iri(datatype)}' not in {constraints}) with "
                    f"predicate '{stringify_iri(p)}'."
                )

        return p, o

    def add(
        self,
        p: ResourceOrIri,
        o: ObjectType,
        lang: LangType = DEFAULT_LANGUAGE,
        graph: Optional[Graph] = None,
        check_triple: Optional[bool] = None,
    ) -> None:
        """Add triple to self._graph.

        Args:
            p (Resource | IRI):
                Predicate of triple.
            o (Resource | IRI | Literal | Any):
                Object of triple.
            lang (str | None, optional):
                Language of object. Defaults to DEFAULT_LANGUAGE.
            graph (Graph | None, optional):
                Graph where to add triple in. Defaults to None.
            check_triple (bool | None, optional):
                Whether to check the added triple. Defaults to None.
        """

        # If check_triple is not specified, use Class's value
        if check_triple is None:
            check_triple = self._check_triples

        # Prepare predicate and object
        p, o = self._format_p_o(p, o, lang=lang, check_triple=check_triple)

        # If no graph is specified
        if graph is None:
            # Use self._graph
            graph = self._graph

        # If there is a 'maxCount' constraint of 1
        # and the value is trying to be added
        if check_triple and self._constraints[p].get("maxCount") == 1:
            # Raise a warning
            warnings.warn(
                f"{self}: Adding an object with the predicate "
                f"'{stringify_iri(p)}' (with the add() method), "
                "instead of setting it (with set())."
            )

        # Add object o to Resource, using predicate p
        graph.add((self._identifier, p, o))

    def set(
        self,
        p: ResourceOrIri,
        o: ObjectType,
        lang: LangType = DEFAULT_LANGUAGE,
        replace: bool = False,
        graph: Optional[Graph] = None,
        check_triple: Optional[bool] = None,
    ) -> None:
        """Set triple in self._graph.

        Args:
            p (Resource | IRI):
                Predicate of triple.
            o (Resource | IRI | Any):
                Object of triple.
            lang (str | None, optional):
                Language of object. Defaults to DEFAULT_LANGUAGE.
            replace (bool, optional):
                Whether triple should replace an existing one.
                Defaults to False.
            graph (Graph | None, optional):
                Graph where to set triple in. Defaults to None.
            check_triple (bool | None, optional):
                Whether to check the added triple. Defaults to None.
        """

        # If check_triple is not specified, use Class's value
        if check_triple is None:
            check_triple = self._check_triples

        # Prepare predicate and object
        p, o = self._format_p_o(p, o, lang=lang, check_triple=check_triple)

        # If no graph is specified
        if graph is None:
            # Use self._graph
            graph = self._graph

        # If attribute was already set to another value
        if (
            not replace
            and check_triple
            and p in graph.predicates(self._identifier, unique=True)
        ):
            # If the value is the same, do not do anything
            value = self.get_value(p)
            if value == o:
                return

            # Otherwise, raise warning
            warnings.warn(
                f"{self}: Overwriting value of (unique) attribute with "
                f"predicate '{stringify_iri(p)}', from '{value}' to '{o}' "
                f"in graph '{graph.identifier}'."
            )

        # Set object o to Resource, using predicate p
        graph.set((self._identifier, p, o))

    def get_value(
        self,
        p: ResourceOrIri,
        graph: Optional[Graph] = None,
        check_triple: Optional[bool] = None,
    ) -> IRI | Literal:
        """Get value of (unique) attribute.

        Args:
            p (Resource | IRI):
                Predicate that links to target attribute.
            graph (Graph | None, optional):
                Graph where to add triple in. Defaults to None.
            check_triple (bool | None, optional):
                Whether to check the added triple. Defaults to None.

        Returns:
            IRI | Literal: Target attribute value.
        """

        # If check_triple is not specified, use Class's value
        if check_triple is None:
            check_triple = self._check_triples

        # Format p for graph input
        p = self._format_resource(p, is_object=False)

        # If no graph is specified
        if graph is None:
            # Use self._graph
            graph = self._graph

        # Whether to raise an error if attribute value is not unique
        # If not, any value will be returned if multiple values
        any_ = not check_triple

        # Fetch attribute value
        value = graph.value(self._identifier, p, any=any_)

        return value

    def remove(
        self,
        p: ResourceOrIri,
        o: Optional[ObjectType] = None,
        lang: LangType = DEFAULT_LANGUAGE,
        graph: Optional[Graph] = None,
        check_triple: Optional[bool] = None,
    ) -> None:
        """Replace an attribute with another value.

        Args:
            p (Resource | IRI):
                Predicate of triple.
            o (Resource | IRI | Any):
                Object of triple.
            lang (str | None, optional):
                Language of object. Defaults to DEFAULT_LANGUAGE.
            graph (Graph | None, optional):
                Graph where to remove triple from. Defaults to None.
            check_triple (bool | None, optional):
                Whether to check the added triple. Defaults to None.
        """

        # If check_triple is not specified, use Class's value
        if check_triple is None:
            check_triple = self._check_triples

        # Prepare predicate and object
        p, o = self._format_p_o(p, o, lang=lang, check_triple=check_triple)

        # If no graph is specified
        if graph is None:
            # Use self._graph
            graph = self._graph

        # If no triple matches
        if check_triple and (self._identifier, p, o) not in graph:
            # Raise a warning
            if o is None:
                message = (
                    f"{self}: Failed to remove triples with predicate '{p}' "
                    f"from graph '{graph.identifier}' as none exist."
                )
            else:
                message = (
                    f"{self}: Failed to remove triples with predicate '{p}' "
                    f"from graph '{graph.identifier}' and object '{o}' as it "
                    "does not exist."
                )
            warnings.warn(message)

        # Remove object o from Resource, using predicate p
        graph.remove((self._identifier, p, o))

    def replace(
        self,
        p: ResourceOrIri,
        o: ObjectType,
        lang: LangType = DEFAULT_LANGUAGE,
        graph: Optional[Graph] = None,
        check_triple: Optional[bool] = None,
    ) -> None:
        """Replace an attribute with another value.

        Args:
            p (Resource | IRI):
                Predicate of triple.
            o (Resource | IRI | Any):
                Object of triple.
            lang (str | None, optional):
                Language of object. Defaults to DEFAULT_LANGUAGE.
            graph (Graph | None, optional):
                Graph where to replace triple in. Defaults to None.
            check_triple (bool | None, optional):
                Whether to check the added triple. Defaults to None.
        """

        # Remove old value of attribute
        self.remove(p, graph=graph)

        # Set its new value
        self.set(
            p,
            o,
            lang=lang,
            replace=True,
            graph=graph,
            check_triple=check_triple,
        )

    def add_alt_label(
        self,
        alt_label: str,
        lang: LangType = DEFAULT_LANGUAGE,
        graph: Optional[Graph] = None,
        check_triple: Optional[bool] = None,
    ) -> None:
        """Add a SKOS.altLabel to Resource.

        Args:
            alt_label (str):
                Alternative label.
            lang (str | None, optional):
                Language of label. Defaults to DEFAULT_LANGUAGE.
            graph (Graph | None, optional):
                Graph where to add altLabel in. Defaults to None.
            check_triple (bool | None, optional):
                Whether to check the added triple. Defaults to None.
        """

        # If check_triple is not specified, use Class's value
        if check_triple is None:
            check_triple = self._check_triples

        if check_triple:
            # If altLabel to be added is already prefLabel, do nothing
            if self.get_value(SKOS.prefLabel) == alt_label:
                warnings.warn(
                    f"{self}: SKOS.altLabel '{str(alt_label)}' is already the "
                    f"SKOS.prefLabel in graph '{graph.identifier}'. "
                    "Not adding it to the altLabel list."
                )
                return

        # Add alt_label to Resource's SKOS.altLabel list
        self.add(
            SKOS.altLabel,
            alt_label,
            lang=lang,
            graph=graph,
            check_triple=check_triple,
        )

    def set_pref_label(
        self,
        pref_label: str,
        lang: LangType = DEFAULT_LANGUAGE,
        graph: Optional[Graph] = None,
        check_triple: Optional[bool] = None,
    ) -> None:
        """Set Resource's SKOS.prefLabel.

        Args:
            pref_label (str):
                Preferred label.
            lang (str | None, optional):
                Language of label. Defaults to DEFAULT_LANGUAGE.
            graph (Graph | None, optional):
                Graph where to set prefLabel in. Defaults to None.
            check_triple (bool | None, optional):
                Whether to check the added triple. Defaults to None.
        """

        # If check_triple is not specified, use Class's value
        if check_triple is None:
            check_triple = self._check_triples

        # Set pref_label as Resource's SKOS.prefLabel
        self.set(
            SKOS.prefLabel,
            pref_label,
            lang=lang,
            graph=graph,
            check_triple=check_triple,
        )

        # If pref_label was already added as a SKOS.altLabel
        if check_triple and pref_label in self.objects(SKOS.altLabel):
            warnings.warn(
                f"{self}: SKOS.prefLabel '{str(pref_label)}' is already a "
                f"SKOS.altLabel in graph '{graph.identifier}'. "
                "Removing it from the altLabel list."
            )

            # Remove pref_label from SKOS.altLabel list
            self.remove(SKOS.altLabel, o=pref_label, graph=graph)
