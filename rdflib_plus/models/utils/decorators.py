"""Useful decorators"""


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
