from __future__ import annotations
from typing import Union, Literal, Any
from dataclasses import dataclass


# Expressions
# e ::= x
#       | e1 e2 
#       | \x.e
#       | let x = e1 in e2


@dataclass
class VariableExpression:
    x: str

@dataclass
class ApplicationExpression:
    e1: Expression
    e2: Expression

@dataclass
class AbstractionExpression:
    x: str
    e: Expression

@dataclass
class LetExpression:
    x: str
    e1: Expression
    e2: Expression


Expression = Union[
    VariableExpression,
    ApplicationExpression,
    AbstractionExpression,
    LetExpression,
]

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
    
class TypeQuantifier:
  a: str
  sigma: PolyType

PolyType = Union[
    MonoType,
    TypeQuantifier,
]

# Contexts

class Context(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

