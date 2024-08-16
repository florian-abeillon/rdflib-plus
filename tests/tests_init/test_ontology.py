"""Test Ontology constructor"""

import random as rd

import pytest
from rdflib import OWL, RDFS, XSD, Literal

from tests.parameters import (
    PARAMETERS_LABELS,
    PARAMETERS_ONTOLOGY,
    PARAMETERS_VERSIONS,
)
from tests.tests_init.utils import check_init_labeled_object
from tests.utils import SEED


@pytest.mark.parametrize("version", PARAMETERS_VERSIONS)
def test_init_ontology_with_version(version: str):
    """Test Ontology creation with version number."""

    # Arbitrarily select label
    rd.seed(SEED)
    label = rd.choice(PARAMETERS_LABELS)[0]

    # Set kwargs to be used by constructor
    kwargs = {"label": label, "version": version}

    # Format identifier and version number
    identifier = Literal(label, datatype=XSD.string)
    legal_identifier = identifier
    version = Literal(version, datatype=XSD.string)

    # Set additional triple
    add_triples = [(OWL.versionInfo, version)]

    # Test constructor
    _ = check_init_labeled_object(
        *PARAMETERS_ONTOLOGY,
        identifier,
        legal_identifier,
        kwargs,
        identifier_property=RDFS.label,
        add_triples=add_triples,
    )


@pytest.mark.parametrize("comment", PARAMETERS_LABELS)
def test_init_ontology_with_comment(comment: str):
    """Test Ontology creation with comment."""

    # Arbitrarily select label
    rd.seed(SEED)
    label = rd.choice(PARAMETERS_LABELS)[0]

    # Set kwargs to be used by constructor
    comment = comment[0]
    kwargs = {"label": label, "comment": comment}

    # Format identifier and comment
    identifier = Literal(label, datatype=XSD.string)
    legal_identifier = identifier
    comment = Literal(comment, datatype=XSD.string)

    # Set additional triple
    add_triples = [(RDFS.comment, comment)]

    # Test constructor
    _ = check_init_labeled_object(
        *PARAMETERS_ONTOLOGY,
        identifier,
        legal_identifier,
        kwargs,
        identifier_property=RDFS.label,
        add_triples=add_triples,
    )
