import os
import sys

par_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parser_path = par_dir + "/Simple-Programming-Language-Python/"
prgm_path = par_dir + "/type-unification-python/demo_prgms"
sys.path.append(parser_path)

import lark
from lark import Tree
from lark.lexer import Token
from AST import ParseTreeToLambda, split_parse_tree, DAGMaker, LetBinder
from spl_parser import spl_parser
from models import AbsExpr, AppExpr, VarExpr, LetExpr, Context, \
        TypeVariable
from w import W
from helpers import create_monotype
import pytest

def init_builders(path: str, fname="tree", visualize=False):
    lambda_converter = ParseTreeToLambda()
    let_binder = LetBinder()

    with open(prgm_path + path, "r") as f:
        prgm = f.read()
    tree = spl_parser.parse(prgm)

    if visualize:
        from lark.tree import pydot__tree_to_png
        pydot__tree_to_png(tree, f"visual/{fname}.png")

    return tree, lambda_converter, let_binder

def get_fargs(tree):
    fargs_branch = list(filter(lambda t: t.data == "fargs", tree.iter_subtrees_topdown()))[0]
    return Tree('start',[fargs_branch])

def test_dag_seperate_main():
    with open(prgm_path + "/simple_well_typed.spl", "r") as f:
        prgm = f.read()

    tree = spl_parser.parse(prgm)
    dag_maker = DAGMaker()
    main_branch = split_parse_tree(tree)
    lark.tree.pydot__tree_to_png(main_branch, 'tree.png')

    dag_fwd, dag_bwd, dag = dag_maker(main_branch)
    print(dag_maker.dag_bwd)
    print(dag_maker.dag_fwd)
    lark.tree.pydot__tree_to_png(dag, 'dag.png')

    assert dag_fwd == {'y' : ['x'], 'z' : ['x', 'y']}
    assert dag_bwd == {'x' : ['y', 'z'] , 'y' : ['z']}

    
def test_let_expr_e2_binding():
    '''
    tree = parse(prgm)
    unbound_type_tree = convert_to_lamba(tree)
    bound_type_tree = bind_let_expressions(unbound_type_tree)
    type, sub = W(bound_type_tree)
    '''

    lambda_converter = ParseTreeToLambda()
    let_binder = LetBinder()

    with open(prgm_path + "/simple_well_typed.spl", "r") as f:
        prgm = f.read()
        tree = spl_parser.parse(prgm)

    unbound_type_tree, ctx = lambda_converter.transform(tree)
    bound_type_tree = let_binder.trasnform(unbound_type_tree)
    inferred_type, Substitution = W(bound_type_tree, Context({}))

    assert inferred_type == create_monotype("(Int )")



def test_lambda_converter_outputs_correct_branches():
    tree, lambda_converter, let_binder = init_builders("/simple_well_typed.spl", visualize=True)


    unbound_type_tree, ctx = lambda_converter.transform(tree)

    print(unbound_type_tree)
    assert unbound_type_tree == [
            AbsExpr(
                x = "_0", 
                e = VarExpr("_0")),
            AbsExpr(None, None)
            ]

def test_lambda_converter_init_appexpr():
    tree, lambda_converter, _ = init_builders("/t_init_appexpr.spl", fname="longarg", visualize=True)
    fargs = get_fargs(tree)
    folded_fargs = lambda_converter.transform(fargs)

    print(tree.pretty())
    print(fargs.pretty())
    print(folded_fargs)
    # lark.tree.pydot__tree_to_png(fargs, 'visual/long_arg.png')
    # lark.tree.pydot__tree_to_png(folded_fargs, 'visual/folded_long_arg.png')

    assert folded_fargs == Tree('fargs', [  
              Tree('arg', [Token('ID', 'x'), 'a']),
              Tree('arg', [Token('ID', 'y'), 'Int']),
              Tree('arg', [Token('ID', 'z'), 'undefined']),
              ])



@pytest.mark.skip(reason="Fix VarDecl first")
def test_AST_parse_to_type_tree():
    tree = spl_parser.parse(prgm)
    ast_to_type = ParseTreeToLambda()

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

