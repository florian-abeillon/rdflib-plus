"""Define test parameters for key functions"""

# 0 - Functions to retrieve key to use in sorting (Callable)
PARAMETERS_KEY_FUNCTIONS = [
    lambda x: x,
    str,
    lambda x: str(type(x)),
    lambda x: 0,
]
