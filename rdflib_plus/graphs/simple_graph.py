"""Custom SimpleGraph constructor"""

from rdflib import Graph

from rdflib_plus.config import (
    DEFAULT_FORMAT_FAST_SIMPLEGRAPH,
    DEFAULT_FORMAT_READABLE_SIMPLEGRAPH,
)
from rdflib_plus.graphs.build import build_custom_graph

SimpleGraph = build_custom_graph(
    Graph, DEFAULT_FORMAT_FAST_SIMPLEGRAPH, DEFAULT_FORMAT_READABLE_SIMPLEGRAPH
)
