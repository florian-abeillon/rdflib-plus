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
from rdflib_plus.models.utils.decorators import (
    default_check_triple,
    default_graph,
)
from rdflib_plus.models.utils.types import (
    ConstraintsType,
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

    # TODO: Find a better way to do it?
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
        return {**constraints, **cls._constraints}

    @property
    def id(self) -> IdentifierType:
        """Return Resource's identifier.

        Returns:
            str | int: Resource '_id' attribute.
        """
        return self._id

    @property
    def identifier_property(self) -> ResourceOrIri:
        """Return Resource's identifier property.

        Returns:
            ResourceOrIri: Resource '_identifier_property' attribute.
        """
        return self._identifier_property

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
    def properties(self) -> set[IRI]:
        """Return Resource's allowed properties.

        Returns:
            set[IRI]: Resource's allowed properties.
        """
        return set(self._constraints.keys())

    @property
    def type(self) -> ResourceOrIri:
        """Return Resource's type.

        Returns:
            ResourceOrIri: Resource's '_type' attribute.
        """
        return self._type

    def __init__(
        self,
        graph: Graph,
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
            graph (Graph):
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
        self._id = self._format_identifier(identifier)
        self._lang = self._format_lang(lang)
        self._check_triples = check_triples

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
                    f"{stringify_iri(self._type)} '{identifier}': Namespace "
                    f"'{namespace}' provided, but specified graph does not "
                    "support subgraphs (use rdflib_plus.MultiGraph instead of "
                    "rdflib_plus.Graph)."
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

    def __repr__(self) -> IRI:
        """Unambiguous representation of Resource"""
        return self._identifier

    def __str__(self) -> str:
        """Human-readable string representation of Resource"""
        return stringify_iri(self._identifier)
        # TODO: Is this necessary?
        # type_ = self.__class__.__name__
        # return f"{type_}(iri={stringify_iri(self._identifier)})"

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

    def _check_p_o(
        self, p: ResourceOrIri, o: ObjectType
    ) -> tuple[IRI, IRI | Literal]:
        """Check that predicate and object are correct.

        Args:
            p (IRI):
                Predicate to be checked.
            o (IRI | Literal):
                Object to be checked.
        """

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

        # If o is a Literal, and predicate has a "datatype" constraint
        if isinstance(o, Literal) and "datatype" in constraints:
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

    def _format_lang(self, lang: Optional[str]) -> Optional[str]:
        """Set Resource's '_lang' attribute."""

        # If a language is specified
        if lang is not None:
            # Otherwise, if a lang is specified
            try:
                # TODO: Necessary? Not already featured in rdflib?
                # Standardize lang
                lang = standardize_tag(lang)

            # If lang is not in the right format
            except LanguageTagError:
                # Raise a warning
                warnings.warn(
                    f"{stringify_iri(self._type)} '{self._id}': Language "
                    f"code '{lang}' could not be parsed according to BCP-47. "
                    "Setting language to None."
                )

        return lang

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
        resource: ObjectType, check_triple: bool = DEFAULT_CHECK_TRIPLES
    ) -> IRI | Literal:
        """Format resource for graph input, to be added to triplestore.

        Args:
            resource (Resource | IRI | Literal | Any):
                Resource to format.
            is_object (bool, optional):
                Whether resource is object of a triple. Defaults to False
            check_triple (bool, optional):
                Whether to check the added triple.
                Defaults to DEFAULT_CHECK_TRIPLES.

        Returns:
            IRI | Literal: IRI of resource, or value of attribute.
        """

        # If resource is None, raise error
        if check_triple and resource is None:
            raise ValueError("Triples cannot contain None.")

        # If resource is a Resource, return its IRI
        if isinstance(resource, Resource):
            return resource.iri

        return resource

    def _format_predicate(
        self,
        p: Optional[ResourceOrIri],
        check_triple: bool = DEFAULT_CHECK_TRIPLES,
    ) -> IRI:
        """Prepare predicate, to be added to triplestore.

        Args:
            p (Resource | IRI | None):
                Predicate to be added to triplestore.
            check_triple (bool, optional):
                Whether to check the added triple.
                Defaults to DEFAULT_CHECK_TRIPLES.

        Returns:
            IRI: Prepared predicate.
        """

        if check_triple:
            # TODO: Check that predicate is indeed a Property
            # if not is_object and not (
            #     resource._type == RDF.Property or "Property" in resource.path
            # ):
            #     warnings.warn()
            pass

        p = self._format_resource(p, check_triple=check_triple)

        # If predicate is not an IRI, raise error
        if check_triple and not isinstance(p, IRI):
            raise TypeError(
                f"'{p}' is trying to be used in a triple, "
                "but it is neither an IRI nor a rdflib_plus.Resource."
            )

        return p

    def _format_object(
        self,
        o: Optional[ObjectType],
        lang: LangType = DEFAULT_LANGUAGE,
        check_triple: bool = DEFAULT_CHECK_TRIPLES,
    ) -> IRI | Literal:
        """Prepare object, to be added to triplestore.

        Args:
            o (Resource | IRI | Literal | Any | None):
                Object to be added to triplestore.
            lang (str | None, optional):
                Language of object. Defaults to DEFAULT_LANGUAGE.
            check_triple (bool, optional):
                Whether to check the added triple.
                Defaults to DEFAULT_CHECK_TRIPLES.

        Returns:
            IRI | Literal: Prepared object.
        """

        # Format o for graph input
        o = self._format_resource(o, check_triple=check_triple)

        # If a non-IRI object is specified
        if o is not None and not isinstance(o, IRI):

            # If o is an empty string, raise warning
            if o == "":
                warnings.warn(
                    f"{self}: Empty string is used as object in triple."
                )

            # If a language is specified, force o to be a string,
            # and specify language
            kwargs = {}
            if lang is not None:
                o = str(o)
                kwargs["lang"] = lang

            # Otherwise, if o is a string but not a Literal already
            elif isinstance(o, str) and not isinstance(o, Literal):

                # Add appropriate kwarg, given Resource's _lang attribute
                if self._lang is not None:
                    kwargs["lang"] = self._lang
                else:
                    kwargs["datatype"] = XSD.string

            # Turn o into Literal
            o = Literal(o, **kwargs)

        return o

    @default_graph
    @default_check_triple
    def add(
        self,
        p: ResourceOrIri,
        o: ObjectType,
        lang: LangType = DEFAULT_LANGUAGE,
        graph: Optional[Graph] = None,
        check_triple: Optional[bool] = None,
    ) -> None:
        """Add triple to graph.

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

        # Prepare predicate and object
        p = self._format_predicate(p, check_triple=check_triple)
        o = self._format_object(o, lang=lang, check_triple=check_triple)

        # If necessary, check that they are correct
        if check_triple:
            self._check_p_o(p, o)

            # If there is a 'maxCount' constraint of 1 and the value is trying
            # to be added, raise a warning
            if self._constraints[p].get("maxCount") == 1:
                warnings.warn(
                    f"{self}: Adding an object with the predicate "
                    f"'{stringify_iri(p)}' (with the add() method), "
                    "instead of setting it (with set())."
                )

        # Add object o to Resource, using predicate p
        graph.add((self._identifier, p, o))

    @default_graph
    @default_check_triple
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

        # If altLabel to be added is already prefLabel, do nothing
        if check_triple and self.get_value(SKOS.prefLabel) == alt_label:
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

    @default_graph
    @default_check_triple
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

        # Whether to raise an error if attribute value is not unique
        # If not, any value will be returned if multiple values
        any_ = not check_triple

        # Fetch attribute value
        p = self._format_predicate(p, check_triple=False)
        value = graph.value(self._identifier, p, any=any_)

        return value

    @default_graph
    def objects(
        self,
        predicate: Optional[ResourceOrIri] = None,
        graph: Optional[Graph] = None,
    ) -> list[IRI | Literal]:
        """Get objects of triples with Resource as subject.

        Args:
            predicate (Resource | IRI | None, optional):
                Predicate that links to Resource. Defaults to None.
            graph (Graph | None, optional):
                Graph where to search triples in. Defaults to None.

        Returns:
            list[IRI | Literal]:
                List of objects of triples from graph, with Resource
                as subject and predicate as predicate (if specified).
        """
        predicate = self._format_predicate(predicate, check_triple=False)
        return graph.objects(self._identifier, predicate)

    @default_graph
    def predicates(
        self,
        o: Optional[ObjectType] = None,
        graph: Optional[Graph] = None,
    ) -> list[IRI]:
        """Get predicates of triples with Resource as subject.

        Args:
            o (Resource | IRI | Any | None, optional):
                Object that is linked to Resource. Defaults to None.
            graph (Graph | None, optional):
                Graph where to search triples in. Defaults to None.

        Returns:
            list[IRI]:
                List of predicates of triples from graph, with Resource
                as subject and o as object (if specified).
        """
        o = self._format_object(o, check_triple=False)
        return graph.predicates(self._identifier, o)

    @default_graph
    def predicate_objects(
        self, graph: Optional[Graph] = None
    ) -> list[tuple[IRI, IRI | Literal]]:
        """Get predicates and objects of triples with Resource as subject.

        Args:
            graph (Graph | None, optional):
                Graph where to search triples in. Defaults to None.

        Returns:
            list[tuple[IRI, IRI | Literal]]:
                List of triples, with Resource as object.
        """
        return graph.predicate_objects(self._identifier)

    # TODO: erase() to remove the node whatsoever?

    @default_graph
    @default_check_triple
    def remove(
        self,
        p: ResourceOrIri,
        o: Optional[ObjectType] = None,
        lang: LangType = DEFAULT_LANGUAGE,
        graph: Optional[Graph] = None,
        check_triple: Optional[bool] = None,
    ) -> None:
        """Delete the value of an attribute in graph.

        Args:
            p (Resource | IRI):
                Predicate of triple.
            o (Resource | IRI | Any | None, optional):
                Object of triple. Defaults to None.
            lang (str | None, optional):
                Language of object. Defaults to DEFAULT_LANGUAGE.
            graph (Graph | None, optional):
                Graph where to remove triple from. Defaults to None.
            check_triple (bool | None, optional):
                Whether to check the added triple. Defaults to None.
        """

        # Prepare predicate and object
        p = self._format_predicate(p, check_triple=False)
        o = self._format_object(o, lang=lang, check_triple=False)

        # If no triple matches, raise a warning
        if check_triple and (self._identifier, p, o) not in graph:
            if o is None:
                warnings.warn(
                    f"{self}: Failed to remove triples with predicate "
                    f"'{p}' from graph '{graph.identifier}' as none exist."
                )
            else:
                warnings.warn(
                    f"{self}: Failed to remove triples with predicate "
                    f"'{p}' from graph '{graph.identifier}' and object "
                    f"'{o}' as it does not exist."
                )

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
        self.set(
            p,
            o,
            lang=lang,
            replace=True,
            graph=graph,
            check_triple=check_triple,
        )

    @default_graph
    @default_check_triple
    def set(
        self,
        p: ResourceOrIri,
        o: ObjectType,
        lang: LangType = DEFAULT_LANGUAGE,
        replace: bool = False,
        graph: Optional[Graph] = None,
        check_triple: Optional[bool] = None,
    ) -> None:
        """Set triple in graph.

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

        # Prepare predicate and object
        p = self._format_predicate(p, check_triple=check_triple)
        o = self._format_object(o, lang=lang, check_triple=check_triple)

        # If necessary, check that they are correct
        if check_triple:
            self._check_p_o(p, o)

            # If attribute was already set to another value
            if not replace and p in graph.predicates(
                self._identifier, unique=True
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

    @default_graph
    @default_check_triple
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

    @default_graph
    def subjects(
        self,
        predicate: Optional[ResourceOrIri] = None,
        graph: Optional[Graph] = None,
    ) -> list[IRI]:
        """Get subjects of triples with Resource as object.

        Args:
            predicate (Resource | IRI | None, optional):
                Predicate that links to Resource. Defaults to None.
            graph (Graph | None, optional):
                Graph where to search triples in. Defaults to None.

        Returns:
            list[IRI]:
                List of subjects of triples from graph, with Resource
                as object and predicate as predicate (if specified).
        """
        predicate = self._format_predicate(predicate, check_triple=False)
        return graph.subjects(predicate, self._identifier)

    @default_graph
    def subject_objects(
        self, graph: Optional[Graph] = None
    ) -> list[tuple[IRI, IRI | Literal]]:
        """Get subjects and objects of triples with Resource as predicate.

        Args:
            graph (Graph | None, optional):
                Graph where to search triples in. Defaults to None.

        Returns:
            list[tuple[IRI, IRI | Literal]]:
                List of triples, with Resource as object.
        """
        return graph.subject_objects(self._identifier)

    @default_graph
    def subject_predicates(
        self, graph: Optional[Graph] = None
    ) -> list[tuple[IRI, IRI]]:
        """Get subjects and predicates of triples with Resource as object.

        Args:
            graph (Graph | None, optional):
                Graph where to search triples in. Defaults to None.

        Returns:
            list[tuple[IRI, IRI]]:
                List of triples, with Resource as object.
        """
        return graph.subject_predicates(self._identifier)
