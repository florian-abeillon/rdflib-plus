"""Property with attributes"""

from typing import Optional

from rdflib import Graph

from rdflib_plus.config import DEFAULT_CHECK_TRIPLES
from rdflib_plus.models.custom.n_ary_property import NaryProperty
from rdflib_plus.models.rdf.rdfs_resource import Resource, ResourceOrIri
from rdflib_plus.namespaces import DEFAULT_NAMESPACE


class PropertyWithAttributes(NaryProperty):
    """Constructor of Property with attributes"""

    # PropertyWithAttributes's RDF type
    _type: ResourceOrIri = DEFAULT_NAMESPACE["PropertyWithAttributes"]

    def __call__(
        self,
        graph: Optional[Graph] = None,
        check_triples: Optional[bool] = DEFAULT_CHECK_TRIPLES,
        **kwargs
    ) -> Resource:
        """Create instance of Property with attributes.

        Args:
            graph (Graph | None, optional):
                Graph to search or create instance into. Defaults to None.
            check_triples (bool | None, optional):
                Whether to check triples that are added or set using Resource.
                Defaults to None.

        Returns:
            Resource: Instance of Property with attributes.
        """

        # Parse attributes into the appropriate format to be set
        attributes = [(p, o, True) for p, o in kwargs.items()]

        # Create n-ary property
        return super().__call__(
            self, outgoing=attributes, graph=graph, check_triples=check_triples
        )
