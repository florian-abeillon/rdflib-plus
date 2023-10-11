"""RDFS Class constructor"""

import warnings
from typing import Optional, Union
from urllib.parse import urldefrag

from inflection import camelize
from rdflib import RDFS, Namespace
from rdflib import URIRef as IRI

from rdflib_plus.config import (
    DEFAULT_CHECK_TRIPLES,
    DEFAULT_HIERARCHICAL_PATH,
    DEFAULT_LANGUAGE,
)
from rdflib_plus.definitions import RDFS_CLASSES
from rdflib_plus.models.rdf.rdfs_resource import Resource, ResourceOrIri
from rdflib_plus.models.utils.types import (
    ConstraintsType,
    GraphType,
    IdentifierType,
    LangType,
)
from rdflib_plus.namespaces import DEFAULT_NAMESPACE
from rdflib_plus.utils import format_label

# Define specific custom type
SuperClassType = Union["Class", IRI, list[Union["Class", IRI]]]


class Class(Resource):
    """RDFS Class constructor"""

    # Class's RDF type
    _type: ResourceOrIri = RDFS.Class

    # Property that links Class to its parent(s)
    # Typehint: Property | IRI
    _parent_property: IRI = RDFS.subClassOf

    # Class's property constraints
    _constraints: ConstraintsType = Resource.update_constraints(
        RDFS_CLASSES[_type]["constraints"]
    )

    def __init__(
        self,
        graph: GraphType,
        label: str,
        identifier_property: Optional[IRI] = None,
        namespace: Optional[Namespace] = None,
        super_class: Optional[SuperClassType] = None,
        hierarchical_path: bool = DEFAULT_HIERARCHICAL_PATH,
        lang: LangType = DEFAULT_LANGUAGE,
        check_triples: bool = DEFAULT_CHECK_TRIPLES,
        bnode: bool = False,
        constraints: Optional[ConstraintsType] = None,
    ) -> None:
        """Initialize Class.

        Args:
            graph (Graph | MultiGraph):
                Graph to search or create Class into.
            label (str):
                Class's label.
            identifier_property (Optional[IRI | Property], optional):
                Class's specific identifier property.
                Defaults to None.
            namespace (Optional[Namespace], optional):
                Namespace to search or create Class into. Defaults to None.
            super_class (Optional[Class | IRI | list[Class | IRI]], optional):
                Class's super-class. Defaults to None.
            hierarchical_path (bool, optional):
                Whether to include Class's parent hierarchy in its path.
                Defaults to DEFAULT_HIERARCHICAL_PATH.
            lang (Optional[str], optional):
                Class's language. Defaults to DEFAULT_LANGUAGE.
            check_triples (bool, optional):
                Whether to check triples that are added or set using Class.
                Defaults to DEFAULT_CHECK_TRIPLES.
            bnode (bool, optional):
                Whether instances of Class should be blank nodes.
                Defaults to False.
            constraints (Optional[dict[IRI, dict[str, Any]]], optional):
                Class's specific constraints.
                Defaults to None.
        """

        # Set whether instances of Class should be blank nodes
        self.bnode = bnode

        # Initialize parent hierarchy
        path = []

        # If a single superclass is specified
        if super_class is not None and not isinstance(super_class, list):
            # If required, keep track of Class's parent hierarchy
            # using superclass's path (if it is a Class), or
            # superclass's fragment (if it is an IRI)
            if hierarchical_path:
                path = (
                    super_class.path
                    if isinstance(super_class, Class)
                    else [super_class.fragment]
                )

            # Turn superclass into a list for convenience
            super_class = [super_class]

        # Create Class as a Resource
        super().__init__(
            graph,
            label=label,
            path=path,
            identifier_property=identifier_property,
            namespace=namespace,
            lang=lang,
            check_triples=check_triples,
        )

        # Set constraints of instances of Class
        self.constraints_instance = self._get_constraints_instance(
            constraints, super_class
        )

        # Create constructor to create Class's instances
        self.instance = self._build_instance_constructor()

        # If superclass(es) was specified
        if super_class is not None:
            # For every superclass
            for class_ in super_class:
                # Get super_class's IRI
                class_iri = self._format_resource(class_)

                # Add hierarchical relation in the graph
                self.add(self._parent_property, class_iri)

    def _build_path(self, identifier: str) -> str:
        """Add Resource's identifier to IRI path.

        Args:
            identifier (str):
                Resource's identifier.

        Returns:
            str: Full Resource's IRI path.
        """

        # Add Class's identifier to self.path,
        # So that instances of Class have its identifier in their path
        self._path.append(identifier)

        # Add identifier to path as a pathinfo
        path = "/".join(self._path)

        return path

    @staticmethod
    def _format_identifier(identifier: str) -> str:
        """Format Class's identifier (in PascalCase).

        Args:
            identifier (str):
                Class's identifier.

        Returns:
            str: Formatted Class's identifier.
        """

        return camelize(format_label(identifier))

    def _get_constraints_instance(
        self,
        constraints: Optional[ConstraintsType] = None,
        super_class: Optional[SuperClassType] = None,
    ) -> ConstraintsType:
        """Set Class's 'constraints_instance' attribute.

        Args:
            constraints (Optional[dict[IRI, dict[str, Any]]], optional):
                Class's specific constraints. Defaults to None.
            super_class (Optional[list[Class | IRI]], optional):
                Class's super-class. Defaults to None.
        """

        # Initialize instance constraints
        constraints_instance = {}

        # If class-specific constraints and at least one super-class
        # are specified
        if constraints is not None and super_class is not None:
            # Initialize dictionary to collect
            # super-classes' instance constraints
            super_class_constraints = {}

            # For every super-class
            for class_ in super_class:
                # Overlook IRI super-classes as they do not include constraints
                if not isinstance(class_, Class):
                    continue

                # For every key-value pair of current super-class
                for constraint, value in class_.items():
                    # If current super-class has the same constraint as another
                    # super-class (and the same value), and this constraint is
                    # not overruled in class-specific constraints
                    if (
                        constraint in super_class_constraints
                        and constraint not in constraints
                        and value != super_class_constraints[constraint]
                    ):
                        # Raise a warning
                        warnings.warn(
                            f"""
                            {self}: Constraint '{constraint}' has conflicting
                            values in at least two super-classes. Please
                            harmonize the constraint values, or overrule them
                            by specifying a class-specific value.
                            """
                        )

                # Add current super-class's constraints
                super_class_constraints |= class_.constraints_instance

            # Update super-class's constraints with class-specific constraints
            constraints_instance = {
                **super_class_constraints,
                **constraints,
            }

        # Update Resource's constraints with class-specific's
        constraints_instance = Resource.update_constraints(
            constraints_instance
        )

        return constraints_instance

    def _build_instance_constructor(self) -> type:
        """Build Class's instance constructor.

        Returns:
            type: Class's instance constructor.
        """

        return type(
            f"{self.id_}Instance",
            (Resource,),
            {
                "_type": self,
                "_identifier_property": self._identifier_property,
                "_constraints": self.constraints_instance,
            },
        )

    def __call__(
        self,
        graph: Optional[GraphType] = None,
        identifier: Optional[IdentifierType] = None,
        label: Optional[str] = None,
        lang: LangType = DEFAULT_LANGUAGE,
        check_triples: Optional[bool] = None,
    ) -> Resource:
        """Create instance of Class.

        Args:
            graph (Optional[Graph | MultiGraph], optional):
                Graph to search or create instance into. Defaults to None.
            identifier (Optional[str | int], optional):
                Instance's identifier. Defaults to None.
            label (Optional[str], optional):
                Instance's label. Defaults to None.
            lang (Optional[str], optional):
                Instance's language. Defaults to DEFAULT_LANGUAGE.
            check_triples (Optional[bool], optional):
                Whether to check triples that are added or set using Resource.
                Defaults to None.

        Returns:
            Resource: Instance of Class.
        """

        # If no graph was specified, use Class's one
        if graph is None:
            graph = self._graph

        # If check_triples was not specified, use Class's one
        if check_triples is None:
            check_triples = self._check_triples

        # If Class's instances should blank nodes
        if self.bnode:
            # If an identifier was specified
            if identifier is not None:
                # Raise an error
                raise ValueError(
                    f"""
                    {self}: Trying to create instance as a blank node,
                    but an identifier is specified ('{identifier}').
                    """
                )

            # If a label was specified
            if label is not None:
                # Raise an error
                raise ValueError(
                    f"""
                    {self}: Trying to create instance as a blank node,
                    but a label is specified ('{label}').
                    """
                )

        # Create instance of Class
        instance = self.instance(
            graph,
            label=label,
            path=self._path,
            lang=lang,
        )

        return instance

    @classmethod
    def format_fragment(
        cls, fragment: str | IRI, namespace: Namespace = DEFAULT_NAMESPACE
    ) -> IRI:
        """Format fragment of IRI using Class's method.

        Args:
            fragment (str | IRI):
                Fragment or IRI to be formatted.

        Returns:
            IRI: IRI with formatted fragment.
        """

        # If fragment is an IRI
        if isinstance(fragment, IRI):
            # # If not custom IRI, return IRI
            # if not fragment.startswith(NS_DEFAULT):
            #     return fragment

            namespace, fragment = urldefrag(fragment)

        # Format fragment, and create IRI from it
        fragment = cls._format_identifier(fragment)
        iri = namespace[fragment]

        return iri
