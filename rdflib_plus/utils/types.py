"""Useful custom types"""

from typing import Any, Optional

from rdflib import ConjunctiveGraph, Graph, Literal
from rdflib import URIRef as IRI

GraphType = Graph | ConjunctiveGraph
IdentifierType = str | int
IdentifierPropertyType = IRI | dict[str, IRI]
LangType = Optional[str]
ObjectType = "Resource" | IRI | Literal | Any
PropertyConstraintsType = dict[IRI, dict[str, Any]]
ResourceOrIri = "Resource" | IRI
