"""RDF Property constructor"""

import re
import warnings
from typing import Optional, Union

from inflection import camelize
from rdflib import OWL, RDF, RDFS, Graph, Namespace
from rdflib import URIRef as IRI

from rdflib_plus.config import (
    DEFAULT_CHECK_TRIPLES,
    DEFAULT_HIERARCHICAL_PATH,
    DEFAULT_LANGUAGE,
)
from rdflib_plus.definitions import RDFS_CLASSES
from rdflib_plus.models.rdf.rdfs_class import Class
from rdflib_plus.models.rdf.rdfs_resource import (
    ObjectType,
    Resource,
    ResourceOrIri,
)
from rdflib_plus.models.utils.types import ConstraintsType, LangType
from rdflib_plus.namespaces import stringify_iri
from rdflib_plus.utils import format_label

# Define specific custom types
PropertyOrIri = Union["Property", IRI]
SuperPropertyType = Union[PropertyOrIri, list[PropertyOrIri]]
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
        RDFS_CLASSES[_type]["constraints"]
    )

    def __init__(
        self,
        graph: Graph,
        label: str,
        namespace: Optional[Namespace] = None,
        local: bool = False,
        super_property: Optional[SuperPropertyType] = None,
        hierarchical_path: bool = DEFAULT_HIERARCHICAL_PATH,
        lang: LangType = DEFAULT_LANGUAGE,
        type_in_iri: bool = True,
        check_triples: bool = DEFAULT_CHECK_TRIPLES,
        constraints: Optional[ConstraintsType] = None,
    ) -> None:
        """Initialize Property.

        Args:
            graph (Graph):
                Graph to search or create Property into.
            label (str):
                Property's label.
            namespace (Namespace | None, optional):
                Namespace to search or create Property into. Defaults to None.
            local (bool, optional):
                Whether Resource only appears in the specified namespace.
                Defaults to False.
            super_property (Property | IRI | list[Property | IRI] | None,
                            optional):
                Property's super-property. Defaults to None.
            hierarchical_path (bool, optional):
                Whether to include Property's parent hierarchy in its path.
                Defaults to DEFAULT_HIERARCHICAL_PATH.
            lang (str | None, optional):
                Property's language. Defaults to DEFAULT_LANGUAGE.
            type_in_iri (bool, optional):
                Whether to include Resource's type in IRI. Defaults to True.
            check_triples (bool, optional):
                Whether to check triples that are added or set using Property.
                Defaults to DEFAULT_CHECK_TRIPLES.
            constraints (dict[IRI, dict[str, Any]] | None, optional):
                Class's specific constraints. Defaults to None.
        """

        super().__init__(
            graph,
            label,
            namespace=namespace,
            local=local,
            super_class=super_property,
            hierarchical_path=hierarchical_path,
            lang=lang,
            type_in_iri=type_in_iri,
            check_triples=check_triples,
            bnode=False,
            constraints=constraints,
        )

        # Set inverse property of Property
        self.inverse = self._set_inverse_property(
            graph,
            label,
            namespace=namespace,
            super_property=super_property,
            hierarchical_path=hierarchical_path,
            lang=lang,
        )

    @classmethod
    def _format_identifier(cls, identifier: str) -> str:
        """Format Property's identifier (in camelCase).

        Args:
            identifier (str): Property's identifier

        Returns:
            str: Formatted Property's identifier
        """

        # Format identifier
        identifier_formatted = camelize(
            format_label(identifier), uppercase_first_letter=False
        )

        # If a formatting has been necessary
        if identifier != identifier_formatted:
            # Raise a warning
            warnings.warn(
                f"{stringify_iri(cls._type)} '{identifier}': Formatting "
                f"identifier '{identifier}' into '{identifier_formatted}'."
            )

        return identifier_formatted

    def _get_label_inverse(self) -> Optional[str]:
        """Return label of Inverse property of Property, if appropriate.

        Returns:
            str | None: Label of Inverse property.
        """

        # Look for patterns like "has..." in Property's label
        res = re.fullmatch(r"has([A-Z]\w*)", self._id)
        if res:
            return f"is{res.group(1)}Of"

        # Look for patterns like "is...Of" in Property's label
        res = re.fullmatch(r"is([A-Z]\w*)Of", self._id)
        if res:
            return f"has{res.group(1)}"

        return None

    def _set_inverse_property(
        self,
        graph: Graph,
        label: str,
        namespace: Optional[Namespace] = None,
        super_property: Optional[SuperPropertyType] = None,
        hierarchical_path: bool = DEFAULT_HIERARCHICAL_PATH,
        lang: LangType = DEFAULT_LANGUAGE,
    ) -> Optional["Property"]:
        """Set potential inverse property of Property.

        Args:
            graph (Graph):
                Graph to search or create inverse Property into.
            label (str):
                Inverse Property's label.
            namespace (Namespace | None, optional):
                Namespace to search or create inverse Property into.
                Defaults to None.
            super_property (Property | IRI | list[Property | IRI] | None,
                            optional):
                Property's super-property. Defaults to None.
            hierarchical_path (bool, optional):
                Whether to include Property's parent hierarchy in its path.
                Defaults to False.
            lang (str | None, optional):
                Inverse Property's language. Defaults to None.

        Returns:
            Property | None: Inverse property if any, otherwise None.
        """

        # Initialize potential OWL inverse property
        inverse = None

        # Get label of potential inverse property
        label_inverse = self._get_label_inverse()

        # If Property can have an inverse property
        if label_inverse is not None:
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
            inverse = self.__class__(
                graph,
                label,
                namespace=namespace,
                super_property=super_property,
                hierarchical_path=hierarchical_path,
                lang=lang,
            )

            # Link Property to its inverse
            self.add(OWL.inverseOf, inverse.iri)

        return inverse

    def __call__(self, *args, **kwargs) -> Resource:
        """Null function, as vanilla Property object cannot be called"""

        # Raise an error
        raise AttributeError(f"{self}: Cannot call non-n-ary Property.")
