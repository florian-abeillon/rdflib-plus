"""OWL Ontology class"""

from typing import Optional

from rdflib import OWL, RDFS, Literal, Namespace
from rdflib import URIRef as IRI

from rdflib_plus.models.rdfs_resource import Resource
from rdflib_plus.utils.types import (
    GraphType,
    IdentifierPropertyType,
    LangType,
    PropertyConstraintsType,
    ResourceOrIri,
)


class Ontology(Resource):
    """OWL Ontology"""

    # RDFS label of Ontology
    _identifier_property: IdentifierPropertyType = RDFS.label

    # Property constraints
    _constraints: PropertyConstraintsType = {
        OWL.versionInfo: Literal,
        RDFS.comment: Literal,
        OWL.priorVersion: IRI,
        OWL.imports: IRI,
    }

    # Resource's RDF type
    _type: ResourceOrIri = OWL.Ontology

    def __init__(
        self,
        graph: GraphType,
        label: str,
        version: Optional[str] = None,
        comment: Optional[str] = None,
        namespace: Optional[Namespace] = None,
        lang: LangType = None,
        check_triples: bool = True,
    ):
        """Initialize Ontology.

        Args:
            graph (Graph | ConjunctiveGraph):
                Graph to search or create Ontology into.
            label (str):
                Ontology's label.
            version (Optional[str], optional):
                Ontology's version. Defaults to None.
            comment (Optional[str], optional):
                Ontology's description. Defaults to None.
            namespace (Optional[Namespace], optional):
                Namespace to search or create Ontology into. Defaults to None.
            lang (Optional[str], optional):
                Ontology's language. Defaults to None.
            check_triples (bool, optional):
                Whether to check triples that are added or set using Ontology.
                Defaults to True.
        """

        super().__init__(
            graph,
            identifier=label,
            namespace=namespace,
            lang=lang,
            check_triples=check_triples,
        )

        # If any, set ontology version
        if version is not None:
            self.set(OWL.versionInfo, version)

        # If any, set ontology description as a RDFS comment
        if comment is not None:
            self.set(RDFS.comment, comment)
