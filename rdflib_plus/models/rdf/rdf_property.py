"""RDF Property constructor"""

import re
import warnings
from typing import Optional

from inflection import camelize
from rdflib import OWL, RDF, RDFS, Namespace
from rdflib import URIRef as IRI

from rdflib_plus.config import (
    DEFAULT_CHECK_TRIPLES,
    DEFAULT_HIERARCHICAL_PATH,
    DEFAULT_LANGUAGE,
)
from rdflib_plus.definitions import RDF_PROPERTIES
from rdflib_plus.models.rdf.rdfs_class import Class
from rdflib_plus.models.rdf.rdfs_resource import Resource
from rdflib_plus.utils import (
    ConstraintsType,
    GraphType,
    LangType,
    ObjectType,
    PropertyOrIri,
    ResourceOrIri,
    format_label,
)

# Define specific custom types
SuperPropertyType = "Property" | IRI | list["Property" | IRI]
ParsedPairType = tuple[ResourceOrIri, ObjectType, bool]
UnparsedPairType = tuple[ResourceOrIri, ObjectType] | ParsedPairType
UnparsedPairListType = list[UnparsedPairType]


class Property(Class):
    """RDF Property constructor"""

    # Property's RDF type
    _type: ResourceOrIri = RDF.Property

    # Property that links Property to its parent(s)
    _parent_property: PropertyOrIri = RDFS.subPropertyOf

    # Class's property constraints
    _constraints: ConstraintsType = Resource.update_constraints(
        RDF_PROPERTIES[_type]["constraints"]
    )

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
                Whether to include Property's parent hierarchy in its path.
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
            super_class=super_property,
            hierarchical_path=hierarchical_path,
            lang=lang,
            check_triples=check_triples,
            bnode=False,
            constraints=constraints,
        )

        # Initialize potential OWL Inverse property
        self.inverse = None

        # If Property can have an Inverse property
        # Get its label
        label_inverse = self._get_label_inverse()

        if label_inverse:
            # Build it
            self.inverse = self._build_inverse(
                graph,
                label_inverse,
                namespace=namespace,
                super_property=super_property,
                hierarchical_path=hierarchical_path,
                lang=lang,
            )

            # Link Property to its inverse
            self.add(OWL.inverseOf, self.inverse.iri)

    @staticmethod
    def _format_identifier(identifier: str) -> str:
        """Format Property's identifier (in camelCase).

        Args:
            identifier (str): Property's identifier

        Returns:
            str: Formatted Property's identifier
        """

        return camelize(format_label(identifier), uppercase_first_letter=False)

    def _get_label_inverse(self) -> Optional[str]:
        """Return label of Inverse property of Property, if appropriate.

        Returns:
            Optional[str]: Label of Inverse property.
        """

        # Look for patterns like "has..." in Property's label
        res = re.match(r"has([A-Z]\w*)$", self.id_)
        if res:
            return f"is{res.group(1)}Of"

        # Look for patterns like "is...Of" in Property's label
        res = re.match(r"is([A-Z]\w*)Of$", self.id_)
        if res:
            return f"has{res.group(1)}"

        return None

    def _build_inverse(
        self,
        graph: GraphType,
        label: str,
        namespace: Optional[Namespace] = None,
        super_property: Optional[SuperPropertyType] = None,
        hierarchical_path: bool = DEFAULT_HIERARCHICAL_PATH,
        lang: LangType = DEFAULT_LANGUAGE,
    ) -> "Property":
        """Build potential inverse Property of Property

        Args:
            graph (Graph | MultiGraph):
                Graph to search or create inverse Property into.
            label (str):
                Inverse Property's label.
            namespace (Optional[Namespace], optional):
                Namespace to search or create inverse Property into.
                Defaults to None.
            super_property (Optional[Property | IRI | list[Property | IRI]],
                            optional):
                Property's super-property. Defaults to None.
            hierarchical_path (bool, optional):
                Whether to include Property's parent hierarchy in its path.
                Defaults to False.
            lang (Optional[str], optional):
                Inverse Property's language. Defaults to None.

        Returns:
            Property: Inverse property.
        """

        # If a super-property is specified
        if super_property is not None:
            # Turn single super_property into list
            if not isinstance(super_property, list):
                super_property = [super_property]

            # Replace every super-property by its inverse
            super_property = [
                property_.inverse
                for property_ in super_property
                if isinstance(property_, Property)
            ]

        # Create inverse property
        inverse = Property(
            graph,
            label,
            namespace=namespace,
            super_property=super_property,
            hierarchical_path=hierarchical_path,
            lang=lang,
        )

        return inverse

    def __call__(self, *args, **kwargs) -> Resource:
        """Null function, as vanilla Property object cannot be called"""

        # Raise warning and error
        warnings.warn(f"Cannot call Property '{self.iri}'.")
        raise NotImplementedError
