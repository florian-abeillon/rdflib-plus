# rdflib-plus

Package to make the creation of RDF-compliant graphs easier.

# TODO

- Implement shape graph creation
- Implement SHACL validation
- Write examples
- Write README
- Write tests
- Set random seed?
- Is it better to explicitly add properties like inverse (is...Of/has...) or symmetric, or to find a way to add it in SPARQL queries?
-> *s is...Of o* -> *{s is...Of o} UNION {o has... s}*
-> *TransitiveProperty* -> *TransitiveProperty\**
-> *SymmetricProperty* -> *(SymmetricProperty|^SymmetricProperty)*

- Fix "UserWarning: Code: _pytestfixturefunction is not defined in namespace XSD" warning when running tests
- Write test for "constraints" kwarg of Class/Property classes
- Write test for "check_triples" and "graph* kwargs for Resource's methods
- Add support for "sorted" for RDF.Seq and RDF.List?
- Write test to see if warnings are raised
- Write test to see if errors are raised
- Warnings/errors in *\__init__()* methods cannot call *\__str__()* yet
- Test **\__init__* of oredered objects with Collection instance
- Implement the same methods as sets for Bags, if allow_duplicate == False?
- In test_methods, check graph
