"""Define test parameters for paths"""

# 0 - Input path (list[str])
# 1 - Joined path (str)
PARAMETERS_PATHS: list[tuple[list[str], str]] = [
    (
        [],
        "",
    ),
    (
        ["ResourceParent"],
        "ResourceParent",
    ),
    (
        ["path", "to", "resource"],
        "path/to/resource",
    ),
]
