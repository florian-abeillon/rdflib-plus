"""Define test parameters for versions"""

# 0 - Version number (str)
# 1 - Whether the version number is well-formatted (bool)
PARAMETERS_VERSIONS: list[tuple[str, bool]] = [
    ("1", True),
    ("1.5", True),
    ("2.0.1", True),
    ("0.1.2.3", True),
    (".5", False),
    ("1.", False),
    ("version.number", False),
]
