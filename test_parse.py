import os
import sys

par_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parser_path = par_dir + "/Simple-Programming-Language-Python/"
prgm_path = par_dir + "/type-unification-python/demo_prgms"
sys.path.append(parser_path)

import lark
from AST import AstToTypeTree, split_parse_tree
from spl_parser import spl_parser
from models import AbsExpr, VarExpr, LetExpr, Context, \
        TypeVariable
from w import W
from helpers import create_monotype
    
import pytest


prgm_with_df = \
"""
id(x, y: Int) {
    var a = 1;
    var b = a + y;
    x = x;
    return(x);
}

"""

prgm = \
"""
id(x) {
    return(x);
}
"""

def test_AST_seperate_main():
    with open(prgm_path + "/simple_well_typed.spl", "r") as f:
        prgm = f.read()

    tree = spl_parser.parse(prgm)
    main_branch, tree = split_parse_tree(tree)
    lark.tree.pydot__tree_to_png(main_branch, "tree.png")
    for child in main_branch.children[1:]:
        print(child)

    assert False

@pytest.mark.skip(reason="Fix VarDecl first")
def test_to_lambda_vardecl():
    with open(prgm_path + "/vardecl.spl", "r") as f:
        prgm = f.read()

    tree = spl_parser.parse(prgm)
    ast_to_type = AstToTypeTree()
    prod_expr = ast_to_type.transform(tree)
    prod_ctx = ast_to_type.ctx

    # import lark
    # lark.tree.pydot__tree_to_png(tree, "tree.png")

    expt_expr = LetExpr(
            x = 'a',
            e1 = VarExpr("_0"),
            e2 = VarExpr("_0")
        )
    expt_ctx = Context({"_0" : TypeVariable("_0")})

    assert expt_expr == prod_expr, \
            f"Expected {expt_expr}, got {prod_expr}"
    assert expt_ctx == prod_ctx, \
            f"Expected {expt_ctx}, got {prod_ctx}"

    Sub, prod_type_found = W(prod_ctx, prod_expr)
    
    expt_type_found = create_monotype("Int")

    assert expt_type_found == prod_type_found, \
            f"Expected {expt_type_found}, got {prod_type_found}"


@pytest.mark.skip(reason="Fix VarDecl first")
def test_AST_parse_to_type_tree():
    tree = spl_parser.parse(prgm)
    ast_to_type = AstToTypeTree()

    ast_to_type.transform(tree)
    produced_expr = trans.make() 

    expected_expr = AbsExpr(
        x = "x", 
        e = AbsExpr(
            x = "y",
            e = VarExpr(
                x = 'x'
            )))
    
    assert produced_expr ==  expected_expr

