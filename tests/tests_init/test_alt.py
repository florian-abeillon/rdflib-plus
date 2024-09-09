"""Test Alt constructor"""

from typing import Any

import pytest
from rdflib import RDF, Literal
from rdflib import URIRef as IRI

from tests.parameters import (
    PARAMETERS_ALT,
    PARAMETERS_ELEMENT_LISTS,
    PARAMETERS_ELEMENTS,
)
from tests.tests_init.utils import (
    check_init_blank_node_object,
    get_element_set,
)
from tests.utils import (
    cartesian_product,
    check_graph_triples,
    check_graph_unordered_collection,
)


@pytest.mark.parametrize("element, element_check", PARAMETERS_ELEMENTS)
def test_init_with_default(
    element: IRI | Literal | Any, element_check: IRI | Literal
):
    """Test Alt creation with default element."""

    # Set kwargs to be used by constructor
    kwargs = {"default": element}

    # Test constructor
    alt = check_init_blank_node_object(
        *PARAMETERS_ALT,
        kwargs=kwargs,
        check_triples=False,
    )

    # Check default, alternatives and elements properties
    assert alt.default == element
    assert alt.alternatives == []
    assert alt.elements == [element]

    # Check that the expected triples (and only them) were indeed added to the
    # graph
    triples = [
        (alt.iri, RDF.type, RDF.Alt),
        (alt.iri, RDF["_1"], element_check),
    ]
    check_graph_triples(alt.graph, triples)


@pytest.mark.parametrize(
    "element_list, element_list_check", PARAMETERS_ELEMENT_LISTS
)
def test_init_with_alternatives(
    element_list: list[IRI | Literal | Any],
    element_list_check: list[IRI | Literal],
):
    """Test Alt creation with alternative elements."""

    # Set kwargs to be used by constructor
    kwargs = {"alternatives": element_list}

    # Test constructor
    alt = check_init_blank_node_object(
        *PARAMETERS_ALT,
        kwargs=kwargs,
        check_triples=False,
    )

    # Check default, alternatives and elements properties
    element_set, element_set_check = get_element_set(
        element_list, element_list_check
    )
    if not element_list:
        assert alt.default is None
        assert alt.alternatives == []
        assert alt.elements == []
    else:
        # assert alt.default == element_list[0]
        assert all(element in alt.elements for element in element_set)
        assert len(alt.elements) == len(element_set)

    # Check that the expected triples, predicates and objects (and only them)
    # were indeed added to the graph
    triples = [(alt.iri, RDF.type, RDF.Alt)]
    predicates = [RDF[f"_{i + 1}"] for i in range(len(element_set_check))]
    objects = element_set_check
    check_graph_unordered_collection(
        alt.iri,
        alt.graph,
        predicates,
        objects,
        triples=triples,
        exact=True,
    )


@pytest.mark.parametrize(
    "element, element_check, element_list, element_list_check",
    cartesian_product(PARAMETERS_ELEMENTS, PARAMETERS_ELEMENT_LISTS),
)
def test_init_with_default_and_alternatives(
    element: IRI | Literal | Any,
    element_check: IRI | Literal,
    element_list: list[IRI | Literal | Any],
    element_list_check: list[IRI | Literal],
):
    """Test Alt creation with default and alternative elements."""

    # Set kwargs to be used by constructor
    kwargs = {"default": element, "alternatives": element_list}

    # Test constructor
    alt = check_init_blank_node_object(
        *PARAMETERS_ALT,
        kwargs=kwargs,
        check_triples=False,
    )

    # Check default, alternatives and elements properties
    assert alt.default == element
    element_set, element_set_check = get_element_set(
        [element] + element_list, [element_check] + element_list_check
    )
    assert all(el in alt.elements for el in element_set)
    assert len(alt.elements) == len(element_set)
    alternative_set = element_set[1:]
    alternative_set_check = element_set_check[1:]
    assert all(el in alt.alternatives for el in alternative_set)
    assert len(alt.alternatives) == len(alternative_set)

    # Check that the expected triples, predicates and objects (and only them)
    # were indeed added to the graph
    triples = [
        (alt.iri, RDF.type, RDF.Alt),
        (alt.iri, RDF["_1"], element_check),
    ]
    predicates = [RDF[f"_{i + 2}"] for i in range(len(alternative_set_check))]
    objects = alternative_set_check
    check_graph_unordered_collection(
        alt.iri,
        alt.graph,
        predicates,
        objects,
        triples=triples,
        exact=True,
    )


@pytest.mark.parametrize(
    "element_list, element_list_check", PARAMETERS_ELEMENT_LISTS
)
def test_init_with_elements(
    element_list: list[IRI | Literal | Any],
    element_list_check: list[IRI | Literal],
):
    """Test Alt creation with elements."""

    # Set kwargs to be used by constructor
    kwargs = {"elements": element_list}

    # Test constructor
    alt = check_init_blank_node_object(
        *PARAMETERS_ALT,
        kwargs=kwargs,
        check_triples=False,
    )

    # Check default, alternatives and elements properties
    element_set, element_set_check = get_element_set(
        element_list, element_list_check
    )
    if not element_list:
        assert alt.default is None
        assert alt.alternatives == []
        assert alt.elements == []
    else:
        # assert alt.default == element_list[0]
        assert all(element in alt.elements for element in element_set)
        assert len(alt.elements) == len(element_set)

    # Check that the expected triples, predicates and objects (and only them)
    # were indeed added to the graph
    triples = [(alt.iri, RDF.type, RDF.Alt)]
    predicates = [RDF[f"_{i + 1}"] for i in range(len(element_set_check))]
    objects = element_set_check
    check_graph_unordered_collection(
        alt.iri,
        alt.graph,
        predicates,
        objects,
        triples=triples,
        exact=True,
    )
