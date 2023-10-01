"""RDF Property constructor"""

import re
from typing import Optional

from inflection import camelize
from rdflib import OWL, RDF, RDFS, Namespace
from rdflib import URIRef as IRI

from rdflib_plus.definitions import RDF_PROPERTIES
from rdflib_plus.models.rdfs_class import Class
from rdflib_plus.models.rdfs_resource import Resource
from rdflib_plus.utils import format_label
from rdflib_plus.utils.types import (
    ConstraintsType,
    GraphType,
    LangType,
    PropertyConstraintsType,
    PropertyOrIri,
    ResourceOrIri,
)

# Define specific custom type
SuperPropertyType = "Property" | IRI | list["Property" | IRI]


class Property(Class):
    """RDF Property constructor"""

    # Property's RDF type
    _type: ResourceOrIri = RDF.Property

    # Property that links Property to its parent(s)
    _parent_property: PropertyOrIri = RDFS.subPropertyOf

    # Class's property constraints
    _constraints: PropertyConstraintsType = Resource.update_constraints(
        RDF_PROPERTIES[_type]["constraints"]
    )

    def __init__(
        self,
        graph: GraphType,
        label: str,
        namespace: Optional[Namespace] = None,
        super_property: Optional[SuperPropertyType] = None,
        hierarchical_path: bool = False,
        lang: LangType = None,
        check_triples: bool = True,
        constraints: Optional[ConstraintsType] = None,
    ):
        """Initialize Property.

        Args:
            graph (Graph | ConjunctiveGraph):
                Graph to search or create Property into.
            label (str):
                Property's label.
            namespace (Optional[Namespace], optional):
                Namespace to search or create Property into. Defaults to None.
            super_property (Optional[Property | IRI | list[Property | IRI]],
                            optional):
                Property's super-property. Defaults to None.
            hierarchical_path (bool, optional):
                Whether to include Class's parent hierarchy in its path.
                Defaults to False.
            lang (Optional[str], optional):
                Property's language. Defaults to None.
            check_triples (bool, optional):
                Whether to check triples that are added or set using Property.
                Defaults to True.
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
            constraints=constraints,
        )

        # Initialize potential OWL Inverse property
        inverse_property = None

        # Look for patterns like "has..." or "is...Of"
        # In Property's label
        res = re.match(r"has([A-Z]\w*)$", self.id_)
        if res:
            inverse_property = f"is{res.group(1)}Of"
        else:
            res = re.match(r"is([A-Z]\w*)Of$", self.id_)
            if res:
                inverse_property = f"has{res.group(1)}"

        # If one pattern was found
        if inverse_property is not None:
            # Define inverse property
            inverse_property = Property(
                graph,
                inverse_property,
                namespace=namespace,
                super_property=super_property,
                hierarchical_path=hierarchical_path,
                lang=lang,
            )

            # Add inverse relation in the graph
            self.add(OWL.inverseOf, inverse_property.iri)

    @staticmethod
    def format_identifier(identifier: str) -> str:
        """Format Property's identifier (in camelCase).

        Args:
            identifier (str): Property's identifier

        Returns:
            str: Formatted Property's identifier
        """

        return camelize(format_label(identifier), uppercase_first_letter=False)
