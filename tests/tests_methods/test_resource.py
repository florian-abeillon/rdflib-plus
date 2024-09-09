"""Test Resource methods"""

import random as rd
from typing import Any

import pytest
from rdflib import DCTERMS, SKOS, Literal
from rdflib import URIRef as IRI

from rdflib_plus import Resource, SimpleGraph
from tests.parameters import (
    PARAMETERS_ELEMENTS_LITERAL_LANGSTRING,
    PARAMETERS_ELEMENTS_LITERAL_STRING,
    PARAMETERS_ELEMENTS_STRING,
    PARAMETERS_IDENTIFIERS,
    PARAMETERS_LANGS,
    PARAMETERS_PROPERTIES_OBJECTS_RESOURCE,
    PARAMETERS_PROPERTIES_TO_OBJECTS_RESOURCE,
)
from tests.tests_methods.utils import (
    build_object,
    build_predicate_object,
    build_resource,
    check_method,
    check_str,
    get_another_parameter,
)
from tests.utils import SEED, cartesian_product

# Set random seed
rd.seed(SEED)


# TODO: Test other namespaces
@pytest.mark.parametrize(
    "identifier, legal_identifier, datatype",
    PARAMETERS_IDENTIFIERS,
)
def test_str(
    identifier: Any,
    legal_identifier: str,
    datatype: IRI,
):
    """Test Resource's __str__ operator."""

    # Initialize graph, and create Resource
    graph = SimpleGraph()
    resource = Resource(graph, identifier=identifier)

    # Check the string representation of the Resource
    check_str(resource, "Resource", legal_identifier)


@pytest.mark.parametrize(
    "predicate_iri, object_, object_check, is_object_resource,"
    "is_predicate_resource, with_graph",
    cartesian_product(
        PARAMETERS_PROPERTIES_OBJECTS_RESOURCE, [True, False], [True, False]
    ),
)
def test_add(
    predicate_iri: IRI,
    object_: Any,
    object_check: Literal | IRI,
    is_object_resource: bool,
    is_predicate_resource: bool,
    with_graph: bool,
):
    """Test Resource's add() method."""

    # Create a Resource
    resource = build_resource()

    # Create predicate and object
    predicate, object_ = build_predicate_object(
        resource.graph,
        predicate_iri,
        is_predicate_resource,
        object_,
        is_object_resource,
    )

    # Set args to feed the method with
    args_method = (predicate, object_)

    # Specify additional triples to check for
    triples_add = [(resource.iri, predicate_iri, object_check)]

    # Check if the method created the expected triples
    check_method(
        resource,
        resource.add,
        args=args_method,
        triples_add=triples_add,
        with_graph=with_graph,
    )


@pytest.mark.parametrize(
    "predicate_iri, object_, object_check, is_object_resource,"
    "is_predicate_resource, lang, with_graph",
    cartesian_product(
        PARAMETERS_PROPERTIES_OBJECTS_RESOURCE,
        [True, False],
        PARAMETERS_LANGS,
        [True, False],
    ),
)
def test_add_with_lang(
    predicate_iri: IRI,
    object_: Any,
    object_check: Literal | IRI,
    is_object_resource: bool,
    is_predicate_resource: bool,
    lang: str,
    with_graph: bool,
):
    """Test Resource's add() method while specifying a language."""

    # Only consider properties which accept string objects
    if predicate_iri not in [
        DCTERMS.identifier,
        SKOS.prefLabel,
        SKOS.altLabel,
    ]:
        return

    # Create a Resource
    resource = build_resource()

    # Create predicate, and object as it should appear in the graph
    predicate, object_ = build_predicate_object(
        resource.graph,
        predicate_iri,
        is_predicate_resource,
        object_,
        is_object_resource,
    )
    object_check = Literal(str(object_), lang=lang)

    # Set args and kwargs to feed the method with
    args_method = (predicate, object_)
    kwargs_method = {"lang": lang}

    # Specify additional triples to check for
    triples_add = [(resource.iri, predicate_iri, object_check)]

    # Check if the method created the expected triples
    check_method(
        resource,
        resource.add,
        args=args_method,
        kwargs=kwargs_method,
        triples_add=triples_add,
        with_graph=with_graph,
    )


