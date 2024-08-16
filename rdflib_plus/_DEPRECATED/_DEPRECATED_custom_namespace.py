"""CustomNamespace and associated CustomIRI classes"""

from rdflib import Namespace
from rdflib import URIRef as IRI


class CustomIRI(IRI):
    """Vanilla IRI constructor, with overriden 'fragment' property"""

    @property
    def fragment(self) -> str:
        """Get IRI's last element.

        Returns:
            str: IRI fragment, or last element of IRI's path.

        Example:
        >>> CustomIRI("http://example.com/some/path#some-fragment").fragment
        'some-fragment'
        >>> CustomIRI("http://example.com/some/path/some-fragment").fragment
        'some-fragment'
        """

        fragment = super().fragment

        # If no fragment, get last element of path
        if not fragment:
            fragment = self.rsplit("/", 1)[-1]

        return fragment


class CustomNamespace(Namespace):
    """Namespace overriding IRI"""

    def term(self, name: str) -> CustomIRI:
        """Override IRI term() method with CustomIRI.

        Args:
            name (str): Name of the resource in the namespace.

        Returns:
            CustomIRI: IRI with overriden fragment property.
        """

        return CustomIRI(super().term(name))
