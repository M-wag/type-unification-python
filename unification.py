from models import MonoType, TypeVariable, TypeFunctionApplication
from typing import Callable

# TODO: unify should return Subsituin, don't know how to type hint

def make_substition(): pass
def contains(): pass

def unify(a: MonoType, b: MonoType) -> Callable:
    match a, b:
        # Type Variables
        case TypeVariable(), TypeVariable() if a.name == b.name:
            return make_substition({})
        case TypeVariable(), TypeVariable() if contains(b, a):
            raise Exception("Occurs check failed, cannot create infinite type")
        case TypeVariable(), _ :
            # TODO: subsitution a to b 
            make_substition({})
        case _, TypeVariable():
            return unify(b, a)
        
        # Type Function Applications
        case TypeFunctionApplication(), TypeFunctionApplication() if a.C != b.C:
            raise Exception(f"Failed to unify different type functions: {a.C}, {b.C}")
        case TypeFunctionApplication(), TypeFunctionApplication() if a.C == b.C:
            S = {}
            pass
