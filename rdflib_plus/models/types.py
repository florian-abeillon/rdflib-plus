"""Define useful custom types"""

from typing import Optional

from rdflib import ConjunctiveGraph, Graph
from rdflib import URIRef as IRI

FragmentType = str | IRI
GraphType = Graph | ConjunctiveGraph
IdentifierType = str | int
LangType = Optional[str]
PathType = Optional[list[str]]
