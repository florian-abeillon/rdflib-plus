"""Test Ontology constructor"""

import random as rd

import pytest
from rdflib import RDFS, XSD, Literal

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

    # Format identifier and label
    identifier = Literal(label, datatype=XSD.string)
    label = identifier
    legal_identifier = label

    # Test constructor
    _ = check_init_labeled_object(
        *PARAMETERS_ONTOLOGY,
        identifier,
        legal_identifier,
        kwargs,
        label=label,
        identifier_property=RDFS.label,
    )
