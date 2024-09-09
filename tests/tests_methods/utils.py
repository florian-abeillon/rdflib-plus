"""Useful functions for testing methods"""

import copy
import random as rd
from typing import Any, Callable, Optional

from rdflib import RDF, Literal
from rdflib import URIRef as IRI

from rdflib_plus import (
    Alt,
    Bag,
    Class,
    List,
    MultiGraph,
    Resource,
    Seq,
    SimpleGraph,
)
from tests.parameters import PARAMETERS_ELEMENT_LISTS, PARAMETERS_IDENTIFIERS
from tests.utils import check_rem_add, parse_element_list_with_check


def build_alt(
    element_list: Optional[list[IRI | Literal | Any]] = None,
    graph: Optional[SimpleGraph | MultiGraph] = None,
) -> Alt:
    """Build Alt from element list."""

    # If no element list is specified
    if element_list is None:
        # Randomly select list of elements
        element_list = rd.choice(PARAMETERS_ELEMENT_LISTS)

    # If no graph is specified, initialize it
    if graph is None:
        graph = SimpleGraph()

    # Create Alt
    if element_list:
        default, *alternatives = element_list
        alt = Alt(graph, default=default, alternatives=alternatives)
    else:
        alt = Alt(graph)

    return alt


def build_collection(
    model: type,
    element_list: Optional[list[IRI | Literal | Any]] = None,
    graph: Optional[SimpleGraph | MultiGraph] = None,
) -> Alt | Bag | List | Seq:
    """Build Collection object from (random) element list."""

    # If no element list is specified
    if element_list is None:
        # Randomly select list of elements
        element_list = rd.choice(PARAMETERS_ELEMENT_LISTS)

    # If model is Alt, create an Alt
    if model == Alt:
        return build_alt(element_list=element_list, graph=graph)

    # If no graph is specified, initialize it
    if graph is None:
        graph = SimpleGraph()

    # Create object
    collection = model(graph, elements=element_list)

    return collection


def build_object(
    graph: SimpleGraph | MultiGraph,
    predicate_iri: IRI,
    object_: Any,
    is_object_resource: bool,
) -> Any | Resource | Class:
    """Build object with the appropriate form."""

    if is_object_resource:
        object_ = (
            Class(graph, object_)
            if predicate_iri == RDF.type
            else Resource(graph, object_)
        )

    return object_


def build_predicate_object(
    graph: SimpleGraph | MultiGraph,
    predicate_iri: IRI,
    is_predicate_resource: bool,
    object_: Any,
    is_object_resource: bool,
) -> tuple[Resource | IRI, Any | Resource | Class]:
    """Build predicate and object with the appropriate form."""

    # Create predicate
    predicate = (
        Resource(graph, iri=predicate_iri)
        if is_predicate_resource
        else predicate_iri
    )

    # Create object
    object_ = build_object(graph, predicate_iri, object_, is_object_resource)

    return predicate, object_


def build_resource(model: type = Resource) -> Resource:
    """Build a Resource with an arbitrary label."""

    # Randomly select an identifier
    identifier, legal_identifier, datatype = rd.choice(PARAMETERS_IDENTIFIERS)

    # Initialize graph, and create object
    graph = SimpleGraph()
    resource = model(graph, identifier=identifier)

    return resource


# TODO: Makes sense to still have this function?
def check_elements(
    collection: Alt | Bag | List | Seq,
    element_list: list[Any],
    element_set: Optional[list[Any]] = None,
):
    """
    Check whether collection_elements is the appropriate representation of
    element_list, given the type of Collection object.
    """

    # If Collection object is an Alt or a Bag
    if isinstance(collection, (Alt, Bag)):
        # It it is an Alt, remove duplicates from element list
        if isinstance(collection, Alt):
            if element_set is None:
                element_set = []
                for element in element_list:
                    if not any(
                        element == el
                        and isinstance(element, type(el))
                        and isinstance(el, type(element))
                        for el in element_set
                    ):
                        element_set.append(element)
            element_list = element_set

        # Check that there are as many elements in Collection object as in list
        assert len(collection.elements) == len(element_list)
        # Check that all elements in list also appear in Collection
        assert all(element in collection.elements for element in element_list)

    # Otherwise, if object is a List or a Seq
    else:
        # Check that the list of elements from Collection is the same as list
        assert list(collection.elements) == list(element_list)


