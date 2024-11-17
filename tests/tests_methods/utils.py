"""Useful functions for testing methods"""

import copy
import random as rd
from typing import Any, Callable, Optional

from rdflib import RDF, Graph, Literal
from rdflib import URIRef as IRI

from rdflib_plus import Alt, Bag, Class, List, Resource, Seq, SimpleGraph
from tests.parameters import PARAMETERS_ELEMENT_LISTS, PARAMETERS_IDENTIFIERS
from tests.utils import check_graph_diff


def build_collection(
    type_: type,
    graph: Optional[Graph] = None,
    not_empty: bool = False,
    **kwargs,
) -> tuple[
    Alt | Bag | List | Seq,
    list[IRI | Literal | Any],
    list[IRI | Literal],
]:
    """Build Collection object from (random) element list."""

    # Randomly select list of elements
    elements, elements_check = rd.choice(PARAMETERS_ELEMENT_LISTS)

    # If specified, make sure that element list is not empty
    if not_empty:
        while len(elements) == 0:
            elements, elements_check = rd.choice(PARAMETERS_ELEMENT_LISTS)

    # If no graph is specified, initialize one
    if graph is None:
        graph = SimpleGraph()

    # Create object
    collection = type_(graph, elements=elements, **kwargs)

    return collection, elements, elements_check


def build_object(
    graph: Graph,
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
    graph: Graph,
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


def check_method(
    resource: Resource,
    method: Callable,
    args: tuple = (),
    kwargs: Optional[dict] = None,
    triples_add: Optional[list[tuple]] = None,
    triples_rem: Optional[list[tuple]] = None,
    with_graph: bool = False,
    graph: Optional[Graph] = None,
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
    check_graph_diff(graph_before, graph, triples_rem, triples_add)


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
    elements: list[IRI | Literal | Any],
) -> tuple[Optional[IRI | Literal | Any], list[IRI | Literal | Any]]:
    """Get default and alternatives from list of elements."""

    # If list is empty
    if not elements:
        # Default is None, and alternatives is an empty list
        return None, []

    # Get default and alternatives
    default, *alternatives = elements

    return default, alternatives


def count_exact_match(
    element: IRI | Literal | Any, elements: list[IRI | Literal | Any]
) -> int:
    """
    Count the number of times element appear in a list, using exact matching
    (eg. 0 != 0.0 != False).
    """
    return sum(
        (
            element == el
            and isinstance(element, type(el))
            and isinstance(el, type(element))
        )
        for el in elements
    )


def index_exact_match(
    element: IRI | Literal | Any,
    elements: list[IRI | Literal | Any],
    start: int = 0,
    end: int = -1,
) -> Optional[int]:
    """
    Get the index of element in a list, using exact matching
    (eg. 0 != 0.0 != False).
    """

    # Format start and end indices
    n = len(elements)
    if start < 0:
        start += n
    if end < 0:
        end += n

    # For every element of list
    for i, el in enumerate(elements[start : end + 1]):

        # If it matches element exactly, return the corresponding index
        if (
            element == el
            and isinstance(element, type(el))
            and isinstance(el, type(element))
        ):
            return i + start

    # If not found, return None
    return None
