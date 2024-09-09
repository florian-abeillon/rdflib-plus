"""Define test parameters for object elements"""

from rdflib import XSD, Literal

from tests.parameters.identifiers import PARAMETERS_IDENTIFIERS
from tests.parameters.langs import PARAMETERS_LANGS
from tests.utils import build_iri, cartesian_product

# Define example elements of different types
elements_string = [
    "a",
    "string",
    "Object",
    "customLabel",
    "12345",
]
elements_integer = [
    0,
    1,
    12345,
]
elements_double = [
    0.0,
    1.0,
    1.5,
    123.45,
]
elements_boolean = [
    True,
    False,
]
elements_iri = [
    build_iri(legal_identifier)
    for (
        identifier,
        legal_identifier,
        datatype,
    ) in PARAMETERS_IDENTIFIERS
]

# 0 - String element (str)
# 1 - String element as it should appear in the graph (Literal)
PARAMETERS_ELEMENTS_STRING = [
    (
        string,
        Literal(string, datatype=XSD.string),
    )
    for string in elements_string
]

# 0 - Literal string element (Literal)
# 1 - Literal string element as it should appear in the graph (Literal)
PARAMETERS_ELEMENTS_LITERAL_STRING = [
    (
        Literal(string, datatype=XSD.string),
        Literal(string, datatype=XSD.string),
    )
    for string in elements_string
]

# 0 - Literal string element with language (Literal)
# 1 - Literal string element with language as it should appear in the graph
PARAMETERS_ELEMENTS_LITERAL_LANGSTRING = [
    (Literal(string, lang=lang), Literal(string, lang=lang))
    for string, lang in cartesian_product(elements_string, PARAMETERS_LANGS)
]

# 0 - Integer element (int)
# 1 - Integer element as it should appear in the graph (Literal)
PARAMETERS_ELEMENTS_INTEGER = [
    (
        integer,
        Literal(integer, datatype=XSD.integer),
    )
    for integer in elements_integer
]

# 0 - Literal integer element (Literal)
# 1 - Literal integer element as it should appear in the graph (Literal)
PARAMETERS_ELEMENTS_LITERAL_INTEGER = [
    (
        Literal(integer, datatype=XSD.integer),
        Literal(integer, datatype=XSD.integer),
    )
    for integer in elements_integer
]

# 0 - Float element (float)
# 1 - Float element as it should appear in the graph (Literal)
PARAMETERS_ELEMENTS_DOUBLE = [
    (float_, Literal(float_, datatype=XSD.double))
    for float_ in elements_double
]

# 0 - Literal float element (Literal)
# 1 - Literal float element as it should appear in the graph (Literal)
PARAMETERS_ELEMENTS_LITERAL_DOUBLE = [
    (
        Literal(float_, datatype=XSD.double),
        Literal(float_, datatype=XSD.double),
    )
    for float_ in elements_double
]

# 0 - Boolean element (bool)
# 1 - Boolean element as it should appear in the graph (Literal)
PARAMETERS_ELEMENTS_BOOLEAN = [
    (boolean, Literal(boolean, datatype=XSD.boolean))
    for boolean in elements_boolean
]

# 0 - Literal boolean element (Literal)
# 1 - Literal boolean element as it should appear in the graph (IRI)
PARAMETERS_ELEMENTS_LITERAL_BOOLEAN = [
    (
        Literal(boolean, datatype=XSD.boolean),
        Literal(boolean, datatype=XSD.boolean),
    )
    for boolean in elements_boolean
]

# 0 - IRI element (IRI)
# 1 - IRI element as it should appear in the graph (IRI)
PARAMETERS_ELEMENTS_IRI = [(iri, iri) for iri in elements_iri]

# 0 - Element (IRI | Literal | Any)
# 1 - Element as it should appear in the graph (IRI | Literal | Any)
PARAMETERS_ELEMENTS = [
    *PARAMETERS_ELEMENTS_BOOLEAN,
    *PARAMETERS_ELEMENTS_DOUBLE,
    *PARAMETERS_ELEMENTS_INTEGER,
    *PARAMETERS_ELEMENTS_LITERAL_BOOLEAN,
    *PARAMETERS_ELEMENTS_LITERAL_DOUBLE,
    *PARAMETERS_ELEMENTS_LITERAL_INTEGER,
    *PARAMETERS_ELEMENTS_LITERAL_STRING,
    *PARAMETERS_ELEMENTS_LITERAL_LANGSTRING,
    *PARAMETERS_ELEMENTS_STRING,
    *PARAMETERS_ELEMENTS_IRI,
]
