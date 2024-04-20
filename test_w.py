from w import W 
from models import TypeQuantifier
from models import AbsExpr, VarExpr, Context, AppExpr
from helpers import create_monotype


def test_var_expr_monotypes_equality():
    pass

    # Passing in monotypes should always return the same monotype 
    # Should return empty Substituion

def test_var_expr_instantiates():
    pass
    # infered_type, Substitution = W(env, expr)

    # Pass a TypeQuantifier, with a contexto
    # Should return instantiate to MonoType
    # Should return empty Substituion

def test_w_examples():
    # isneg : Int -> Bool
    # \x.isneg x : t1 -> t2
    # outcome: t1 -> t2 ~ Int -> Bool

    ctx = Context({'isneg' : create_monotype('-> (Int) (Bool)')})
    expr = AbsExpr(
            x='x',
            e = AppExpr(
                e1 = VarExpr("isneg"), 
                e2 = VarExpr("x"),
            ))
                    
    S, type_found = W(ctx, expr)


    print(f"expected {create_monotype("-> (Int) (Bool)")}")
    print(f"got      {type_found.raw}")
    assert type_found == create_monotype("-> (Int) (Bool)")



    

# Known variable
# Polymorphic variable
# Variable shadowing
# Known constraints
# Empty context raise error 
