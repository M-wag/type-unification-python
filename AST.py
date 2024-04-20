
from lark import Transformer
from models import Expr, AppExpr, VarExpr, AbsExpr, LetExpr, \
    Context, TypeVariable
from helpers import create_monotype

# idea 1:
# map everything without dataflow analysis

# idea 2: use dataflow analys

class AstToTypeTree(Transformer):
    def __init__(self):
        self._fargs = None
        self._rettype = None
        self._vardecl = [] 
        self._return_stmt = [] 

        self.ctx = Context({})
        self.tv_count = 0
    
    def start(self, args):
        return args[0]

    def fargs(self, args):
        self._fargs = [arg.value for arg in args[::-1]] 

    def rettype(self, args):
        self._rettype = args

    def return_stmt(self, args):
        self._return_stmt = args

    def decl(self, args):
        return args[0]
    
    def vardecl(self, args):
        varname, expr = (args[0].value, args[0:])
        tv_name = f"_{self.tv_count}"
        self.tv_count += 1
        self.ctx[tv_name] = TypeVariable(tv_name)
        return LetExpr(
            x = varname,
            e1 = VarExpr(tv_name),
            e2 = None
        )


    def fundecl(self, args):
        self._fargs = [arg.value for arg in args[::-1]]
