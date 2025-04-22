"""Useful decorators"""

from rdflib_plus.models.utils.utils import format_index


# TODO: Using protected member
def default_check_triple(func):
    """Decorator to default check_triple kwarg."""

    def wrapper(self, *args, **kwargs):
        if kwargs.get("check_triple") is None:
            kwargs["check_triple"] = self._check_triples
        return func(self, *args, **kwargs)

    return wrapper


def default_graph(func):
    """Decorator to default graph kwarg."""

    def wrapper(self, *args, **kwargs):
        if kwargs.get("graph") is None:
            kwargs["graph"] = self.graph
        return func(self, *args, **kwargs)

    return wrapper


def formatted_index(inserting: bool = False):
    """Decorator constructor."""

    def decorator(func):
        """Decorator to format index arg."""

        def wrapper(self, index: int, *args, **kwargs):
            index = format_index(index, len(self), inserting=inserting)
            return func(self, index, *args, **kwargs)

        return wrapper

    return decorator
