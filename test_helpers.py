from helpers import unify, Substitution, create_monotype, instantiate, free_vars, \
        Context
from models import TypeVariable, TypeFunctionApplication, TypeQuantifier
from errors import UnificationError, OccursError
import pytest


### HELPERS 

@pytest.fixture(autouse=True)
def reset_tyvar_counter():
    TypeVariable.current_type_var = 0  

def check_equality(S_produced, S_expect):
    expected = {'t0' : 't1'}
    # print(S_produced)
    assert S_produced == S_expect, f"Expected {S_expect}, got {S_produced}"

### SUCCESFUL MAPPINGS

def test_unify_diff_type_vars():
    S = unify(
        TypeVariable('t0'),
        TypeVariable('t1')
    )
    check_equality(S.raw, {'t0' : 't1'})

def test_unify_same_type_vars():
    S = unify(
        TypeVariable('t0'),
        TypeVariable('t0')
    )
    check_equality(S.raw, {})

def test_unify_same_type_apps():
    S = unify(
        TypeFunctionApplication(
            C = '->',
            mus = [TypeVariable('t0'), TypeVariable('t1')]
        ),
        TypeFunctionApplication(
            C = '->',
            mus = [TypeVariable('t0'), TypeVariable('t1')]
        ),
    )
    check_equality(S.raw, {})

def test_unify_type_apps_same_typvar_mus():
    S = unify(
        TypeFunctionApplication(
            C = '->',
            mus = [TypeVariable('t0'), TypeVariable('t1')]
        ),
        TypeFunctionApplication(
            C = '->',
            mus = [TypeVariable('t0'), TypeVariable('t1')]
        ),
    )
    check_equality(S.raw, {})

    S = unify(
        TypeFunctionApplication(
            C = 'List',
            mus = [TypeVariable('t0')]
        ),
        TypeFunctionApplication(
            C = 'List',
            mus = [TypeVariable('t0')]
        ),
    )
    check_equality(S.raw, {})

def test_unify_type_apps_diff_typvar_mus():
    S = unify(
        TypeFunctionApplication(
            C = '->',
            mus = [TypeVariable('t0'), TypeVariable('t1')]
        ),
        TypeFunctionApplication(
            C = '->',
            mus = [TypeVariable('t2'), TypeVariable('t3')]
        ),
    )
    check_equality(S.raw, {'t0' : 't2', 't1' : 't3'})

    S = unify(
        TypeFunctionApplication(
            C = 'List',
            mus = [TypeVariable('t0')]
        ),
        TypeFunctionApplication(
            C = 'List',
            mus = [TypeVariable('t1')]
        ),
    )
    check_equality(S.raw, {'t0' : 't1'})


def test_create_monotype_produced_types():
    # TODO: do not require parentehsis around Int
    x = [
        ("(List Int)", TypeFunctionApplication),
        ("List a", TypeFunctionApplication),
        ("(Int)", TypeFunctionApplication),
        ("(Bool)", TypeFunctionApplication),
        ("-> a b", TypeFunctionApplication),
        ("-> (Int) (Int)", TypeFunctionApplication),
        ("a", TypeVariable),
    ]

    for type_note, expected_type in x:
        produced_type = create_monotype(type_note)
        assert isinstance(produced_type, expected_type), \
            f"For \"{type_note}\" expected type : {expected_type.__name__}, got {type(produced_type).__name__}"


### MAPPINGS THAT RAISE ERRORS

def test_unify_diff_tyfuns_raise_error():
    with pytest.raises(UnificationError) as exc_info:
        unify(
            TypeFunctionApplication(
                C = 'List',
                mus = [TypeVariable('t0')]
            ), 
            TypeFunctionApplication(
                C = '->',
                mus = [TypeVariable('t0'), TypeVariable('t1')]
            )
        )
    assert str(exc_info.value) == "Failed to unify different type functions: List, ->"

def test_unify_inf_type_raise_error():
    with pytest.raises(OccursError) as exc_info:
        unify(
            TypeFunctionApplication(
                C = 'List',
                mus = [TypeVariable('t0')]
            ), 
            TypeVariable('t0')
        )
    assert str(exc_info.value) == "Cannot create infinite type"




### SUBSTITUTION

def test_substitution_tyvar():
    mappings = {
            't1' : 't2',
            't1' : 'Int',
            't1' : 'Float',
            't1' : 'List Int',
            't1' : '-> t2 t3',
    }
    
    S = Substitution(mappings)
    for pre, expected in mappings.items():

        res = S(create_monotype(pre)).raw
        assert  res == expected, \
            f"Expected substitution to produce type notation {expected}, got {res}"

def test_substitution_tyfaps():
    x = [
        ({'t1' : 't2'}, '-> t1 t3', '-> t2 t3'),
        ({'t1' : '(List t2)'}, '-> t1 t3', '-> (List t2) t3'),
        ({'t1' : '(-> t2 t3)'}, '-> t1 t3', '-> (-> t2 t3) t3'),
        ({'t1' : 't2', 't3' : 't4'}, '-> t1 t3', '-> t2 t4'),
    ]

    for mapping, pre, expected in x:
        res = Substitution(mapping)(create_monotype(pre))
        assert type(res).__name__ == TypeFunctionApplication.__name__, \
            f"Expected type: TypeFunctionApplication, got {type(res).__name__}"
        assert res.raw == expected, \
            f"Expected substitution to produce type notation {expected}, got {res.raw}"

def test_instantiation():
    quantifier = TypeQuantifier('a', 
                                TypeQuantifier('b', 
                                    create_monotype('-> a b')))

    x = instantiate(quantifier)
    assert x == create_monotype('-> t0 t1')

def test_free_vars():

    complex_type = create_monotype("-> (-> (Int) (-> a (List (-> c (Bool))))) (-> b c)")
    assert set(free_vars(TypeVariable("_0"))) == {"_0"}
    assert set(free_vars(complex_type)) == {"a", "b", "c"}
    assert set(free_vars(Context(
        {
            "x" : complex_type,
            "y" : TypeVariable("d")
        }
        ))) == {"a", "b", "c", "d"}
    assert set(free_vars(TypeQuantifier("d", complex_type))) == {"a", "b", "c"}