@pytest.mark.parametrize(
    "predicate_iri, object_, object_check, is_object_resource,"
    "is_predicate_resource, with_graph",
    cartesian_product(
        PARAMETERS_PROPERTIES_OBJECTS_RESOURCE, [True, False], [True, False]
    ),
)
def test_set(
    predicate_iri: IRI,
    object_: Any,
    object_check: Literal | IRI,
    is_object_resource: bool,
    is_predicate_resource: bool,
    with_graph: bool,
):
    """Test Resource's set() method."""

    # Create a Resource
    resource = build_resource()

    # Create predicate and object
    predicate, object_ = build_predicate_object(
        resource.graph,
        predicate_iri,
        is_predicate_resource,
        object_,
        is_object_resource,
    )

    # Set args to feed the method with
    args_method = (predicate, object_)

    # Specify additional triples to check for
    triples_add = [(resource.iri, predicate_iri, object_check)]

    # Check if the method created the expected triples
    check_method(
        resource,
        resource.set,
        args=args_method,
        triples_add=triples_add,
        with_graph=with_graph,
    )


@pytest.mark.parametrize(
    "predicate_iri, object_, object_check, is_object_resource,"
    "is_predicate_resource, lang, with_graph",
    cartesian_product(
        PARAMETERS_PROPERTIES_OBJECTS_RESOURCE,
        [True, False],
        PARAMETERS_LANGS,
        [True, False],
    ),
)
def test_set_with_lang(
    predicate_iri: IRI,
    object_: Any,
    object_check: Literal | IRI,
    is_object_resource: bool,
    is_predicate_resource: bool,
    lang: str,
    with_graph: bool,
):
    """Test Resource's set() method while specifying a language."""

    # Only consider properties which accept string objects
    if predicate_iri not in [
        DCTERMS.identifier,
        SKOS.prefLabel,
        SKOS.altLabel,
    ]:
        return

    # Create a Resource
    resource = build_resource()

    # Create predicate, and object as it should appear in the graph
    predicate, object_ = build_predicate_object(
        resource.graph,
        predicate_iri,
        is_predicate_resource,
        object_,
        is_object_resource,
    )
    object_check = Literal(str(object_), lang=lang)

    # Set args and kwargs to feed the method with
    args_method = (predicate, object_)
    kwargs_method = {"lang": lang}

    # Specify additional triples to check for
    triples_add = [(resource.iri, predicate_iri, object_check)]

    # Check if the method created the expected triples
    check_method(
        resource,
        resource.set,
        args=args_method,
        kwargs=kwargs_method,
        triples_add=triples_add,
        with_graph=with_graph,
    )


@pytest.mark.parametrize(
    "predicate_iri, object_1, object_1_check, is_object_1_resource,"
    "is_predicate_resource, with_graph",
    cartesian_product(
        PARAMETERS_PROPERTIES_OBJECTS_RESOURCE,
        [True, False],
        [True, False],
    ),
)
def test_set_with_replace(
    predicate_iri: IRI,
    object_1: Any,
    object_1_check: Literal | IRI,
    is_object_1_resource: bool,
    is_predicate_resource: bool,
    with_graph: bool,
):
    """Test Resource's set() method when replacing a value."""

    # Create a Resource
    resource = build_resource()

    # Get another set of parameters, that is valid with predicate
    object_2, object_2_check, is_object_2_resource = get_another_parameter(
        PARAMETERS_PROPERTIES_TO_OBJECTS_RESOURCE[predicate_iri],
        key=lambda new_parameter: new_parameter[1] != object_1_check,
    )

    # Create predicate and objects
    predicate, object_1 = build_predicate_object(
        resource.graph,
        predicate_iri,
        is_predicate_resource,
        object_1,
        is_object_1_resource,
    )
    object_2 = build_object(
        resource.graph,
        predicate_iri,
        object_2,
        is_object_2_resource,
    )

    # If necessary, create a new, separate graph
    kwargs = {}
    if with_graph:
        graph = SimpleGraph()
        kwargs["graph"] = graph

    # Set them
    resource.set(predicate, object_1, **kwargs)

    # Set args and kwargs to feed the method with
    args_method = (predicate, object_2)
    kwargs_method = {"replace": True}

    # Specify additional triples to check for
    triples_add = [(resource.iri, predicate_iri, object_2_check)]
    triples_rem = [(resource.iri, predicate_iri, object_1_check)]

    # Check if the method created the expected triples
    if not with_graph:
        kwargs = {"triples_rem": triples_rem}
    check_method(
        resource,
        resource.set,
        args=args_method,
        kwargs=kwargs_method,
        triples_add=triples_add,
        with_graph=with_graph,
        **kwargs
    )


