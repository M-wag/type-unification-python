import lark
from lark import Lark, Transformer
from models import TypeVariable, TypeFunctionApplication


grammar = """
?start:      tyfap | mu         -> start 

tyfap:      TYPE                -> type
            | "->" mu mu        -> function
            | "List" mu         -> list

?mu :        "(" tyfap ")"
            | tyvar

TYPE:       "Int" | "Bool"
tyvar:      /[a-zA-Z_][a-zA-Z0-9_]*/ -> tyvar


%ignore /\\s/ 
        | /\\/\\/.*/

"""

type_parser = Lark(grammar, parser='lalr', debug=True) 

class TypeParserTransformer(Transformer):
    
    def start(self, args):
        return args[0]

    def function(self, args):
        return TypeFunctionApplication(
            C  = "->", 
            mus = args,
        )

    def list(self, args):
        return TypeFunctionApplication(
            C  = "List", 
            mus = args,
        )
        
    def type(self, args):
        return TypeFunctionApplication(C=args[0], mus=[])
    
    def tyvar(self, args):
        return TypeVariable(args[0].value)


