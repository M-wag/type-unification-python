from helpers import unify
from models import TypeVariable, TypeFunctionApplication
from errors import UnificationError, OccursError
import pytest


def check_equality(S_produced, S_expect):
    expected = {'t0' : 't1'}
    # print(S_produced)
    assert S_produced == S_expect, f"Expected {S_expect}, got {S_produced}"

# Successful Raw Mappings
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

# TODO : unifying typefunction applications and typevars


# Wrongful Mappings
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
    assert False
    with pytest.raises(OccursError) as exc_info:
        unify(
            TypeFunctionApplication(
                C = 'List',
                mus = [TypeVariable('t0')]
            ), 
            TypeVariable('t0')
        )
    assert str(exc_info.value) == "Failed to unify different type functions: List, ->"


def test_unify_inf_type_raise_error():
    pass

# nested 
#