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
    @classmethod
    def get_raw(cls, monotype: MonoType):
        # if isinstance(monotype, TypeVariable):
        #     return 'A'
        match monotype:
            case TypeVariable():
                return monotype.raw
            case TypeFunctionApplication():
                if monotype.mus is None:
                    return monotype.C
                else:
                    return f"({monotype.C} {' '.join(cls.get_raw(mu) for mu in monotype.mus)})"
        raise Exception(f"Unexpected type: {type(monotype).__name__} passed")



    def __init__(self, C:str=None, mus:List[str]=None, raw:str=None):
        if raw is None:
            self.C = C
            self.mus = mus
            self.raw = self.get_raw(self)
        else: 
            raise NotImplemented()

    def __str__(self):
        return self.raw
    

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

