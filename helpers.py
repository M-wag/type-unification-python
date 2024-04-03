from typing import Union, Literal
from dataclasses import dataclass


# mu    ::= a 
#       ::= | C mu_0 ... mu_n

# sigma ::= sigma
#           | Va.sigma

@dataclass
class TypeVariable:
    a: str

TypeFunction = Literal["->", "Bool", "Int", "List"]

@dataclass
class TypeFunctionApplication:
    C: TypeFunction

MonoType = Union[
    TypeVariable,
    TypeFunctionApplication
]
    

