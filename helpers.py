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

    T = typing.TypeVar('T', Context, TypeVariable, TypeFunctionApplication, TypeQuantifier)
    def apply(self, value: T) -> T:
        match value:
            case Context():
                return Context({k: self.apply(v) for k, v in value.items()})

            case TypeVariable():
                return self.raw.get(value['a'], value)

            case TypeFunctionApplication():
                return {**value, "mus": [self.apply(m) for m in value['mus']]}

            case TypeQuantifier():
                return {**value, "sigma": self.apply(value['sigma'])}

        raise Exception('Unknown argument passed to substitution')

