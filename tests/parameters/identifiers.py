"""Define test parameters for identifiers"""

from rdflib import XSD

from tests.parameters.labels import PARAMETERS_LABELS

# 0 - Input identifier (str | int)
# 1 - Identifier legalized for IRI (str)
# 2 - Datatype of identifier (IRI)
PARAMETERS_IDENTIFIERS: list[tuple[str | int, str]] = [
    (
        1,
        "1",
        XSD.integer,
    ),
    (
        42,
        "42",
        XSD.integer,
    ),
    (
        666,
        "666",
        XSD.integer,
    ),
    (
        2023,
        "2023",
        XSD.integer,
    ),
    (
        123456789,
        "123456789",
        XSD.integer,
    ),
    *[
        (label, legal_label, XSD.string)
        for (
            label,
            legal_label,
            label_PascalCase,
            legal_label_PascalCase,
            label_camelCase,
            legal_label_camelCase,
        ) in PARAMETERS_LABELS
    ],
]
