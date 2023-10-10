"""Useful custom types"""

from typing import Any, Optional

from rdflib import ConjunctiveGraph as MultiGraph
from rdflib import Graph
from rdflib import URIRef as IRI

ConstraintsType = dict[IRI, dict[str, Any]]
GraphType = Graph | MultiGraph
IdentifierType = str | int
IdentifierPropertyType = IRI | dict[str, IRI]
LangType = Optional[str]
