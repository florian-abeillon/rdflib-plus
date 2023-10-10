"""Custom MultiGraph constructor"""

from typing import Optional

from rdflib import ConjunctiveGraph, Namespace

from rdflib_plus.graphs.graph import Graph


class MultiGraph(ConjunctiveGraph, Graph):
    """Custom MultiGraph constructor"""

    def save(
        self, path: str, fast: bool = False, encoding: Optional[str] = None
    ) -> None:
        """Save MultiGraph locally.

        Args:
            path (str):
                Path where to save MultiGraph to.
            fast (bool, optional):
                Whether to save MultiGraph in a format that is faster to parse
                and serialize. Defaults to False.
            encoding (Optional[str], optional):
                Encoding to use when serializing MultiGraph. Defaults to None.
        """

        # Set format
        format_ = "nquads" if fast else "trig"

        # Serialize Graph
        super().serialize(destination=path, format=format_, encoding=encoding)

    def get_subgraph(self, namespace: Namespace) -> Graph:
        """Get subgraph from MultiGraph.

        Args:
            namespace (Namespace):
                Namespace of target subgraph.

        Returns:
            Graph: Target subgraph.
        """

        # Get subgraph
        subgraph = Graph(
            store=self.store,
            identifier=namespace,
            namespace_manager=self.namespace_manager,
        )

        return subgraph
