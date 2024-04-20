

import os
import sys

par_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parser_path = par_dir + "/Simple-Programming-Language-Python/"
sys.path.append(parser_path)

from AST import AstToTypeTree
from spl_parser import spl_parser
from models import AbsExpr, VarExpr


prgm = \
"""
//var x = 1;
// var y = False;

id(x, y: Int) {
    var a = 1;
    var b = a + y;
    x = x;
    return(x);
}

// scope 
// main
"""
def test_parse_to_type_tree():
    tree = spl_parser.parse(prgm)
    trans = AstToTypeTree()
    import lark
    lark.tree.pydot__tree_to_png(tree, "tree.png")
    trans.transform(tree)
    produced_expr = trans.make() 


    expected_expr = AbsExpr(
        x = "x", 
        e = AbsExpr(
            x = "y",
            e = VarExpr(
                x = 'x'
            )))
    
    print(f"ret_stats: {trans._return_stmts}")
    assert produced_expr ==  expected_expr
