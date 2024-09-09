"""Useful functions for testing"""

import itertools
from typing import Any, Optional

from rdflib import RDF, Literal, Namespace
from rdflib import URIRef as IRI

from rdflib_plus import MultiGraph, Resource, SimpleGraph

SEED = 1


def build_iri(
    identifier: str,
    namespace: Optional[Namespace | str] = None,
    path_joined: str = "",
    sep: str = "#",
    model_name: Optional[str] = "Resource",
):
    """Build resource IRI."""

    # If needed, set default namespace
    namespace = (
        "http://default.example.com" if namespace is None else str(namespace)
    )

    # Concatenate elements
    iri = namespace
    if path_joined:
        iri += "/" + path_joined
    if model_name is not None:
        iri += "/" + model_name
    iri += sep + identifier

    return IRI(iri)


def cartesian_product(*args) -> list[list]:
    """Return cartesian product of multiple lists."""

    return [
        list(
            itertools.chain(
                *[
                    element if isinstance(element, tuple) else [element]
                    for element in combination
                ]
            )
        )
        for combination in itertools.product(*args)
    ]


def check_attributes(resource: Resource, **kwargs):
    """Check attribute values of resource."""

    # For every attribute-value pair
    for attribute, value in kwargs.items():
        # Check that resource has attribute
        assert hasattr(resource, attribute)
        print(resource, attribute)
        print(
            getattr(resource, attribute) == value,
            getattr(resource, attribute),
            type(getattr(resource, attribute)),
            value,
            type(value),
        )
        print("------------------")

        # Check that attribute has the right value
        assert getattr(resource, attribute) == value


def check_graph_triples(
    graph: SimpleGraph | MultiGraph,
    triples: list[tuple[IRI, IRI, IRI]],
):
    """Check that graph is equivalent to the specified set of triples."""
    print("TRIPLES IN GRAPH")
    for triple in graph:
        print(triple)
    print("----------")

    # For every triple
    for triple in triples:
        # Check that it appears in graph
        print(triple in graph, triple)
        assert triple in graph

    # Check that graph is exactly the set of triples
    assert len(graph) == len(triples)


def check_graph_unordered_collection(
    subject_iri: IRI,
    graph: SimpleGraph | MultiGraph,
    predicates: list[IRI],
    objects: list[IRI | Literal],
    triples: Optional[list[tuple[IRI, IRI, IRI | Literal]]] = None,
    exact: bool = True,
) -> None:
    """
    Check if graph contains every predicate and every object, as well as every
    triple (if any specified) -- and nothing else.
    """

    # If no triples were specified, turn it into empty list
    if triples is None:
        triples = []

    # For every triple in graph
    for triple in graph:
        # If triple was specified
        if triple in triples:
            # Remove it to make sure it only appears once,
            # then go to the next triple
            triples.remove(triple)
            continue

        # Parse triple
        subject, predicate, object_ = triple

        # Make sure the subject is Collection
        assert subject == subject_iri
        # Remove predicate and object to make sure they only appear once in
        # the lists
        predicates.remove(predicate)
        objects.remove(object_)

    # Make sure all the triples, predicates and objects specified were in graph
    assert not triples
    if exact:
        assert not predicates
        assert not objects


def remove_rem_add_triples(
    triples_rem: list[tuple[IRI, IRI, IRI | Literal]],
    triples_add: list[tuple[IRI, IRI, IRI | Literal]],
) -> tuple[
    list[tuple[IRI, IRI, IRI | Literal]], list[tuple[IRI, IRI, IRI | Literal]]
]:
    """Remove triples that were both removed and added."""
    return (
        list(set(triples_rem).difference(triples_add)),
        list(set(triples_add).difference(triples_rem)),
    )


