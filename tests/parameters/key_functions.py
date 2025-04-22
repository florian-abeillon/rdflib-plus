"""Define test parameters for key functions"""

# 0 - Functions to retrieve key to use in sorting (Callable | None)
PARAMETERS_KEY_FUNCTIONS = [
    # None,
    # lambda x: x,
    str,
    lambda x: str(type(x)),
    lambda x: 0,
]
