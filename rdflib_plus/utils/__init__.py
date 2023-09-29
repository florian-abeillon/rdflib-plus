from ..config import VERSION
from ..namespace.namespaces import (
    DEFAULT_NAMESPACE,
    PREFIXES,
    SHAPES_NAMESPACE,
    build_custom_namespace,
)
from .parse import parse_yaml
from .utils import format_label, legalize_for_iri
