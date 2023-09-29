"""Useful custom types"""

from typing import Optional

from rdflib import ConjunctiveGraph, Graph
from rdflib import URIRef as IRI

GraphType = Graph | ConjunctiveGraph
IdentifierType = str | int
IdentifierPropertyType = IRI | dict[str, IRI]
LangType = Optional[str]
