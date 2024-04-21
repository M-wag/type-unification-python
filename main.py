from helpers import Substitution
from models import TypeVariable, TypeFunctionApplication, Context, \
    AbsExpr, AppExpr, VarExpr

from w import W

from type_parser import type_parser, TypeParserTransformer
import lark
from test_w import test_w_examples
from test_helpers import test_free_vars

def main():
    ctx = Context({})

    id = AbsExpr(
        x = "x", 
        e = VarExpr(
            x = 'x'
        )
    )


    S, type_found = W(ctx, id)
    print(type_found)



if __name__ == "__main__":
    test_free_vars()


