"""Useful functions for testing"""

import itertools
from typing import Any, Optional

from rdflib import RDF, Graph, Literal, Namespace
from rdflib import URIRef as IRI

from rdflib_plus import Alt, Bag, List, MultiGraph, Resource, Seq, SimpleGraph

# Set random seed
SEED = 1

# Set warning messages
WARNING_MESSAGE_ALT_COUNT = (
    "Calling Alt's 'count()' method does not make sense, as Alt does not "
    "allow duplicated values. Prefer using the 'in' operator instead."
)
WARNING_MESSAGE_DEFAULT = r"Using element '.+' as default\."
WARNING_MESSAGE_DEFAULT_REMOVED = (
    "Default element removed. New default set to '{}'."
)

WARNING_MESSAGE_DUPLICATES = (
    r"Trying to set new alternative '.+' to Alt, but it is "
    r"already (?:its default element|in Alt)\. "
    r"Not adding it again\."
)
WARNING_MESSAGE_FORMATTING = "Formatting identifier '{}' into '{}'."
WARNING_MESSAGE_SET_OVERWRITE = (
    "Overwriting value of (unique) attribute with predicate '{}', "
    "from '{}' to '{}' in graph '{}'."
)
WARNING_MESSAGE_VERSION = (
    "Version number '{}' is not in the appropriate format. Setting it anyway."
)


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
    graph: Graph,
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
    collection: Alt | Bag,
    objects: list[IRI | Literal],
    type_: Optional[IRI] = None,
    default: Optional[IRI | Literal] = None,
    graph_diff: Optional[SimpleGraph | MultiGraph] = None,
) -> None:
    """
    Check if graph contains every predicate and every object of collection,
    as well as every triple (if any specified) -- and nothing else.
    """

    # Deep copy list, as their elements are going to be removed
    objects = objects.copy()

    # Initialize exact triples to look for in the graph
    triples = []
    if type_ is not None:
        triples.append((collection.iri, RDF.type, type_))
    if default is not None:
        triples.append((collection.iri, RDF["_1"], default))

    # Prepare predicates
    shift = 0 if default is None else 1
    predicates = [RDF[f"_{i + 1}"] for i in range(shift, shift + len(objects))]

    # Get graph, in particular get the difference with other graph
    # (if any specified)
    graph = collection.graph
    if graph_diff is not None:
        graph -= graph_diff

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
        assert subject == collection.iri
        # Remove predicate and object to make sure they only appear once in
        # the lists
        predicates.remove(predicate)
        objects.remove(object_)

    # Make sure all the triples, predicates and objects specified were in graph
    assert not triples
    assert not predicates
    assert not objects


def check_graph_alt(
    alt: Alt,
    objects: list[IRI | Literal],
    default: Optional[IRI | Literal] = None,
    graph_diff: Optional[SimpleGraph | MultiGraph] = None,
) -> None:
    """
    Check if graph contains every predicate and every object of Alt,
    as well as every triple (if any specified) -- and nothing else.
    """
    check_graph_unordered_collection(
        alt, objects, type_=RDF.Alt, default=default, graph_diff=graph_diff
    )


def check_graph_bag(
    bag: Bag,
    objects: list[IRI | Literal],
    graph_diff: Optional[SimpleGraph | MultiGraph] = None,
) -> None:
    """
    Check if graph contains every predicate and every object of Bag,
    as well as every triple (if any specified) -- and nothing else.
    """
    check_graph_unordered_collection(
        bag, objects, type_=RDF.Bag, graph_diff=graph_diff
    )


def check_graph_list(
    list_: List,
    objects: list[IRI | Literal],
    graph_diff: Optional[SimpleGraph | MultiGraph] = None,
    is_new_list: bool = True,
) -> None:
    """
    Check if graph contains a list containing every object, as well as every
    triple (if any specified) -- and nothing else.
    """

    # Get graph, in particular get the difference with other graph
    # (if any specified)
    graph = list_.graph
    if graph_diff is not None:
        graph -= graph_diff

    # Initialize first subject, and triples list
    subject = list_.iri

    # If objects were specified
    triples = []
    if objects:

        # For every element in the list
        for i, object_ in enumerate(objects):

            # If sublist or if required, add type triple
            if i > 0 or is_new_list:
                triples.append((subject, RDF.type, RDF.List))

            # Get sublist or RDF.nil, and add the related triples
            rest = graph.value(subject, RDF.rest)
            triples.extend(
                [
                    (subject, RDF.first, object_),
                    (subject, RDF.rest, rest),
                ]
            )

            # Use object_ as subject
            subject = rest

        # Check that last rest is RDF.nil
        assert rest == RDF.nil

    # Otherwise and if required, add type triple
    elif is_new_list:
        triples.append((subject, RDF.type, RDF.List))

    # Check graph triples
    check_graph_triples(graph, triples)


