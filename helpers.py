from __future__ import annotations
from models import Context, TypeVariable, TypeFunctionApplication, TypeQuantifier, \
                   MonoType, PolyType, TypeFunction
import typing
from typing import Dict, Union, List
from errors import UnificationError, OccursError


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

            case TypeVariable():
                return create_monotype(self.apply(value.raw))

            case TypeFunctionApplication():
                return {**value, "mus": [self.apply(m) for m in value['mus']]}

            case TypeQuantifier():
                return {**value, "sigma": self.apply(value['sigma'])}
            
            case str():
                return ' '.join(self.raw.get(part, part) for part in value.split())

        raise Exception(f'Unknown argument {value} passed to substitution application')

def instantiate(polytype: PolyType, mappings:Dict[str, MonoType]=None) -> MonoType:
    if mappings is None:
        mappings = {}

    print(polytype)
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
        t = TypeQuantifier(name=q, sigma=t)
    return t

def diff(a: List, b: List) -> List:
    bset = set(b)
    return [v for v in a if v not in bset]

def free_vars(value: Union[PolyType, Context]) -> List[str]:
    match value:
        case Context():
            return [var for vals in value.values() for var in free_vars(vals)]

        case TypeVariable():
            return [value.a]

        case TypeFunctionApplication():
            return [var for mu in value.mus for var in free_vars(mu)]

        case TypeQuantifier():
            return [var for var in free_vars(value.sigma) if var != value.a]

    raise Exception('Unknown argument passed to substitution')

def unify(a: MonoType, b: MonoType) -> Substitution:
    match a, b:
        # Type Variables
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
    if note_to_type(type_notation) == TypeVariable:
        return TypeVariable(type_notation)
    else:
        return TypeFunctionApplication(type_notation)

    TypeParserTransformer.transform(type_parser.parse(raw))

def note_to_type(type_notation):
    type_parts = type_notation.split()
    if len(type_parts) == 0:
        raise Exception("Tried to initalize empty MonoType")
    elif type_parts[0] in TypeFunction:
        return TypeFunctionApplication
    elif len(type_parts) == 1:
        return TypeVariable
    else:
        raise Exception(f"Passed type notation: {type_notation}, does not qualify")