def check_graph_diff_unordered_collection(
    graph_before: SimpleGraph | MultiGraph,
    graph_after: SimpleGraph | MultiGraph,
    subject_iri: IRI,
    predicates_rem: list[IRI],
    predicates_add: list[IRI],
    objects_rem: list[IRI | Literal],
    objects_add: list[IRI | Literal],
    triples_rem: Optional[list[tuple[IRI, IRI, IRI]]] = None,
    triples_add: Optional[list[tuple[IRI, IRI, IRI]]] = None,
):
    """
    Check that the removed and additional predicates and objects are correct.
    """

    # If no triples were specified, turn it into empty list
    if triples_rem is None:
        triples_rem = []
    if triples_add is None:
        triples_add = []

    # Remove triples that were both removed and added
    triples_rem, triples_add = remove_rem_add_triples(triples_rem, triples_add)

    # Check that the expected triples, predicates and objects (and only them)
    # were indeed removed from the graph
    check_graph_unordered_collection(
        subject_iri,
        graph_before - graph_after,
        predicates_rem,
        objects_rem,
        triples=triples_rem,
        exact=False,
    )

    # Check that the expected triples, predicates and objects (and only them)
    # were indeed added to the graph
    check_graph_unordered_collection(
        subject_iri,
        graph_after - graph_before,
        predicates_add,
        objects_add,
        triples=triples_add,
        exact=False,
    )

    # Make sure the remaining predicates and objects (which have been removed
    # then added back) are the same
    assert set(predicates_rem) == set(predicates_add) and len(
        predicates_rem
    ) == len(predicates_add)
    assert set(objects_rem) == set(objects_add) and len(objects_rem) == len(
        objects_add
    )


def check_graph_list(
    list_iri: IRI,
    element_list: list[Any],
    graph: SimpleGraph | MultiGraph,
    triples: Optional[list[tuple[IRI, IRI, IRI | Literal]]] = None,
    is_new_list: bool = True,
) -> None:
    """
    Check if graph contains a list containing every object, as well as every
    triple (if any specified) -- and nothing else.
    """

    # If no triples were specified, initialize it as empty list
    if triples is None:
        triples = []

    # If element list is not empty
    if element_list:

        # For every element in the list
        for i, element in enumerate(element_list):

            # If sublist, or if explicitly required
            if i > 0 or is_new_list:
                # Add type triple
                triples.append((list_iri, RDF.type, RDF.List))

            # Get sublist or RDF.nil, and add the related triples
            object_ = graph.value(list_iri, RDF.rest)
            triples.extend(
                [
                    (list_iri, RDF.first, element),
                    (list_iri, RDF.rest, object_),
                ]
            )

            # Use object_ as subject
            list_iri = object_

    # Otherwise, if list just got initialized, add its type triple
    elif is_new_list:
        triples.append((list_iri, RDF.type, RDF.List))

    # Check graph triples
    check_graph_triples(graph, triples)


def check_rem_add(
    graph_before: SimpleGraph | MultiGraph,
    graph_after: SimpleGraph | MultiGraph,
    triples_rem: list[tuple[IRI, IRI, IRI]],
    triples_add: list[tuple[IRI, IRI, IRI]],
):
    """Check that the removed and additional triples are correct."""

    # Remove triples that were both removed and added
    triples_rem, triples_add = remove_rem_add_triples(triples_rem, triples_add)

    # Check that the removed triples are correct
    check_graph_triples(graph_before - graph_after, triples_rem)
    # Check that the added triples are correct
    check_graph_triples(graph_after - graph_before, triples_add)


def get_label(
    camel_case: bool,
    pascal_case: bool,
    label: str,
    legal_label: str,
    label_camel_case: str,
    legal_label_camel_case: str,
    label_pascal_case: str,
    legal_label_pascal_case: str,
) -> tuple[str, str, str]:
    """Get necessary labels for resource object creation."""

    # Get appropriate label
    if camel_case or pascal_case:
        if camel_case:
            label = label_camel_case
            legal_label = legal_label_camel_case
        else:
            label = label_pascal_case
            legal_label = legal_label_pascal_case
        sep = "/"
    else:
        sep = "#"

    return (label, legal_label, sep)