@pytest.mark.parametrize(
    "predicate_iri, object_, object_check, is_object_resource,"
    "is_predicate_resource",
    cartesian_product(PARAMETERS_PROPERTIES_OBJECTS_RESOURCE, [True, False]),
)
def test_get_value(
    predicate_iri: IRI,
    object_: Any,
    object_check: Literal | IRI,
    is_object_resource: bool,
    is_predicate_resource: bool,
):
    """Test Resource's get_value() method."""

    # Create a Resource
    resource = build_resource()

    # Create predicate and object
    predicate, object_ = build_predicate_object(
        resource.graph,
        predicate_iri,
        is_predicate_resource,
        object_,
        is_object_resource,
    )

    # Set them
    resource.set(predicate, object_)

    # Retrieve the value just set, and check it
    assert resource.get_value(predicate) == object_check
    assert resource.get_value(predicate_iri) == object_check


@pytest.mark.parametrize(
    "predicate_iri, object_, object_check, is_object_resource,"
    "is_predicate_resource, with_o, with_graph",
    cartesian_product(
        PARAMETERS_PROPERTIES_OBJECTS_RESOURCE,
        [True, False],
        [True, False],
        [True, False],
    ),
)
def test_remove(
    predicate_iri: IRI,
    object_: Any,
    object_check: Literal | IRI,
    is_object_resource: bool,
    is_predicate_resource: bool,
    with_o: bool,
    with_graph: bool,
):
    """
    Test Resource's remove() method, with and without specifying an
    object.
    """

    # Create a Resource
    resource = build_resource()

    # Create predicate and object
    predicate, object_ = build_predicate_object(
        resource.graph,
        predicate_iri,
        is_predicate_resource,
        object_,
        is_object_resource,
    )

    # If necessary, create a new, separate graph
    kwargs = {}
    if with_graph:
        graph_new = SimpleGraph()
        kwargs["graph"] = graph_new

    # Set them
    resource.set(predicate, object_, replace=True, **kwargs)

    # Set args and potential kwargs to feed the method with
    args_method = (predicate,)
    kwargs_method = {"o": object_} if with_o else {}

    # Specify removed triples to check for
    triples_rem = [(resource.iri, predicate_iri, object_check)]

    # Check if the method removed the expected triples
    check_method(
        resource,
        resource.remove,
        args=args_method,
        kwargs=kwargs_method,
        triples_rem=triples_rem,
        with_graph=with_graph,
        **kwargs
    )


@pytest.mark.parametrize(
    "predicate_iri, object_1, object_1_check, is_object_1_resource,"
    "is_predicate_resource, with_o, with_graph",
    cartesian_product(
        PARAMETERS_PROPERTIES_OBJECTS_RESOURCE,
        [True, False],
        [True, False],
        [True, False],
    ),
)
def test_remove_multiple(
    predicate_iri: IRI,
    object_1: Any,
    object_1_check: Literal | IRI,
    is_object_1_resource: bool,
    is_predicate_resource: bool,
    with_o: bool,
    with_graph: bool,
):
    """
    Test Resource's remove() method on multiple objects, with and without
    specifying an object.
    """

    # Create a Resource
    resource = build_resource()

    # If a value was already set for this predicate during the initialization
    # of the Resource
    object_2 = resource.get_value(predicate_iri)
    if object_2 is not None:
        # Use it as second object for the removal test
        object_2_check = object_2

    else:
        # Get another set of parameters, that is valid with predicate
        object_2, object_2_check, is_object_2_resource = get_another_parameter(
            PARAMETERS_PROPERTIES_TO_OBJECTS_RESOURCE[predicate_iri],
            key=lambda new_parameter: new_parameter[1] != object_1_check,
        )

        # Create second object
        object_2 = build_object(
            resource.graph,
            predicate_iri,
            object_2,
            is_object_2_resource,
        )

    # Create predicate and first object
    predicate, object_1 = build_predicate_object(
        resource.graph,
        predicate_iri,
        is_predicate_resource,
        object_1,
        is_object_1_resource,
    )
    print(">> object_1", object_1)

    # If necessary, create a new, separate graph
    kwargs = {}
    if with_graph:
        graph_new = SimpleGraph()
        kwargs["graph"] = graph_new

    # Add both
    resource.add(predicate, object_1, **kwargs)
    resource.add(predicate, object_2, **kwargs)

    # Set args to feed the method with
    args_method = (predicate,)

    # Specify removed triples to check for, and set potential kwargs
    # to feed the method with
    triples_rem = [(resource.iri, predicate_iri, object_1_check)]
    if with_o:
        kwargs_method = {"o": object_1}
    else:
        kwargs_method = {}
        if object_2_check != object_1_check:
            triples_rem.append((resource.iri, predicate_iri, object_2_check))

    # Check if the method removed the expected triples
    check_method(
        resource,
        resource.remove,
        args=args_method,
        kwargs=kwargs_method,
        triples_rem=triples_rem,
        with_graph=with_graph,
        **kwargs
    )


