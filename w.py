# see: https://doi.org/10.1145/291891.291892
from typing import Tuple
from helpers import generalise, instantiate, unify, Substitution
from models import Context, VarExpr, AbsExpr, Expr, \
    MonoType, TypeVariable, TypeFunctionApplication

def W(env: Context, expr: Expr) -> Tuple[Substitution, MonoType]:
    match expr:
        case VarExpr():
            value = env.get(expr.x)
            if value is None:
                raise Exception(f"Undefined variable: {expr.x}")
            return (Substitution({}), instantiate(value))

        case AbsExpr():
            beta = TypeVariable()
            env[expr.x] = beta
            S1, t1 = W(env, expr.e)
            return S1, TypeFunctionApplication("->", [S1(beta), t1])

        # # W(E, e1 e2)
        # if expr.type == "app":
        #     s1, t1 = W(typ_env, expr.e1)
        #     s2, t2 = W(s1.apply(typ_env), expr.e2)
        #     beta = new_type_var()

        #     s3 = unify(s2.apply(t1), {
        #         'type': 'ty-app',
        #         'C': '->',
        #         'mus': [t2, beta]
        #     })
        #     return s3.compose(s2.compose(s1)), s3.apply(beta)

        # # W(E, let x = e1 in e2)
        # if expr.type == "let":
        #     s1, t1 = W(typ_env, expr.e1)
        #     typ_env_updated = s1.apply(typ_env)
        #     typ_env_updated[expr.x] = generalise(typ_env, t1)
        #     s2, t2 = W(make_context(typ_env_updated), expr.e2)
        #     return s2.compose(s1), t2

        # raise Exception('Unknown expression type')
