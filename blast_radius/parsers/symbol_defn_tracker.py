# ref: https://github.com/python/typeshed/blob/main/stdlib/ast.pyi
# establish the blast radius of the symbol within the definition.
#
# e.g.
#   symbol: Class.Attribute -> [Class, VariablesAssignedToClass]
#   symbol: Class.Method -> [Class, VariablesAssignedToClass]