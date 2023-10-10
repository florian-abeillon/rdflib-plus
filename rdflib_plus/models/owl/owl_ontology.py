"""OWL Ontology constructor"""

from typing import Optional

from rdflib import OWL, RDFS, Namespace

from rdflib_plus.config import DEFAULT_CHECK_TRIPLES, DEFAULT_LANGUAGE
from rdflib_plus.definitions import RDFS_CLASSES
from rdflib_plus.models.rdf.rdf_property import PropertyOrIri
from rdflib_plus.models.rdf.rdfs_resource import Resource, ResourceOrIri
from rdflib_plus.models.utils.types import ConstraintsType, GraphType, LangType


class Ontology(Resource):
    """OWL Ontology constructor"""

    # Resource's RDF type
    _type: ResourceOrIri = OWL.Ontology

    # RDFS label of Ontology
    _identifier_property: PropertyOrIri = RDFS.label

    # Property constraints
    _constraints: ConstraintsType = Resource.update_constraints(
        RDFS_CLASSES[_type]["constraints"]
    )

    def __init__(
        self,
        graph: GraphType,
        label: str,
        version: Optional[str] = None,
        comment: Optional[str] = None,
        namespace: Optional[Namespace] = None,
        lang: LangType = DEFAULT_LANGUAGE,
        check_triples: bool = DEFAULT_CHECK_TRIPLES,
    ) -> None:
        """Initialize Ontology.

        Args:
            graph (Graph | MultiGraph):
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
                Ontology's language. Defaults to DEFAULT_LANGUAGE.
            check_triples (bool, optional):
                Whether to check triples that are added or set using Ontology.
                Defaults to DEFAULT_CHECK_TRIPLES.
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
