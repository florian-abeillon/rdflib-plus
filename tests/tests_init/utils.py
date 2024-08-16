"""Useful functions for testing constructors"""

import re
from copy import deepcopy
from typing import Any, Optional

from rdflib import DCTERMS, RDF, SKOS, XSD, Literal, Namespace
from rdflib import URIRef as IRI

from rdflib_plus import MultiGraph, Resource, SimpleGraph
from tests.parameters import PARAMETERS_ALT
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
    add_triples: Optional[list[tuple[IRI, Any]]] = None,
    type_in_iri: bool = True,
    check_triples: bool = True,
) -> tuple[SimpleGraph | MultiGraph, Resource]:
    """Test object creation."""

    # Initialize graph, and create object
    graph = MultiGraph() if namespace is not None else SimpleGraph()
    if kwargs is None:
        kwargs = {}
    print("KWARGS", kwargs)
    resource = model(graph, **kwargs)

    # print(graph.serialize())

    # Set list of additional triples
    if add_triples is None:
        add_triples = []
    if label is not None:
        add_triples.append((SKOS.prefLabel, label))

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
        add_triples.append((identifier_property, identifier))

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
        for p, o in add_triples:
            triples.append((iri, p, o))

        # Check that all triples are in the graph
        check_graph_triples(graph, triples, exact=True)

    return graph, resource


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
    add_triples: Optional[list[tuple[IRI, Any]]] = None,
    type_in_iri: bool = True,
    check_triples: bool = True,
) -> tuple[SimpleGraph | MultiGraph, Resource]:
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
        add_triples=add_triples,
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
    add_triples: Optional[list[tuple[IRI, Any]]] = None,
    check_triples: bool = True,
) -> tuple[SimpleGraph | MultiGraph, Resource]:
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
        add_triples=add_triples,
        check_triples=check_triples,
    )


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


def format_elements(
    elements: list[IRI | Literal | Any],
) -> list[IRI | Literal]:
    """Turn elements into Literals."""

    # Initialize formatted element list
    elements_formatted = []

    # For every element
    for element in elements:
        # If it is not an IRI nor a Literal
        if not isinstance(element, (Literal, IRI)):
            # Set them as Literals of adequate datatype
            datatype = (
                XSD.string
                if isinstance(element, str)
                else (
                    XSD.boolean
                    if isinstance(element, bool)
                    else (
                        XSD.integer if isinstance(element, int) else XSD.double
                    )
                )
            )
            element = Literal(element, datatype=datatype)

        # Add formatted element to the list
        elements_formatted.append(element)

    return elements_formatted


def check_container_predicates(
    elements: list[IRI | Literal | Any],
    graph: SimpleGraph | MultiGraph,
    resource: Resource,
) -> None:
    """Check that elements are related to resource with
    appropriate properties."""

    # For each element
    for element in set(elements):
        # For each triple that connects it to the collection object
        for s, p, o in graph.triples((resource.iri, None, element)):
            # Check that predicate has the appropriate format
            assert isinstance(p, IRI)
            assert p.defrag() + "#" == IRI(RDF)
            assert re.match(r"\_\d+", p.fragment)


def check_elements(
    resource: Resource,
    elements: list[IRI | Literal],
) -> None:
    """Check Collection's "elements" attribute."""

    # Check that Collection has "element" attribute
    assert hasattr(resource, "elements")
    resource_elements = getattr(resource, "elements")

    # Check that Collection's "element" attribute has the appropriate
    # number of elements
    assert len(resource_elements) == len(elements)

    # For each element in the list
    for element in elements:
        # Check that it is in Collection's "element" attribute
        assert element in resource_elements


def check_init_alt(
    default: Optional[IRI | Literal | Any],
    alternatives: list[IRI | Literal | Any],
) -> None:
    """Test Alt creation."""

    # Set kwargs to be used by constructor
    # alternatives.copy() as alternatives are mutable
    kwargs = {"default": default, "alternatives": deepcopy(alternatives)}

    # Format elements
    element_list = []
    if default is not None:
        element_list.append(default)
    if alternatives is not None:
        element_list.extend(alternatives)
    elements = format_elements(element_list)
    add_triples = [(None, element) for element in elements]

    # Test constructor
    graph, resource = check_init_blank_node_object(
        *PARAMETERS_ALT,
        kwargs=kwargs,
        add_triples=add_triples,
    )

    # Check Alt's "elements" attribute
    check_elements(resource, element_list)

    # Check default element
    assert hasattr(resource, "default")
    if default is not None:
        assert getattr(resource, "default") == default
    elif alternatives is not None and len(alternatives) > 0:
        assert getattr(resource, "default") in alternatives
    else:
        assert getattr(resource, "default") is None

    # Check that elements are related to resource with appropriate properties
    check_container_predicates(elements, graph, resource)