def check_method(
    resource: Resource,
    method: Callable,
    args: tuple = (),
    kwargs: Optional[dict] = None,
    triples_add: Optional[list[tuple]] = None,
    triples_rem: Optional[list[tuple]] = None,
    with_graph: bool = False,
    graph: Optional[SimpleGraph | MultiGraph] = None,
) -> None:
    """Check call to a Resource's method."""

    # Initialize kwargs
    if kwargs is None:
        kwargs = {}

    # Freeze the state of the graph before calling the method
    resource_graph_before = copy.deepcopy(resource.graph)

    # If testing with the "graph" kwarg
    if with_graph:
        # If no graph is specified
        if graph is None:
            # Create a new, separate graph
            graph = SimpleGraph()

        # Freeze the state of the graph before calling the method
        graph_before = copy.deepcopy(graph)

        # Add graph to kwargs
        kwargs["graph"] = graph

    # Otherwise, use Resource's graph
    else:
        graph = resource.graph
        graph_before = resource_graph_before

    # Call the method
    method(*args, **kwargs)

    # If testing with the "graph" kwarg
    if with_graph:
        # Check that Resource's graph did not change
        assert set(resource.graph) == set(resource_graph_before)

    # If no removed triples are specified
    if triples_rem is None:
        triples_rem = []
    # If no additional triples are specified
    if triples_add is None:
        triples_add = []

    # Check the correctness of the removed and additional triples
    check_rem_add(graph_before, graph, triples_rem, triples_add)


def check_str(
    instance: Resource,
    model_name: str,
    identifier: str,
    namespace: str = ":",
    sep: str = "#",
) -> None:
    """Check the string representation of the resource instance."""
    assert str(instance) == f"{namespace}/{model_name}{sep}{identifier}"


def get_another_parameter(
    parameter_list: list[Any],
    parameter: Optional[Any] = None,
    key: Optional[Callable] = None,
) -> Any:
    """Returns another parameter from the list."""

    # If no key function is specified
    if key is None:
        # Use mere difference between parameters
        key = lambda new_parameter: new_parameter != parameter

    # Iterate over all the parameters of the list
    for new_parameter in parameter_list:
        # If the new parameter is different from parameter, return it
        if key(new_parameter):
            return new_parameter

    # If no other parameter could be found in the list, raise an error
    raise ValueError("Could not get another parameter from the list")


def get_default_alternatives(
    element_list_with_check: list[tuple[IRI | Literal | Any, IRI | Literal]],
) -> tuple[Optional[IRI | Literal | Any], list[IRI | Literal | Any]]:
    """Get default and alternatives from list of elements."""

    # If list is empty
    if not element_list_with_check:
        # Default is None, and alternatives is an empty list
        return None, []

    # Get default and alternatives
    default_with_check, *alternatives_with_check = element_list_with_check

    # Remove duplicated alternatives, and remove default if it appears among
    # them
    alternatives_with_check = set(alternatives_with_check)
    alternatives_with_check.discard(default_with_check)

    # Parse default and alternatives with check
    default, default_check = default_with_check
    alternatives, alternatives_check = parse_element_list_with_check(
        alternatives_with_check
    )

    return default_check, alternatives_check


def index_exact_match(
    element: IRI | Literal | Any, element_list: list[IRI | Literal | Any]
) -> Optional[int]:
    """
    Get the index of element in a list, using exact matching
    (eg. 0 != 0.0 != False).
    """

    # For every element of list
    for i, el in enumerate(element_list):
        # If it matches element exactly
        if (
            element == el
            and isinstance(element, type(el))
            and isinstance(el, type(element))
        ):
            # Return corresponding index
            return i

    # If not found, return None
    return None
