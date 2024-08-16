"""Define constraints of standard RDF properties"""

from ...utils import parse_yaml

CONSTRAINTS_BASE_PROPERTIES = parse_yaml(
    "properties.yaml", __file__, normalize=True, normalize_keys=True
)

CONSTRAINTS_BASE_PROPERTIES = {
    label: kwargs["constraints"]
    for label, kwargs in CONSTRAINTS_BASE_PROPERTIES.items()
}
