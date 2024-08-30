"""Define test parameters for object elements"""

from rdflib import XSD, Literal

from tests.parameters.identifiers import PARAMETERS_IDENTIFIERS
from tests.parameters.langs import PARAMETERS_LANGS
from tests.utils import build_iri, cartesian_product

# 0 - String element (str)
PARAMETERS_ELEMENTS_STRING = [
    "a",
    "string",
    "Object",
    "customLabel",
    "12345",
]

# 0 - Literal string element (Literal)
PARAMETERS_ELEMENTS_LITERAL_STRING = [
    Literal(string, datatype=XSD.string)
    for string in PARAMETERS_ELEMENTS_STRING
]

# 0 - Literal string element with language (Literal)
PARAMETERS_ELEMENTS_LITERAL_LANGSTRING = [
    Literal(string, lang=lang)
    for string, lang in cartesian_product(
        PARAMETERS_ELEMENTS_STRING, PARAMETERS_LANGS
    )
]

# 0 - Integer element (int)
PARAMETERS_ELEMENTS_INTEGER = [
    0,
    1,
    12345,
]

# 0 - Literal integer element (Literal)
PARAMETERS_ELEMENTS_LITERAL_INTEGER = [
    Literal(integer, datatype=XSD.integer)
    for integer in PARAMETERS_ELEMENTS_INTEGER
]
# 0 - Float element (double)
PARAMETERS_ELEMENTS_DOUBLE = [
    0.0,
    1.5,
    123.45,
]

# 0 - Literal float element (Literal)
PARAMETERS_ELEMENTS_LITERAL_DOUBLE = [
    Literal(float_, datatype=XSD.double)
    for float_ in PARAMETERS_ELEMENTS_DOUBLE
]

# 0 - Boolean element (bool)
PARAMETERS_ELEMENTS_BOOLEAN = [
    True,
    False,
]

# 0 - Literal boolean element (Literal)
PARAMETERS_ELEMENTS_LITERAL_BOOLEAN = [
    Literal(boolean, datatype=XSD.boolean)
    for boolean in PARAMETERS_ELEMENTS_BOOLEAN
]

# 0 - IRI element (IRI)
PARAMETERS_ELEMENTS_IRI = [
    build_iri(legal_identifier)
    for (
        identifier,
        legal_identifier,
        datatype,
    ) in PARAMETERS_IDENTIFIERS
]

# 0 - Element (IRI | Literal | Any)
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
