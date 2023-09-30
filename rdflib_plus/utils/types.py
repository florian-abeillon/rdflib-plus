"""Useful custom types"""

from typing import Any, Optional

from rdflib import ConjunctiveGraph, Graph
from rdflib import URIRef as IRI

ConstraintsType = dict[IRI, dict[str, Any]]
GraphType = Graph | ConjunctiveGraph
IdentifierType = str | int
IdentifierPropertyType = IRI | dict[str, IRI]
LangType = Optional[str]
PropertyConstraintsType = dict[IRI, dict[str, Any]]
ResourceOrIri = "Resource" | IRI