def check_graph_seq(
    seq: Seq,
    objects: list[IRI | Literal],
    type_: Optional[IRI] = None,
    graph_diff: Optional[SimpleGraph | MultiGraph] = None,
) -> None:
    """
    Check if graph contains a seq containing every object, as well as every
    triple (if any specified) -- and nothing else.
    """

    # Prepare the triples to look for in the graph
    triples = [
        (seq.iri, RDF[f"_{i + 1}"], object_)
        for i, object_ in enumerate(objects)
    ]

    # Add the type triple
    triples.append((seq.iri, RDF.type, type_))

    # Get graph, in particular get the difference with other graph
    # (if any specified)
    graph = seq.graph
    if graph_diff is not None:
        graph -= graph_diff

    # Check graph triples
    check_graph_triples(graph, triples)


def check_graph_collection(
    collection: Alt | Bag | List | Seq, objects: list[IRI | Literal], **kwargs
) -> None:
    """
    Check if graph contains a Collection containing every object,
    as well as every triple (if any specified) -- and nothing else.
    """

    # If collection is an Alt
    if isinstance(collection, Alt):
        check_graph_alt(collection, objects, **kwargs)

    # Otherwise, if collection is a Bag
    elif isinstance(collection, Bag):
        check_graph_bag(collection, objects, **kwargs)

    # Otherwise, if collection is a List
    elif isinstance(collection, List):
        check_graph_list(collection, objects, **kwargs)

    # Otherwise, if collection is a Seq
    elif isinstance(collection, Seq):
        check_graph_seq(collection, objects, **kwargs)

    # Otherwise, raise error
    else:
        raise TypeError


def check_elements_unordered_collection(
    collection: Alt | Bag, elements: list[IRI | Literal]
) -> None:
    """Check that collection contains every element -- and nothing else."""
    assert len(collection) == len(elements)
    assert all(el in collection for el in elements)


def check_elements_ordered_collection(
    collection: List | Seq, elements: list[IRI | Literal]
) -> None:
    """Check that collection element list is equal to elements."""
    assert len(collection) == len(elements)
    assert all(
        element == list_element
        for element, list_element in zip(elements, collection)
    )


def check_elements(
    collection: Alt | Bag | List | Seq,
    elements: list[IRI | Literal],
) -> None:
    """
    Check that collection appropriately contains the elements
    -- and nothing else.
    """

    # If collection is unordered
    if isinstance(collection, (Alt, Bag)):
        check_elements_unordered_collection(collection, elements)

    # Otherwise, if collection is ordered
    elif isinstance(collection, (List, Seq)):
        check_elements_ordered_collection(collection, elements)

    # Otherwise, raise error
    else:
        raise TypeError


def check_graph_diff(
    graph_before: Graph,
    graph_after: Graph,
    triples_rem: list[tuple[IRI, IRI, IRI]],
    triples_add: list[tuple[IRI, IRI, IRI]],
):
    """Check that the removed and additional triples are correct."""

    # Remove triples that were both removed and added
    triples_rem, triples_add = (
        list(set(triples_rem).difference(triples_add)),
        list(set(triples_add).difference(triples_rem)),
    )

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

    return label, legal_label, sep


def remove_duplicated_elements(
    elements: list[IRI | Literal | Any],
    elements_check: list[IRI | Literal],
) -> tuple[list[IRI | Literal | Any], list[IRI | Literal]]:
    """Remove duplicated elements from list, using their formatted form."""

    element_set, element_set_check = [], []

    for i, (element, element_check) in enumerate(
        zip(elements, elements_check)
    ):
        if element_check not in elements_check[:i]:
            element_set.append(element)
            element_set_check.append(element_check)

    return element_set, element_set_check
