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
             
# TODO 
def test_monotype_dump_errors():
    # Wrong type passed
    # n_mu != 2 | C = ->
    # n_mu != 1 | C = List
    # 
    pass

@pytest.mark.filterwarnings("ignore::DeprecationWarning:lark.utils")
def test_type_parser():
    # TODO: deprecation warning
    from type_parser import type_parser, TypeParserTransformer

    x = type_parser.parse("-> (-> a c) b")
    out = TypeParserTransformer().transform(x)


    print(out.C)
    print(out.mus)

