
from lark import Transformer, Visitor
from lark.lexer import Token
from lark.tree import Tree
from models import Expr, AppExpr, VarExpr, AbsExpr, LetExpr, \
    Context, TypeVariable
from helpers import create_monotype
from typing import Any, List, Dict, Tuple
from errors import *

class ParseTreeToLambda(Transformer):
    def __init__(self, visit_tokens: bool = True) -> None:
        super().__init__(visit_tokens)

        self._fargs = None
        self._rettype = None
        self._vardecl = [] 
        self._return_stmt = [] 

        self.ctx = Context({})
        self.tv_count = 0

    def start(self, args):
        return args[0]

    def fargs(self, args):
        arg_type = []
        arg_ID = []
        fargs = []
        # find type and find ID 
        for arg in args: 
            match arg:
                case Tree(data="fargs"): # node: fargs
                    fargs.append(arg)
                case Token(type="ID"): # node: ID 
                    arg_ID.append(arg)
                case _: # node: type TODO: find better way to represent this
                    arg_type.append(arg)

            print(arg)
            print(f"\ttype : {len(arg_type)}")
            print(f"\tID: {len(arg_ID)}")
            print(f"\tfargs: {len(fargs)}")
            
            if max(len(fargs), len(arg_ID), len(arg_type)) > 1:
                raise AstConstructionError(f"Cannot have more then one '{type(arg).__name__}' node for a fargs")

        if len(arg_ID) == 0:
            raise AstConstructionError(f"Attempting to make arg node without arg_ID")

        if len(arg_type) == 0:
            arg_type.append(Tree('type'), 'Any')
            
        arg = Tree('arg', [arg_ID[0], arg_type[0]])

        print()
        if len(fargs) == 1:
            return Tree('fargs', [fargs.children[0], arg])
        else: 
            return Tree('fargs', [arg])




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
            e2 = VarExpr(tv_name)
        )

    def fundecl(self, args):
        # fargs -> app binding
        # rettype -> ??context??
        # vardecl -> let bindings
        # statement -> app expr 
        # return statement -> context
        pass



def is_ID(node): 
    if isinstance(node, Token):
        if node.type == "ID":
            return True
    return False

def _flatten_list(nested):
    flat = []
    for item in nested:
        if isinstance(item, list):
            flat.extend(_flatten_list(item))
        else:
            flat.append(item)
    return flat
    
def split_parse_tree(tree: Tree) -> List[Tree]:
    def is_main_function(node):
        if node.data == "fundecl" and isinstance(node.children[0], Token) and node.children[0] == "main":
            return True
        return False

    main_branch = tree.find_pred(is_main_function)
    return list(main_branch)[0]

class DAGMaker(Transformer): 
    def __init__(self, visit_tokens: bool = True) -> None:
        super().__init__(visit_tokens)

        self.dag_fwd = {}
        self.dag_bwd = {}

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        tree = super().transform(*args, **kwds)
        return self.dag_fwd, self.dag_bwd, tree

    def actargs(self, args):
        return [child for child in args if is_ID(child)]

    def funcall(self, args):
        actargs = args[1]
        return actargs
    
    def exp(self, args):
        return [child for child in _flatten_list(args) if is_ID(child)]

    def vardecl(self, args):

        # graph construction
        dep_var = args[0].value
        # ind_vars = [child for child in _flatten_list(args[1:]) if is_ID(child)]
        ind_vars = [child for child in _flatten_list(args[1:])]

        # if self.dag_bwd.get(dep_var) == None:
        #     self.dag_bwd[dep_var] = ind_vars
        # else:
        #     self.dag_bwd[dep_var] += ind_vars

        # for var in _flatten(ind_vars):
        #     if self.dag_fwd.get(dep_var) == None:
        #         self.dag_fwd[var] = [dep_var]
        #     else: 
        #         self.dag_fwd[var] += dep_var
            
        # visualization 

        return Tree(dep_var, ind_vars)


class LetBinder():
    pass