"""Test Ontology constructor"""

import random as rd
import re
from contextlib import nullcontext

import pytest
from rdflib import OWL, RDFS, XSD, Literal

from tests.parameters import (
    PARAMETERS_LABELS,
    PARAMETERS_ONTOLOGY,
    PARAMETERS_VERSIONS,
)
from tests.tests_init.utils import check_init_labeled_object
from tests.utils import SEED, WARNING_MESSAGE_VERSION

# Set random seed
rd.seed(SEED)


@pytest.mark.parametrize("version, is_well_formatted", PARAMETERS_VERSIONS)
def test_init_with_version(
    version: str,
    is_well_formatted: bool,
):
    """Test Ontology creation with version number."""

    # Arbitrarily select label
    label, legal_label, *_ = rd.choice(PARAMETERS_LABELS)

    # Set kwargs to be used by constructor
    kwargs = {"label": label, "version": version}

    # Format identifier and version number
    identifier = Literal(label, datatype=XSD.string)
    legal_identifier = Literal(legal_label, datatype=XSD.string)
    version = Literal(version, datatype=XSD.string)

    # Set additional triple
    triples_add = [(OWL.versionInfo, version)]

    # Test constructor
    # If version number is not well-formatted, expect warning
    with (
        pytest.warns(UserWarning) if not is_well_formatted else nullcontext()
    ) as record:
        _ = check_init_labeled_object(
            *PARAMETERS_ONTOLOGY,
            identifier,
            legal_identifier,
            kwargs,
            identifier_property=RDFS.label,
            triples_add=triples_add,
        )

        # If expecting warnings
        if record is not None:
            assert len(record) == 1
            assert WARNING_MESSAGE_VERSION.format(version) in str(
                record[0].message
            )


@pytest.mark.parametrize("comment", PARAMETERS_LABELS)
def test_init_with_comment(comment: str):
    """Test Ontology creation with comment."""

    # Arbitrarily select label
    label, legal_label, *_ = rd.choice(PARAMETERS_LABELS)

    # Set kwargs to be used by constructor
    comment = comment[0]
    kwargs = {"label": label, "comment": comment}

    # Format identifier and comment
    identifier = Literal(label, datatype=XSD.string)
    legal_identifier = Literal(legal_label, datatype=XSD.string)
    comment = Literal(comment, datatype=XSD.string)

    # Set additional triple
    triples_add = [(RDFS.comment, comment)]

    # Test constructor
    _ = check_init_labeled_object(
        *PARAMETERS_ONTOLOGY,
        identifier,
        legal_identifier,
        kwargs,
        identifier_property=RDFS.label,
        triples_add=triples_add,
    )
