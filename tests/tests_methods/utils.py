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
from tests.utils import check_graph_triples


def build_alt(element_list: Optional[list[IRI | Literal | Any]] = None) -> Alt:
    """Build Alt from element list."""

    # If no element list is specified
    if element_list is None:
        # Randomly select list of elements
        element_list = rd.choice(PARAMETERS_ELEMENT_LISTS)

    # Initialize graph
    graph = SimpleGraph()

    # Create Alt
    if element_list:
        default, *alternatives = element_list
        alt = Alt(graph, default=default, alternatives=alternatives)
    else:
        alt = Alt(graph)

    return alt


def build_collection(
    model: type, element_list: Optional[list[IRI | Literal | Any]] = None
) -> Alt | Bag | List | Seq:
    """Build Collection object from (random) element list."""

    # If no element list is specified
    if element_list is None:
        # Randomly select list of elements
        element_list = rd.choice(PARAMETERS_ELEMENT_LISTS)

    # If model is Alt, create an Alt
    if model == Alt:
        return build_alt(element_list=element_list)

    # Initialize graph, and create object
    graph = SimpleGraph()
    return model(graph, elements=element_list)


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


def check_elements(
    model: type,
    collection_elements: list[Any],
    element_list: list[Any],
    element_set: Optional[list[Any]] = None,
):
    """
    Check whether collection_elements is the appropriate representation of
    element_list, given the type of Collection object.
    """

    # If Collection object is an Alt or a Bag
    if model in [Alt, Bag]:
        # It it is an Alt, remove duplicates from element list
        if model == Alt:
            element_list = (
                set(element_list) if element_set is None else element_set
            )

        # Check that there are as many elements in Collection object as in list
        assert len(collection_elements) == len(element_list)
        # Check that all elements in list also appear in Collection
        assert all(element in collection_elements for element in element_list)

    # Otherwise, if object is a List or a Seq
    else:
        # Check that the list of elements from Collection is the same as list
        assert list(collection_elements) == list(element_list)


def check_method(
    resource: Resource,
    method: Callable,
    args: tuple = (),
    kwargs: Optional[dict] = None,
    add_triples: Optional[list[tuple]] = None,
    rem_triples: Optional[list[tuple]] = None,
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

    # If additional triples are specified
    if add_triples is not None:

        # Get the additional triples due to the call to the method
        graph_add = graph - graph_before

        # Check that all triples were added to the graph
        check_graph_triples(graph_add, add_triples, exact=True)

    # If removed triples are specified
    if rem_triples is not None:

        # Get the triples removed by the call to the method
        graph_rem = graph_before - graph

        # Check that all triples were removed from the graph
        check_graph_triples(graph_rem, rem_triples, exact=True)


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


def parse_element_list_with_check(
    element_list_with_check: list[tuple[IRI | Literal | Any, IRI | Literal]]
) -> tuple[list[IRI | Literal | Any, IRI | Literal]]:
    """Parse lists of elements with check."""

    if not element_list_with_check:
        return [], []
    return tuple(zip(*element_list_with_check))


def prepare_list_triples_for_check(
    s: IRI,
    element_list: list[Any],
    graph: SimpleGraph | MultiGraph,
) -> list[tuple[IRI, IRI, IRI]]:
    """Prepare the triples from List, for graph check."""

    # If list is empty, return empty list
    if not element_list:
        return []

    # Create an iterator over the elements
    element_iter = iter(element_list)

    # Get the first object, and initialize triples
    o = graph.value(s, RDF.rest)
    triples = [
        (s, RDF.first, next(element_iter)),
        (s, RDF.rest, o),
    ]

    # As long as the list is not finished
    while o != RDF.nil:
        # Add triple
        triples.append((o, RDF.type, RDF.List))

        # Use o as subject
        s = o

        # Get its object with regard to RDF.rest, and add the related triples
        o = graph.value(s, RDF.rest)
        triples.extend(
            [
                (s, RDF.first, next(element_iter)),
                (s, RDF.rest, o),
            ]
        )

    return triples
