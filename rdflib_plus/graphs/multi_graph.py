"""Custom MultiGraph constructor"""

from rdflib import ConjunctiveGraph, Namespace

from rdflib_plus.config import (
    DEFAULT_FORMAT_FAST_MULTIGRAPH,
    DEFAULT_FORMAT_READABLE_MULTIGRAPH,
)
from rdflib_plus.graphs.build import build_custom_graph
from rdflib_plus.graphs.simple_graph import SimpleGraph


def get_subgraph(self, namespace: Namespace) -> SimpleGraph:
    """Get subgraph from MultiGraph.

    Args:
        namespace (Namespace):
            Namespace of target subgraph.

    Returns:
        Graph: Target subgraph.
    """

    # Get subgraph
    subgraph = SimpleGraph(
        store=self.store,
        identifier=namespace,
        namespace_manager=self.namespace_manager,
    )

    return subgraph


additional_methods = [get_subgraph]

MultiGraph = build_custom_graph(
    ConjunctiveGraph,
    DEFAULT_FORMAT_FAST_MULTIGRAPH,
    DEFAULT_FORMAT_READABLE_MULTIGRAPH,
    additional_methods=additional_methods,
)
