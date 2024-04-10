from __future__ import annotations
from typing import Union, Literal, Any, List
from dataclasses import dataclass


# Expressions
# e ::= x
#       | e1 e2 
#       | \x.e
#       | let x = e1 in e2


@dataclass
class VarExpr:
    x: str

@dataclass
class AppExpr:
    e1: Expr
    e2: Expr

@dataclass
class AbsExpr:
    x: str
    e: Expr

@dataclass
class LetExpr:
    x: str
    e1: Expr
    e2: Expr


Expr = Union[
    VarExpr,
    AppExpr,
    AbsExpr,
    LetExpr,
]

# mu    ::= a 
#       ::= | C mu_0 ... mu_n

# sigma ::= sigma
#           | Va.sigma

class TypeVariable:
    current_type_var = 0  

    def __init__(self, raw:str=None):
        if raw is None:
            self.raw = f"t{TypeVariable.current_type_var}"
            TypeVariable.current_type_var += 1
        else:
            self.raw = raw

    def __str__(self):
        return f'tyvar:{self.raw}'

TypeFunction = {"->", "Bool", "Int", "List"}
class TypeFunctionApplication:
    def __init__(self, raw: str=None, C:str=None, mus:List[str]=None):
        if raw is None:
            self.C = C
            self.mus = mus
            self.raw = str(self.C) + ''.join(f" {mu}" for mu in self.mus)
        else: 
            self.raw = raw
            self.C = raw.split()[0] 
            self.mus = raw.split()[1:] 

    def __str__(self):
        return f'tyfap:{self.raw}'

MonoType = TypeVariable | TypeFunctionApplication
    
@dataclass
class TypeQuantifier:
  a: str
  sigma: PolyType

PolyType = MonoType | TypeQuantifier

# Contexts

class Context(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

