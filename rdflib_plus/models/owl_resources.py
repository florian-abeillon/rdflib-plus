"""OWL resources classes"""

from rdflib import OWL

from rdflib_plus.models.utils import define_resource


def define_owl_resource(name: str, is_property: bool = False):
    """Dynamically define an OWL resource as a class.

    Args:
        name (str):
            Name of the new resource.
        is_property (bool, optional):
            Whether resource is a Property (or a mere Class).
    """

    return define_resource(name, OWL, is_property=is_property)


# Define OWL resource classes
FunctionalProperty = define_owl_resource(
    "FunctionalProperty", is_property=True
)
InverseFunctionalProperty = define_owl_resource(
    "InverseFunctionalProperty", is_property=True
)
SymmetricProperty = define_owl_resource("SymmetricProperty", is_property=True)
TransitiveProperty = define_owl_resource(
    "TransitiveProperty", is_property=True
)
