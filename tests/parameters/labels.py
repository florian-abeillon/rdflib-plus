"""Define test parameters for labels"""

# 0 - Input label (str)
# 1 - Label legalized for IRI (str)
# 2 - camelCase label (str)
# 3 - camelCase label legalized for IRI (str)
# 4 - PascalCase label (str)
# 5 - PascalCase label legalized for IRI (str)
PARAMETERS_LABELS: list[tuple[str, str, str, str, str]] = [
    # # Empty string
    # (
    #     "",
    #     "",
    #     "",
    #     "",
    #     "",
    #     "",
    # ),
    # Lowercase string
    (
        "label",
        "label",
        "Label",
        "Label",
        "label",
        "label",
    ),
    # PascalCase string
    (
        "Label",
        "Label",
        "Label",
        "Label",
        "label",
        "label",
    ),
    # Uppercase string
    (
        "LABEL",
        "LABEL",
        "LABEL",
        "LABEL",
        "lABEL",
        "lABEL",
    ),
    # camelCase string
    (
        "laBel",
        "laBel",
        "LaBel",
        "LaBel",
        "laBel",
        "laBel",
    ),
    # String with underscores
    (
        "label_in_several_parts",
        "label_in_several_parts",
        "LabelInSeveralParts",
        "LabelInSeveralParts",
        "labelInSeveralParts",
        "labelInSeveralParts",
    ),
    # Version number
    (
        "0.1.0",
        "0.1.0",
        "0.1.0",
        "0.1.0",
        "0.1.0",
        "0.1.0",
    ),
    # Number
    (
        "123456789",
        "123456789",
        "123456789",
        "123456789",
        "123456789",
        "123456789",
    ),
    # Upper and kebab-case string
    (
        "R2-D2",
        "R2-D2",
        "R2D2",
        "R2D2",
        "r2D2",
        "r2D2",
    ),
    # String with punctuation
    (
        "fun.",
        "fun.",
        "Fun.",
        "Fun.",
        "fun.",
        "fun.",
    ),
    # Potential ttl injection
    (
        "label> a rdfs:Resource . <http://evil.com#command> a "
        "<http://evil.com#injection",
        "label%3E%20a%20rdfs:Resource%20.%20%3Chttp:%2F%2Fevil.com%23command"
        "%3E%20a%20%3Chttp:%2F%2Fevil.com%23injection",
        "Label> a rdfs:resource . <http://evil.com#command> a "
        "<http://evil.com#injection",
        "Label%3E%20a%20rdfs:resource%20.%20%3Chttp:%2F%2Fevil.com%23command"
        "%3E%20a%20%3Chttp:%2F%2Fevil.com%23injection",
        "label> a rdfs:resource . <http://evil.com#command> a "
        "<http://evil.com#injection",
        "label%3E%20a%20rdfs:resource%20.%20%3Chttp:%2F%2Fevil.com%23command"
        "%3E%20a%20%3Chttp:%2F%2Fevil.com%23injection",
    ),
    # Illegal characters
    (
        "illegal:/?#[]@!$&'()*+,;=.",
        "illegal:%2F%3F%23%5B%5D@%21%24%26%27()%2A%2B%2C%3B%3D.",
        "Illegal:/?#[]@!$&'()*+,;=.",
        "Illegal:%2F%3F%23%5B%5D@%21%24%26%27()%2A%2B%2C%3B%3D.",
        "illegal:/?#[]@!$&'()*+,;=.",
        "illegal:%2F%3F%23%5B%5D@%21%24%26%27()%2A%2B%2C%3B%3D.",
    ),
]
