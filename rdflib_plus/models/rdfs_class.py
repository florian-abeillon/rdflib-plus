"""RDFS Class class"""

from typing import Optional
from urllib.parse import urldefrag

from inflection import camelize
from rdflib import RDFS, Namespace
from rdflib import URIRef as IRI

from rdflib_plus.models.rdfs_resource import Resource
from rdflib_plus.models.types import GraphType, LangType
from rdflib_plus.utils import NS_DEFAULT, format_text

# Define specific custom types
SuperclassType = Optional["Class" | IRI | list["Class" | IRI]]


class Class(Resource):
    """RDFS class"""

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
        """

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
            graph, label=label, path=path, namespace=namespace, lang=lang
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
        """Format Class's identifier.

        Args:
            identifier (str):
                Class's identifier.

        Returns:
            str: Formatted Class's identifier.
        """

        return camelize(format_text(identifier))

    @classmethod
    def format_fragment(
        cls, fragment: str | IRI, namespace: Namespace = NS_DEFAULT
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
