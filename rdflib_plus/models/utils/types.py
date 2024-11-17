"""Useful custom types"""

from typing import Any, Optional

from rdflib import URIRef as IRI

ConstraintsType = dict[IRI, dict[str, Any]]
IdentifierType = str | int
LangType = Optional[str]
