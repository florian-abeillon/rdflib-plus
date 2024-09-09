"""Useful functions for testing constructors"""

from typing import Any, Optional

from rdflib import DCTERMS, RDF, SKOS, Literal, Namespace
from rdflib import URIRef as IRI

from rdflib_plus import MultiGraph, Resource, SimpleGraph
from tests.utils import build_iri, check_attributes, check_graph_triples


def check_init(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    blank_node: bool = False,
    identifier: Optional[Literal] = None,
    legal_identifier: Optional[str] = None,
    kwargs: Optional[dict] = None,
    namespace: Optional[Namespace] = None,
    sep: str = "#",
    identifier_property: IRI = DCTERMS.identifier,
    label: Optional[Literal] = None,
    path: Optional[list[str]] = None,
    add_path: Optional[list[str]] = None,
    path_joined: str = "",
    triples_add: Optional[list[tuple[IRI, Any]]] = None,
    type_in_iri: bool = True,
    check_triples: bool = True,
) -> Resource:
    """Test object creation."""

    # Initialize graph, and create object
    graph = MultiGraph() if namespace is not None else SimpleGraph()
    if kwargs is None:
        kwargs = {}
    print("KWARGS", kwargs)
    resource = model(graph, **kwargs)

    # print(graph.serialize())

    # Set list of additional triples
    if triples_add is None:
        triples_add = []
    if label is not None:
        triples_add.append((SKOS.prefLabel, label))

    # If blank node object
    if blank_node:
        # Check IRI and id
        assert isinstance(resource.iri, IRI)
        iri = resource.iri
        assert isinstance(resource.id, str)
        identifier = resource.id

        # Set path and identifier_property, to check
        path = [model_name]
        identifier_property = DCTERMS.identifier

    else:
        # Build IRI from elements
        model_name = model_name if type_in_iri else None
        iri = build_iri(
            legal_identifier,
            namespace=namespace,
            model_name=model_name,
            path_joined=path_joined,
            sep=sep,
        )

        # Add additional triple
        triples_add.append((identifier_property, identifier))

        # Set path and identifier, to check
        if path is None:
            path = []
        if type_in_iri:
            path.append(model_name)
        if add_path is not None:
            path.extend(add_path)
        identifier = identifier.value

    # Check attributes
    check_attributes(
        resource,
        iri=iri,
        id=identifier,
        path=path,
        identifier_property=identifier_property,
        type=model_type,
        properties=properties,
    )

    # If necessary
    if check_triples:
        # Define triples to look for
        triples = [
            (
                iri,
                RDF.type,
                model_type,
            ),
        ]
        for p, o in triples_add:
            triples.append((iri, p, o))

        # Check that all triples are in the graph
        check_graph_triples(graph, triples)

    return resource


def check_init_labeled_object(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    identifier: Literal,
    legal_identifier: str,
    kwargs: Optional[dict] = None,
    namespace: Optional[Namespace] = None,
    sep: str = "#",
    identifier_property: IRI = DCTERMS.identifier,
    label: Optional[Literal] = None,
    path: Optional[list[str]] = None,
    add_path: Optional[list[str]] = None,
    path_joined: str = "",
    triples_add: Optional[list[tuple[IRI, Any]]] = None,
    type_in_iri: bool = True,
    check_triples: bool = True,
) -> Resource:
    """Test labeled object creation."""

    return check_init(
        model,
        model_name,
        model_type,
        properties,
        blank_node=False,
        identifier=identifier,
        legal_identifier=legal_identifier,
        kwargs=kwargs,
        namespace=namespace,
        sep=sep,
        identifier_property=identifier_property,
        label=label,
        path=path,
        add_path=add_path,
        path_joined=path_joined,
        triples_add=triples_add,
        type_in_iri=type_in_iri,
        check_triples=check_triples,
    )


def check_init_blank_node_object(
    model: type,
    model_name: str,
    model_type: IRI,
    properties: set[IRI],
    kwargs: Optional[dict] = None,
    namespace: Optional[Namespace] = None,
    path: Optional[list[str]] = None,
    add_path: Optional[list[str]] = None,
    path_joined: str = "",
    triples_add: Optional[list[tuple[IRI, Any]]] = None,
    check_triples: bool = True,
) -> Resource:
    """Test blank node object creation."""

    return check_init(
        model,
        model_name,
        model_type,
        properties,
        blank_node=True,
        kwargs=kwargs,
        namespace=namespace,
        path=path,
        add_path=add_path,
        path_joined=path_joined,
        triples_add=triples_add,
        check_triples=check_triples,
    )


def get_element_set(
    element_list: list[IRI | Literal | Any],
    element_list_check: list[IRI | Literal],
) -> tuple[list[IRI | Literal | Any, IRI | Literal]]:
    """Remove duplicated elements from list, using their formatted form."""

    # Initialize sets
    element_set = []
    element_set_check = []

    # For every element
    for i, (el, el_check) in enumerate(zip(element_list, element_list_check)):
        # If element was not already encountered
        if el_check not in element_list_check[:i]:
            # Add it and its formatted form to the sets
            element_set.append(el)
            element_set_check.append(el_check)

    return element_set, element_set_check
