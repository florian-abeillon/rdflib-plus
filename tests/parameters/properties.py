"""Define test parameters for properties"""

from rdflib import DCTERMS, OWL, RDF, RDFS, SKOS

from tests.parameters import (
    PARAMETERS_ELEMENTS_DOUBLE,
    PARAMETERS_ELEMENTS_INTEGER,
    PARAMETERS_ELEMENTS_IRI,
    PARAMETERS_ELEMENTS_LITERAL_DOUBLE,
    PARAMETERS_ELEMENTS_LITERAL_INTEGER,
    PARAMETERS_ELEMENTS_LITERAL_LANGSTRING,
    PARAMETERS_ELEMENTS_LITERAL_STRING,
    PARAMETERS_ELEMENTS_STRING,
    PARAMETERS_LABELS,
)
from tests.utils import build_iri, cartesian_product

# PARAMETERS_PROPERTIES_RESOURCE = {
#     DCTERMS.identifier,
#     DCTERMS.source,
#     RDF.type,
#     SKOS.prefLabel,
#     SKOS.altLabel,
# }

parameters_elements_iri_resource_with_check = [
    (label, build_iri(legal_label))
    for (
        label,
        legal_label,
        label_PascalCase,
        legal_label_PascalCase,
        label_camelCase,
        legal_label_camelCase,
    ) in PARAMETERS_LABELS
]
parameters_elements_iri_class_with_check = [
    (
        label,
        build_iri(legal_label_PascalCase, model_name="Class", sep="/"),
    )
    for (
        label,
        legal_label,
        label_PascalCase,
        legal_label_PascalCase,
        label_camelCase,
        legal_label_camelCase,
    ) in PARAMETERS_LABELS
]

PARAMETERS_PROPERTIES_TO_OBJECTS_RESOURCE = {
    DCTERMS.identifier: [
        *cartesian_product(PARAMETERS_ELEMENTS_STRING, [False]),
        *cartesian_product(PARAMETERS_ELEMENTS_LITERAL_STRING, [False]),
        *cartesian_product(PARAMETERS_ELEMENTS_LITERAL_LANGSTRING, [False]),
        *cartesian_product(PARAMETERS_ELEMENTS_INTEGER, [False]),
        *cartesian_product(PARAMETERS_ELEMENTS_LITERAL_INTEGER, [False]),
        # *cartesian_product(PARAMETERS_ELEMENTS_DOUBLE, [False]),
        # *cartesian_product(
        #     PARAMETERS_ELEMENTS_LITERAL_DOUBLE, [False]
        # ),
    ],
    DCTERMS.source: [
        *cartesian_product(PARAMETERS_ELEMENTS_IRI, [False]),
        *cartesian_product(
            parameters_elements_iri_resource_with_check, [True]
        ),
    ],
    RDF.type: [
        *[
            (iri, iri, False)
            for identifier, iri in parameters_elements_iri_class_with_check
        ],
        *cartesian_product(parameters_elements_iri_class_with_check, [True]),
    ],
    SKOS.prefLabel: [
        *cartesian_product(PARAMETERS_ELEMENTS_STRING, [False]),
        *cartesian_product(PARAMETERS_ELEMENTS_LITERAL_STRING, [False]),
        *cartesian_product(PARAMETERS_ELEMENTS_LITERAL_LANGSTRING, [False]),
        # TODO: Add integers etc. with string Literal?
    ],
    SKOS.altLabel: [
        *cartesian_product(PARAMETERS_ELEMENTS_STRING, [False]),
        *cartesian_product(PARAMETERS_ELEMENTS_LITERAL_STRING, [False]),
        *cartesian_product(PARAMETERS_ELEMENTS_LITERAL_LANGSTRING, [False]),
    ],
}

PARAMETERS_PROPERTIES_RESOURCE = (
    PARAMETERS_PROPERTIES_TO_OBJECTS_RESOURCE.keys()
)
PARAMETERS_PROPERTIES_OBJECTS_RESOURCE = [
    (property_, *objects)
    for property_, objects_list in PARAMETERS_PROPERTIES_TO_OBJECTS_RESOURCE.items()
    for objects in objects_list
]

PARAMETERS_PROPERTIES_CLASS = {
    RDFS.subClassOf,
    *PARAMETERS_PROPERTIES_RESOURCE,
}

PARAMETERS_PROPERTIES_PROPERTY = {
    RDFS.subPropertyOf,
    *PARAMETERS_PROPERTIES_RESOURCE,
}

PARAMETERS_PROPERTIES_CONTAINER = {
    RDFS.member,
    *PARAMETERS_PROPERTIES_RESOURCE,
}

PARAMETERS_PROPERTIES_LIST = {
    RDF.first,
    RDF.rest,
    *PARAMETERS_PROPERTIES_RESOURCE,
}

PARAMETERS_PROPERTIES_ONTOLOGY = {
    OWL.imports,
    OWL.priorVersion,
    OWL.versionInfo,
    RDFS.comment,
    RDFS.label,
    *PARAMETERS_PROPERTIES_RESOURCE,
}

PARAMETERS_PROPERTIES_TO_STRING_REPRESENTATION = {
    DCTERMS.identifier: "dcterms:identifier",
    DCTERMS.source: "dcterms:source",
    OWL.imports: "owl:imports",
    OWL.priorVersion: "owl:priorVersion",
    OWL.versionInfo: "owl:versionInfo",
    RDF.first: "rdf:first",
    RDF.rest: "rdf:rest",
    RDF.type: "rdf:type",
    RDFS.comment: "rdfs:comment",
    RDFS.label: "rdfs:label",
    RDFS.member: "rdfs:member",
    RDFS.subClassOf: "rdfs:subClassOf",
    RDFS.subPropertyOf: "rdfs:subPropertyOf",
    SKOS.altLabel: "skos:altLabel",
    SKOS.prefLabel: "skos:prefLabel",
}
