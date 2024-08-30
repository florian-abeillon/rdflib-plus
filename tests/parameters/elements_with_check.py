"""Define test parameters for object elements"""

from rdflib import XSD, Literal

from tests.parameters.elements import (
    PARAMETERS_ELEMENTS_BOOLEAN,
    PARAMETERS_ELEMENTS_DOUBLE,
    PARAMETERS_ELEMENTS_INTEGER,
    PARAMETERS_ELEMENTS_IRI,
    PARAMETERS_ELEMENTS_LITERAL_BOOLEAN,
    PARAMETERS_ELEMENTS_LITERAL_DOUBLE,
    PARAMETERS_ELEMENTS_LITERAL_INTEGER,
    PARAMETERS_ELEMENTS_LITERAL_LANGSTRING,
    PARAMETERS_ELEMENTS_LITERAL_STRING,
    PARAMETERS_ELEMENTS_STRING,
)

# 0 - String element (str)
# 1 - String element as it should appear in the graph (Literal)
PARAMETERS_ELEMENTS_STRING_WITH_CHECK = [
    (
        string,
        Literal(string, datatype=XSD.string),
    )
    for string in PARAMETERS_ELEMENTS_STRING
]


# 0 - Literal string element (Literal)
# 1 - Literal string element as it should appear in the graph (Literal)
PARAMETERS_ELEMENTS_LITERAL_STRING_WITH_CHECK = [
    (literal_string, literal_string)
    for literal_string in PARAMETERS_ELEMENTS_LITERAL_STRING
]

# 0 - Literal string element with language (Literal)
# 1 - Literal string element with language as it should appear in the graph
#     (Literal)
PARAMETERS_ELEMENTS_LITERAL_LANGSTRING_WITH_CHECK = [
    (literal_string_with_lang, literal_string_with_lang)
    for literal_string_with_lang in PARAMETERS_ELEMENTS_LITERAL_LANGSTRING
]

# 0 - Integer element (int)
# 1 - Integer element as it should appear in the graph (Literal)
PARAMETERS_ELEMENTS_INTEGER_WITH_CHECK = [
    (
        integer,
        Literal(integer, datatype=XSD.integer),
    )
    for integer in PARAMETERS_ELEMENTS_INTEGER
]

# 0 - Literal integer element (Literal)
# 1 - Literal integer element as it should appear in the graph (Literal)
PARAMETERS_ELEMENTS_LITERAL_INTEGER_WITH_CHECK = [
    (literal_integer, literal_integer)
    for literal_integer in PARAMETERS_ELEMENTS_LITERAL_INTEGER
]


# 0 - Float element (float)
# 1 - Float element as it should appear in the graph (Literal)
PARAMETERS_ELEMENTS_DOUBLE_WITH_CHECK = [
    (float_, Literal(float_, datatype=XSD.double))
    for float_ in PARAMETERS_ELEMENTS_DOUBLE
]

# 0 - Literal float element (Literal)
# 1 - Literal float element as it should appear in the graph (Literal)
PARAMETERS_ELEMENTS_LITERAL_DOUBLE_WITH_CHECK = [
    (literal_double, literal_double)
    for literal_double in PARAMETERS_ELEMENTS_LITERAL_DOUBLE
]

# 0 - Boolean element (bool)
# 1 - Boolean element as it should appear in the graph (Literal)
PARAMETERS_ELEMENTS_BOOLEAN_WITH_CHECK = [
    (boolean, Literal(boolean, datatype=XSD.boolean))
    for boolean in PARAMETERS_ELEMENTS_BOOLEAN
]

# 0 - Literal boolean element (Literal)
# 1 - Literal boolean element as it should appear in the graph (Literal)
PARAMETERS_ELEMENTS_LITERAL_BOOLEAN_WITH_CHECK = [
    (literal_boolean, literal_boolean)
    for literal_boolean in PARAMETERS_ELEMENTS_LITERAL_BOOLEAN
]

# 0 - IRI element (IRI)
# 1 - IRI element as it should appear in the graph (IRI)
PARAMETERS_ELEMENTS_IRI_WITH_CHECK = [
    (iri, iri) for iri in PARAMETERS_ELEMENTS_IRI
]
