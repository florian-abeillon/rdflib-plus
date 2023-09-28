"""Useful custom types"""

from typing import Optional

from rdflib import ConjunctiveGraph, Graph

GraphType = Graph | ConjunctiveGraph
IdentifierType = str | int
LangType = Optional[str]