@pytest.mark.parametrize(
    "predicate_iri, object_, object_check, is_object_resource,"
    "is_predicate_resource, lang_1, with_graph",
    cartesian_product(
        PARAMETERS_PROPERTIES_OBJECTS_RESOURCE,
        [True, False],
        PARAMETERS_LANGS,
        [True, False],
    ),
)
def test_remove_with_lang(
    predicate_iri: IRI,
    object_: Any,
    object_check: Literal | IRI,
    is_object_resource: bool,
    is_predicate_resource: bool,
    lang_1: str,
    with_graph: bool,
):
    """
    Test Resource's remove() method on multiple objects, while specifying
    a language.
    """

    # Only consider properties which accept string objects
    if predicate_iri not in [
        DCTERMS.identifier,
        SKOS.prefLabel,
        SKOS.altLabel,
    ]:
        return

    # Create a Resource
    resource = build_resource()

    # Create predicate and string object
    predicate, object_ = build_predicate_object(
        resource.graph,
        predicate_iri,
        is_predicate_resource,
        object_,
        is_object_resource,
    )

    # Get another language
    lang_2 = get_another_parameter(PARAMETERS_LANGS, parameter=lang_1)

    # If necessary, create a new, separate graph
    kwargs = {}
    if with_graph:
        graph_new = SimpleGraph()
        kwargs["graph"] = graph_new

    # Add both
    resource.add(predicate, object_, lang=lang_1, **kwargs)
    resource.add(predicate, object_, lang=lang_2, **kwargs)

    # Set args and kwargs to feed the method with
    args_method = (predicate,)
    kwargs_method = {"o": object_, "lang": lang_1}

    # Specify removed triples to check for
    object_check = Literal(str(object_), lang=lang_1)
    triples_rem = [(resource.iri, predicate_iri, object_check)]

    # Check if the method removed the expected triples
    check_method(
        resource,
        resource.remove,
        args=args_method,
        kwargs=kwargs_method,
        triples_rem=triples_rem,
        with_graph=with_graph,
        **kwargs
    )


@pytest.mark.parametrize(
    "predicate_iri, object_1, object_1_check, is_object_1_resource,"
    "is_predicate_resource, with_graph",
    cartesian_product(
        PARAMETERS_PROPERTIES_OBJECTS_RESOURCE, [True, False], [True, False]
    ),
)
def test_replace(
    predicate_iri: IRI,
    object_1: Any,
    object_1_check: Literal | IRI,
    is_object_1_resource: bool,
    is_predicate_resource: bool,
    with_graph: bool,
):
    """Test Resource's replace() method."""

    # Create a Resource
    resource = build_resource()

    # Get another set of parameters, that is valid with predicate
    object_2, object_2_check, is_object_2_resource = get_another_parameter(
        PARAMETERS_PROPERTIES_TO_OBJECTS_RESOURCE[predicate_iri],
        key=lambda new_parameter: new_parameter[1] != object_1_check,
    )

    # Create predicate and objects
    predicate, object_1 = build_predicate_object(
        resource.graph,
        predicate_iri,
        is_predicate_resource,
        object_1,
        is_object_1_resource,
    )
    object_2 = build_object(
        resource.graph,
        predicate_iri,
        object_2,
        is_object_2_resource,
    )

    # If necessary, create a new, separate graph
    kwargs = {}
    if with_graph:
        graph_new = SimpleGraph()
        kwargs["graph"] = graph_new

    # Set them
    resource.set(predicate, object_1, **kwargs)

    # Set args to feed the method with
    args_method = (predicate, object_2)

    # Specify additional triples to check for
    triples_add = [(resource.iri, predicate_iri, object_2_check)]
    triples_rem = [(resource.iri, predicate_iri, object_1_check)]

    # Check if the method created the expected triples
    check_method(
        resource,
        resource.replace,
        args=args_method,
        triples_add=triples_add,
        triples_rem=triples_rem,
        with_graph=with_graph,
        **kwargs
    )


