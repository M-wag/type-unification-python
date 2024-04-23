import os
import sys

par_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parser_path = par_dir + "/Simple-Programming-Language-Python/"
prgm_path = par_dir + "/type-unification-python/demo_prgms"
sys.path.append(parser_path)

from helpers import Substitution
from models import TypeVariable, TypeFunctionApplication, Context, \
    AbsExpr, AppExpr, VarExpr
from w import W
from type_parser import type_parser, TypeParserTransformer
from test_w import test_w_examples
from test_parse import test_to_lambda_vardecl
from spl_parser import spl_parser

import lark

def main():
    with open("demo_prgms/simple_well_typed.spl", "r") as f:
        prgm = f.read()
    
    tree = spl_parser.parse(prgm)


    lark.tree.pydot__tree_to_png(tree, "tree.png")




if __name__ == "__main__":
    main()


