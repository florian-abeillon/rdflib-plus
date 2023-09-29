"""Default constants and useful functions"""

from rdflib import DCTERMS, Namespace

from rdflib_plus.models.rdf_property import Property
from rdflib_plus.models.rdfs_class import Class

# Default property to link a Resource to its identifier
DEFAULT_IDENTIFIER_PROPERTY = DCTERMS.identifier


def define_resource(
    name: str, namespace: Namespace, is_property: bool = False
):
    """Dynamically define a new resource as a class.

    Args:
        name (str):
            Name of the new resource.
        namespace (Namespace):
            Namespace the resource belongs to.
        is_property (bool, optional):
            Whether resource is a Property (or a mere Class).
    """

    super_class = Property if is_property else Class
    type_iri = getattr(namespace, name)
    return type(name, (super_class,), {"_type": type_iri})
