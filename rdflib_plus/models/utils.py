"""Functions to define a custom Resource"""

from rdflib import Namespace

from rdflib_plus.models.rdf_property import Property
from rdflib_plus.models.rdfs_class import Class
from rdflib_plus.models.rdfs_resource import Resource


def define_resource(
    name: str, namespace: Namespace, parent_class: type = Resource, **kwargs
) -> Resource:
    """Dynamically define a new Resource as a class.

    Args:
        name (str):
            Name of the new Resource.
        namespace (Namespace):
            Namespace the Resource belongs to.

    Returns:
        Resource: Created Resource.
    """

    # Get Resource type
    type_iri = getattr(namespace, name)

    # Create Resource
    resource = type(name, (parent_class,), {"_type": type_iri, **kwargs})

    return resource


def define_class(name: str, namespace: Namespace, **kwargs) -> Class:
    """Dynamically define a new Class.

    Args:
        name (str):
            Name of the new Class.
        namespace (Namespace):
            Namespace the Class belongs to.

    Returns:
        Class: Created Class.
    """

    return define_resource(name, namespace, Class, **kwargs)


def define_property(name: str, namespace: Namespace, **kwargs) -> Property:
    """Dynamically define a new Property.

    Args:
        name (str):
            Name of the new Property.
        namespace (Namespace):
            Namespace the Property belongs to.

    Returns:
        Property: Created Property.
    """

    return define_resource(name, namespace, Property, **kwargs)
