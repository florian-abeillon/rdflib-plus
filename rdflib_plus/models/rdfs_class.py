"""RDFS Class class"""

from typing import Optional
from urllib.parse import urldefrag

from inflection import camelize
from rdflib import RDFS, Namespace
from rdflib import URIRef as IRI
from rdflib.term import _serial_number_generator

from rdflib_plus.models.rdfs_resource import Resource
from rdflib_plus.models.utils import DEFAULT_IDENTIFIER_PROPERTY
from rdflib_plus.utils import DEFAULT_NAMESPACE, format_label
from rdflib_plus.utils.types import (
    GraphType,
    IdentifierPropertyType,
    IdentifierType,
    LangType,
)

# Define specific custom types
SuperclassType = Optional["Class" | IRI | list["Class" | IRI]]


class Class(Resource):
    """RDFS Class"""

    # Property that links Class to its parent(s)
    _parent_property = RDFS.subClassOf

    # Class's RDF type
    _type = RDFS.Class

    def __init__(
        self,
        graph: GraphType,
        label: str,
        namespace: Optional[Namespace] = None,
        super_class: SuperclassType = None,
        hierarchical_path: bool = False,
        lang: LangType = None,
        check_triples: bool = True,
        bnode: bool = False,
        identifier_property: IdentifierPropertyType = DEFAULT_IDENTIFIER_PROPERTY,
    ):
        """Initialize Class.

        Args:
            graph (Graph | ConjunctiveGraph):
                Graph to search or create Class into.
            label (str):
                Class's label.
            namespace (Optional[Namespace], optional):
                Namespace to search or create Class into. Defaults to None.
            super_class (Optional[Class | IRI | list[Class | IRI]], optional):
                Class's super-class. Defaults to None.
            hierarchical_path (bool, optional):
                Whether to include Class's parent hierarchy in its path.
                Defaults to False.
            lang (Optional[str], optional):
                Class's language. Defaults to None.
            check_triples (bool, optional):
                Whether to check triples that are added or set using Class.
                Defaults to True.
            bnode (bool, optional):
                Whether instances of Class should be blank nodes.
                Defaults to False.
            identifier_property (bool, optional):
                Property that links a Class's instance to its identifier.
                Defaults to DEFAULT_IDENTIFIER_PROPERTY.
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
                    else super_class.fragment
                )

            # Turn superclass into a list for convenience
            super_class = [super_class]

        # Create Class as a Resource
        super().__init__(
            graph,
            label=label,
            path=path,
            namespace=namespace,
            lang=lang,
            check_triples=check_triples,
        )

        # Create class to create Class's instances
        self.instance = type(
            f"{self.id_}Instance",
            (Resource,),
            {"_type": self, "_identifier_property": identifier_property},
        )

        # If superclass(es) was specified
        if super_class is not None:
            # For every superclass
            for super_class_iri in super_class:
                # If necessary, get super_class's IRI
                if isinstance(super_class_iri, Class):
                    super_class_iri = super_class_iri.iri

                # Add hierarchical relation in the graph
                self.add(self._parent_property, super_class_iri)

    def build_path(self, identifier: str) -> str:
        """Add Resource's identifier to IRI path.

        Args:
            identifier (str):
                Resource's identifier.

        Returns:
            str: Full Resource's IRI path.
        """

        # Add Class's identifier to self.path,
        # So that instances of Class have its identifier in their path
        self.path.append(identifier)

        # Add identifier to path as a pathinfo
        path = "/".join(self.path)

        return path

    @staticmethod
    def format_identifier(identifier: str) -> str:
        """Format Class's identifier (in PascalCase).

        Args:
            identifier (str):
                Class's identifier.

        Returns:
            str: Formatted Class's identifier.
        """

        return camelize(format_label(identifier))

    def __call__(
        self,
        graph: Optional[GraphType] = None,
        identifier: Optional[IdentifierType] = None,
        label: Optional[str] = None,
        lang: LangType = None,
    ) -> Resource:
        """Create instance of Class.

        Args:
            graph (Optional[Graph | ConjunctiveGraph]):
                Graph to search or create instance into. Defaults to None.
            identifier (Optional[str | int], optional):
                Instance's identifier. Defaults to None.
            label (Optional[str], optional):
                Instance's label. Defaults to None.
            lang (Optional[str], optional):
                Instance's language. Defaults to None.

        Returns:
            Resource: Instance of Class.
        """

        # If no graph was specified, use Class's one
        if graph is None:
            graph = self._graph

        # If self is an instance of a blank nodes class
        if self.bnode:
            # Make sure no identifier nor label was given
            assert identifier is None and label is None

            # Generate blank node identifier
            identifier = _serial_number_generator()()

        # Create instance of Class
        instance = self.instance(
            graph,
            identifier=identifier,
            label=label,
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
        fragment = cls.format_identifier(fragment)
        iri = namespace[fragment]

        return iri
