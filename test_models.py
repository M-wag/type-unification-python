from models import TypeVariable, TypeFunctionApplication

def test_monotypes_dump_init_dump_equality():
    x = TypeVariable('t1')
    assert TypeVariable(x.dump()).dump() == x.dump(), \
            "Initiazing TypeVariable from dumped content did not produce identical object"
    y = TypeFunctionApplication("-> t1 t2")
    assert TypeFunctionApplication(y.dump()).dump() == y.dump(), \
            "Initiazing TypeFunctionApplication from dumped content did not produce identical object"
             
# TODO 
def test_monotype_dump_errors():
    # Wrong type passed
    # n_mu != 2 | C = ->
    # n_mu != 1 | C = List
    # 
    pass


