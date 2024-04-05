from __future__ import annotations
from models import Context, TypeVariable, TypeFunctionApplication, TypeQuantifier
import typing
class Substitution:
    def __init__(self, raw):
        self.raw = raw

    def __call__(self, arg):
        if isinstance(arg, Substitution):
            return self.combine(arg)
        else:
            return self.apply(arg)
        
    def combine(self, s2: Substitution) -> Substitution:
        combined_raw = Substitution({**self.raw, **{k: self.apply(v) for k, v in s2.raw.items()}})
        return Substitution(combined_raw)

    A = typing.TypeVar('A', Context, TypeVariable, TypeFunctionApplication, TypeQuantifier)
    def apply(self, value: A) -> A:
        match value:
            case Context():
                return Context({k: self.apply(v) for k, v in value.items()})

            case TypeVariable():
                return self.raw.get(value['a'], value)

            # TODO: Should return TypeFunctionApplication
            case TypeFunctionApplication():
                return {**value, "mus": [self.apply(m) for m in value['mus']]}

            # TODO: Should return Type Quantifier
            case TypeQuantifier():
                return {**value, "sigma": self.apply(value['sigma'])}

        raise Exception('Unknown argument passed to substitution')


def instantiate(type, mappings=None):
    if mappings is None:
        mappings = {}

    match type:
        case TypeVariable():
            return mappings.get(type.a, type)

        case TypeFunctionApplication():
            return TypeFunctionApplication(type.C, [instantiate(m, mappings) for m in type.mus])

        case TypeQuantifier():
            mappings[type.a] = TypeVariable()
            return instantiate(type.sigma, mappings)

    raise Exception('Unknown type passed to instantiate')

class TypeVariable:
    current_type_var = 0  

    def __init__(self):
        self.a = f't{TypeVariable.current_type_var}'
        TypeVariable.current_type_var += 1  
