"""OWL resources constructors"""

from rdflib import OWL

from rdflib_plus.models.utils.define import define_property

# Define OWL Property constructors
FunctionalProperty = define_property("FunctionalProperty", OWL)
InverseFunctionalProperty = define_property("InverseFunctionalProperty", OWL)
SymmetricProperty = define_property("SymmetricProperty", OWL)
TransitiveProperty = define_property("TransitiveProperty", OWL)
