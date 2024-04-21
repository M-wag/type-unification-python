from __future__ import annotations
from models import Context, TypeVariable, TypeFunctionApplication, TypeQuantifier, \
                   MonoType, PolyType, TypeFunction
import typing 
from typing import Dict, Union, List, Iterable, Set
from type_parser import type_parser, TypeParserTransformer
from errors import UnificationError, OccursError
from itertools import chain


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
        return combined_raw


    A = typing.TypeVar('A', Context, TypeVariable, TypeFunctionApplication, TypeQuantifier)
    def apply(self, value: A) -> A:
        match value:
            case Context():
                return Context({k: self.apply(v) for k, v in value.items()})

            case TypeVariable() | TypeFunctionApplication():
                return create_monotype(self.apply(value.raw))

            case TypeQuantifier():
                return {**value, "sigma": self.apply(value['sigma'])}
            
            case str():
                return ' '.join(self.raw.get(part, part) for part in value.split())

        raise Exception(f'Unknown argument {value} passed to substitution application')

def instantiate(polytype: PolyType, mappings:Dict[str, MonoType]=None) -> MonoType:
    if mappings is None:
        mappings = {}

    match polytype:
        case TypeVariable():
            return mappings.get(polytype.raw, polytype)

        case TypeFunctionApplication():
            return TypeFunctionApplication(polytype.C, [instantiate(m, mappings) for m in polytype.mus])

        case TypeQuantifier():
            mappings[polytype.a] = TypeVariable()
            return instantiate(polytype.sigma, mappings)

    raise Exception(f'Unknown type: {type(polytype).__name__} passed to instantiate')


def generalise(ctx: Context, type: PolyType) -> PolyType:
    quantifiers = diff(free_vars(type), free_vars(ctx))
    t = type
    for q in quantifiers:
        t = TypeQuantifier(raw=q, sigma=t)
    return t

def diff(a: List, b: List) -> List:
    bset = set(b)
    return [v for v in a if v not in bset]

def _flatten(arr: Iterable) -> Iterable: 
    x = chain.from_iterable(arr)
    return type(arr)(chain.from_iterable(arr))
def free_vars(value: Union[PolyType, Context], 
              excluded:List[str] = []
              ) -> List[str]:
    match value:
        case Context():
            return _flatten([free_vars(val, excluded) for val in value.values() if val not in excluded])

        case TypeVariable():
            return [value.raw]

        case TypeFunctionApplication():
            return _flatten([free_vars(mu, excluded) for mu in value.mus if mu not in excluded])

        case TypeQuantifier():
            excluded.append(value.a)
            return free_vars(value.sigma, excluded)

    raise Exception('Unknown argument passed to substitution')

def unify(a: MonoType, b: MonoType) -> Substitution:
    match a, b:
        case TypeVariable(), TypeVariable() if a.raw == b.raw:
            return Substitution({})

        case TypeVariable(), _:
            if contains(b, a):
                raise OccursError("Cannot create infinite type")
            return Substitution({a.raw: b.raw})

        case _, TypeVariable():
            return unify(b, a)
        
        # Type Function Applications
        case TypeFunctionApplication(), TypeFunctionApplication():
            if a.C != b.C:
                raise UnificationError(f"Failed to unify different type functions: {a.C}, {b.C}")

            S = Substitution({})
            for t1, t2 in zip(a.mus, b.mus):
                S = S.combine(unify(S(t1), S(t2)))
            return S


def contains(value: MonoType, type2) -> bool:
    match value:
        case TypeVariable(): # should always be a recurive call?
            return value.raw == type2.raw 

        case TypeFunctionApplication():
            return any(contains(t, type2) for t in value.mus)

    raise Exception('Unknown argument passed to contains')


def create_monotype(type_notation: str) -> MonoType:
    if type_notation is None:
        raise Exception('Cannot initialize MonoType from empty string')

    return TypeParserTransformer().transform(type_parser.parse(type_notation))
