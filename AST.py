
from lark import Transformer
from models import Expr, AppExpr, VarExpr, AbsExpr



class AstToTypeTree(Transformer):
    def __init__(self):
        self._fargs = None
        self._rettype = None
        self._return_stmts = [] 
        self.evaluated_children = []
    
    def start(self, args):
        return args[0]

    def fargs(self, args):
        print(args)
        self._fargs = [arg.value for arg in args[::-1]] 

    def rettype(self, args):
        self._rettype = args

    def return_stmt(self, args):
        self._return_stmts.append(args)
        self.evaluated_children.append(args)
    
    def fundecl(self, args):
        for child in list(reverse(args)):
            if shares_with(self._return_stmtsm, child):
                self.evaluated_children.append(child)

    def make(self):
        body = AppExpr(
            e1 = lambda x : x,
            e2 = VarExpr(
                x= "x"
            )
        )
        print(self._rettype)

        expr = AbsExpr(x=self._fargs[0], e=body)
        if len(self._fargs) > 1:
            for farg in self._fargs[1:]:
                expr = AbsExpr(x=farg, e=expr)
        
        return expr