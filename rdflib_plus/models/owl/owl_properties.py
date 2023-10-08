"""OWL resources constructors"""

from rdflib import OWL

from rdflib_plus.models.utils import define_class

# Define OWL Property constructors
FunctionalProperty = define_class("FunctionalProperty", OWL)
InverseFunctionalProperty = define_class("InverseFunctionalProperty", OWL)
SymmetricProperty = define_class("SymmetricProperty", OWL)
TransitiveProperty = define_class("TransitiveProperty", OWL)
