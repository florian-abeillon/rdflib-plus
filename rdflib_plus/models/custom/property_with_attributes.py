"""Property with attributes"""

from typing import Optional

from rdflib_plus.config import DEFAULT_CHECK_TRIPLES
from rdflib_plus.models.custom.n_ary_property import NaryProperty
from rdflib_plus.models.rdf.rdfs_resource import Resource
from rdflib_plus.utils import GraphType


class PropertyWithAttributes(NaryProperty):
    """Constructor of Property with attributes"""

    def __call__(
        self,
        graph: Optional[GraphType] = None,
        check_triples: Optional[bool] = DEFAULT_CHECK_TRIPLES,
        **kwargs
    ) -> Resource:
        """Create instance of Property with attributes.

        Args:
            graph (Optional[Graph | MultiGraph], optional):
                Graph to search or create instance into. Defaults to None.
            check_triples (Optional[bool], optional):
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
