"""OWL Ontology constructor"""

import re
import warnings
from typing import Optional

from rdflib import OWL, RDFS, Graph, Namespace

from rdflib_plus.config import DEFAULT_CHECK_TRIPLES, DEFAULT_LANGUAGE
from rdflib_plus.definitions import RDFS_CLASSES
from rdflib_plus.models.rdf.rdf_property import PropertyOrIri
from rdflib_plus.models.rdf.rdfs_resource import Resource, ResourceOrIri
from rdflib_plus.models.utils.types import ConstraintsType, LangType


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
        graph: Graph,
        label: str,
        version: Optional[str] = None,
        comment: Optional[str] = None,
        namespace: Optional[Namespace] = None,
        lang: LangType = DEFAULT_LANGUAGE,
        check_triples: bool = DEFAULT_CHECK_TRIPLES,
    ) -> None:
        """Initialize Ontology.

        Args:
            graph (Graph):
                Graph to search or create Ontology into.
            label (str):
                Ontology's label.
            version (str | None, optional):
                Ontology's version. Defaults to None.
            comment (str | None, optional):
                Ontology's description. Defaults to None.
            namespace (Namespace | None, optional):
                Namespace to search or create Ontology into. Defaults to None.
            lang (str | None, optional):
                Ontology's language. Defaults to DEFAULT_LANGUAGE.
            check_triples (bool, optional):
                Whether to check triples that are added or set using Ontology.
                Defaults to DEFAULT_CHECK_TRIPLES.
        """

        super().__init__(
            graph,
            identifier=label,
            namespace=namespace,
            local=True,
            lang=lang,
            check_triples=check_triples,
        )

        # If an ontology version is specified
        if version is not None:
            self._set_version_number(version)

        # If any, set ontology description as a RDFS comment
        if comment is not None:
            self.set(RDFS.comment, comment)

    def _set_version_number(self, version: str) -> None:
        """Set version number of Ontology.

        Args:
            version (str): Version number.
        """

        # If version number is not in the right format
        if version and (
            not re.fullmatch(r"[\d\.]*", version)
            or ".." in version
            or version[0] == "."
            or version[-1] == "."
        ):
            # Raise a warning
            warnings.warn(
                f"'{self}': Version number '{version}' is not in the "
                "appropriate format. Setting it anyway."
            )

        # Set ontology version
        self.set(OWL.versionInfo, version)