@pytest.mark.parametrize(
    "label, label_check, with_graph",
    cartesian_product(
        PARAMETERS_ELEMENTS_STRING + PARAMETERS_ELEMENTS_LITERAL_STRING,
        [True, False],
    ),
)
def test_add_alt_label(
    label: str,
    label_check: Literal,
    with_graph: bool,
):
    """Test Resource's add_alt_label() method."""

    # Create a Resource
    resource = build_resource()

    # Set args to feed the method with
    args_method = (label,)

    # Specify additional triples to check for
    triples_add = [(resource.iri, SKOS.altLabel, label_check)]

    # Check if the method created the expected triples
    check_method(
        resource,
        resource.add_alt_label,
        args=args_method,
        triples_add=triples_add,
        with_graph=with_graph,
    )


@pytest.mark.parametrize(
    "label, label_check, lang, with_graph",
    cartesian_product(
        PARAMETERS_ELEMENTS_STRING
        + PARAMETERS_ELEMENTS_LITERAL_STRING
        + PARAMETERS_ELEMENTS_LITERAL_LANGSTRING,
        PARAMETERS_LANGS,
        [True, False],
    ),
)
def test_add_alt_label_with_lang(
    label: str,
    label_check: Literal,
    lang: str,
    with_graph: bool,
):
    """Test Resource's add_alt_label() method, while specifying a language."""

    # Create a Resource
    resource = build_resource()

    # Set args and kwargs to feed the method with
    args_method = (label,)
    kwargs_method = {"lang": lang}

    # Specify additional triples to check for
    label_check = Literal(str(label_check), lang=lang)
    triples_add = [(resource.iri, SKOS.altLabel, label_check)]

    # Check if the method created the expected triples
    check_method(
        resource,
        resource.add_alt_label,
        args=args_method,
        kwargs=kwargs_method,
        triples_add=triples_add,
        with_graph=with_graph,
    )


@pytest.mark.parametrize(
    "label, label_check, with_graph",
    cartesian_product(
        PARAMETERS_ELEMENTS_STRING + PARAMETERS_ELEMENTS_LITERAL_STRING,
        [True, False],
    ),
)
def test_set_pref_label(
    label: str,
    label_check: Literal,
    with_graph: bool,
):
    """Test Resource's set_pref_label() method."""

    # Create a Resource
    resource = build_resource()

    # Set args to feed the method with
    args_method = (label,)

    # Specify additional triples to check for
    triples_add = [(resource.iri, SKOS.prefLabel, label_check)]

    # Check if the method created the expected triples
    check_method(
        resource,
        resource.set_pref_label,
        args=args_method,
        triples_add=triples_add,
        with_graph=with_graph,
    )


@pytest.mark.parametrize(
    "label, label_check, lang, with_graph",
    cartesian_product(
        PARAMETERS_ELEMENTS_STRING
        + PARAMETERS_ELEMENTS_LITERAL_STRING
        + PARAMETERS_ELEMENTS_LITERAL_LANGSTRING,
        PARAMETERS_LANGS,
        [True, False],
    ),
)
def test_set_pref_label_with_lang(
    label: str,
    label_check: Literal,
    lang: str,
    with_graph: bool,
):
    """Test Resource's set_pref_label() method, while specifying a language."""

    # Create a Resource
    resource = build_resource()

    # Set args and kwargs to feed the method with
    args_method = (label,)
    kwargs_method = {"lang": lang}

    # Specify additional triples to check for
    label_check = Literal(str(label_check), lang=lang)
    triples_add = [(resource.iri, SKOS.prefLabel, label_check)]

    # Check if the method created the expected triples
    check_method(
        resource,
        resource.set_pref_label,
        args=args_method,
        kwargs=kwargs_method,
        triples_add=triples_add,
        with_graph=with_graph,
    )
