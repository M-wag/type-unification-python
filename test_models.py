from models import TypeVariable, TypeFunctionApplication
from helpers import create_monotype
import pytest

def test_monotypes_dump_init_dump_equality():
    x = TypeVariable('t1')
    assert TypeVariable(x.raw).raw == x.raw, \
            "Initiazing TypeVariable from dumped content did not produce identical object"
    y = TypeFunctionApplication("-> t1 t2")
    assert TypeFunctionApplication(y.raw).raw == y.raw, \
            "Initiazing TypeFunctionApplication from dumped content did not produce identical object"

def test_monotypes_C_and_mus_to_raw():
    assert TypeFunctionApplication.get_raw(TypeVariable('a')) == 'a', \
            ".get_raw() did not return the return right raw for TypeVariable"

    x = TypeFunctionApplication(
        C = "->", 
        mus = [
            TypeVariable("a"),
            TypeVariable("b")
        ]
    ) 
    assert x.raw == "(-> a b)"

    x = TypeFunctionApplication(
        C = "->", 
        mus = [
            TypeFunctionApplication(
                "->", 
                [TypeVariable("a"), TypeVariable("b")]),
            TypeVariable("c")]
    )
    assert x.raw == "(-> (-> a b) c)"

    x = TypeFunctionApplication(
            C = "List",
            mus = [TypeFunctionApplication('->', [TypeVariable('a'), TypeVariable('b')])]
    )
    assert x.raw == "(List (-> a b))"

             
# TODO 
def test_monotype_dump_errors():
    # Wrong type passed
    # n_mu != 2 | C = ->
    # n_mu != 1 | C = List
    # 
    pass

@pytest.mark.filterwarnings("ignore::DeprecationWarning:lark.utils")
def test_monotypes_raw_to_C_and_mus():
    from type_parser import type_parser, TypeParserTransformer

    parsed_tv = TypeParserTransformer().transform(
            type_parser.parse("-> (-> a b) (List (Int ))")
        )

    manual_tv = TypeFunctionApplication(
            C = '->',
            mus = [
                    TypeFunctionApplication(
                        C = '->',
                        mus = [TypeVariable('a'), TypeVariable('b')]),
                    TypeFunctionApplication(
                        C = 'List',
                        mus = [TypeFunctionApplication('Int', mus=[])]),
                ]
            )

    assert parsed_tv.raw == manual_tv.raw, \
        f"{manual_tv.raw}\n Building from type_note should share type_note manually constructed TypeVariable"
    assert parsed_tv == manual_tv, \
        f"{manual_tv.raw}\n Building from type_note should equal manually constructed TypeVariable"

            

    # Generate tyfap from str 
    # Compare if they work

def test_monotype_equality():
    tv_a = TypeVariable('a')
    tv_b = TypeVariable('b')

    assert (tv_a == tv_a) == True
    assert (tv_a == tv_b) == False

    assert (TypeFunctionApplication('->', [tv_a, tv_b]) == TypeFunctionApplication('->', [tv_a, tv_b])) == True
    assert (TypeFunctionApplication('->', [tv_b, tv_a]) == TypeFunctionApplication('->', [tv_a, tv_b])) == False
    assert (TypeFunctionApplication('List', [tv_b, tv_a]) == TypeFunctionApplication('->', [tv_a, tv_b])) == False

    assert (TypeFunctionApplication('Int', []) == TypeFunctionApplication('Int', [])) == True
    assert (TypeFunctionApplication('Bool', []) == TypeFunctionApplication('Int', [])) == False

    complex_tv_1 = TypeFunctionApplication(
            C = '->',
            mus = [
                    TypeFunctionApplication(
                        C = '->',
                        mus = [TypeVariable('a'), TypeVariable('b')]),
                    TypeFunctionApplication(
                        C = 'List',
                        mus = [TypeFunctionApplication('Int', mus=[])]),
                ]
            )

    complex_tv_2 = TypeFunctionApplication(
            C = '->',
            mus = [
                    TypeFunctionApplication(
                        C = '->',
                        mus = [TypeVariable('a'), TypeVariable('b')]),
                    TypeFunctionApplication(
                        C = 'List',
                        mus = [TypeFunctionApplication('Int', mus=[])]),
                ]
            )

    assert (complex_tv_1 == complex_tv_2) == True

