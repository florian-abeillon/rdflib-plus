"""RDF Bag constructor"""

from rdflib import RDF

from rdflib_plus.models.rdf.rdfs_container import Container
from rdflib_plus.utils import ObjectType, ResourceOrIri


class Bag(Container):
    """RDF Bag constructor"""

    # Bag's RDF type
    _type: ResourceOrIri = RDF.Bag

    # def add(self, element: ObjectType) -> None:
    def add_item(self, element: ObjectType) -> None:
        """Append element to Bag.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to add to Bag.
        """

        super()._append(element)

    def discard(self, element: ObjectType) -> None:
        """Remove element from Bag,
           without raising error if it was not present.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to remove from Bag.
        """

        # Until there are elements with this value left in Bag
        while True:
            # Try to remove it
            try:
                super().remove_item(element)
            # Otherwise, stop iteration as none are left
            except ValueError:
                break

    # def remove(self, element: ObjectType) -> None:
    def remove_item(self, element: ObjectType) -> None:
        """Remove element from Bag,
           and raise an error if it was not present.

        Args:
            element (Resource | IRI | Literal | Any):
                Element to remove from Bag.
        """

        # Remove element
        super().remove_item(element)

        # Try to remove other instances of element, until none are left
        self.discard(element)

    def update(self, new_elements: "Bag" | list[ObjectType]) -> None:
        """Update Bag with new elements.

        Args:
            new_elements (Bag | list[Resource | IRI | Literal | Any]):
                New elements to add to Bag.
        """

        super()._extend(new_elements)
