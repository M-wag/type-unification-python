import lark
from lark import Lark

grammar = """
start:      tyfap
tyfap:      "->" mu mu          -> function
            | "List" mu         -> list
            | TYPE              -> type
?mu :        "(" tyfap ")"
            | tyvar

tyvar:      /[a-zA-Z_][a-zA-Z0-9_]*/ -> tyvar
TYPE:       "Int" | "Bool"


%ignore /\\s/ 
        | /\\/\\/.*/

"""

type_parser = Lark(grammar, parser='lalr', debug=True)
