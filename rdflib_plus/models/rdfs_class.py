"""RDFS Class class"""

from typing import Optional

from inflection import camelize
from rdflib import RDFS, Namespace
from rdflib import URIRef as IRI

from ..utils import NS_DEFAULT, format_text
from .resource import Resource
from .types import GraphType, LangType


class Class(Resource):
    """RDFS class"""

    _type = RDFS.Class

    def __init__(
        self,
        graph: GraphType,
        label: str,
        namespace: Optional[Namespace] = None,
        superclass: Optional["Class"] = None,
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
            superclass (Optional[Class], optional):
                Class's super-class. Defaults to None.
            lang (Optional[str], optional):
                Class's language. Defaults to None.
        """

        # If a superclass is specified, set its path as Class's base path
        path = superclass.path if superclass is not None else []

        # Create Class as a Resource
        super().__init__(
            graph, label=label, path=path, namespace=namespace, lang=lang
        )

        # If a superclass was specified
        if superclass is not None:
            # Add RDFS.subClassOf relation in the graph
            self.add(RDFS.subClassOf, superclass)

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

    # TODO
    @classmethod
    def format_fragment(cls, fragment: str | IRI) -> IRI:
        """Format fragment of IRI using Class method

        Args:
            fragment (str | IRI): _description_

        Returns:
            IRI: _description_
        """

        # If fragment is an IRI
        if isinstance(fragment, IRI):
            # If not custom IRI, return IRI
            if not fragment.startswith(NS_DEFAULT):
                return fragment

            fragment = fragment.fragment

        # Format fragment
        fragment = cls.format_identifier(fragment)
        return NS_DEFAULT[fragment]
