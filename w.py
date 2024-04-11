# see: https://doi.org/10.1145/291891.291892
from typing import Tuple
from helpers import generalise, instantiate, unify, Substitution
from models import Context, VarExpr, AbsExpr, AppExpr, Expr, \
    MonoType, TypeVariable, TypeFunctionApplication

def W(ctx: Context, expr: Expr) -> Tuple[Substitution, MonoType]:
    match expr:
        case VarExpr():
            value = ctx.get(expr.x)
            if value is None:
                raise Exception(f"Undefined variable: {expr.x}")
            return (Substitution({}), instantiate(value))

        case AbsExpr():
            beta = TypeVariable()
            ctx[expr.x] = beta
            S1, t1 = W(ctx, expr.e)
            return S1, TypeFunctionApplication("->", [S1(beta), t1])

        case AppExpr():
            S1, t1 = W(ctx, expr.e1)
            S2, t2 = W(S1(ctx), expr.e2)
            beta = TypeVariable()

            S3 = unify(
                S2(t1),
                TypeFunctionApplication("->", [t2, beta])
            )

            return S3(S2(S1)), S3(beta)

        # # W(E, let x = e1 in e2)
        # if expr.type == "let":
        #     s1, t1 = W(typ_env, expr.e1)
        #     typ_env_updated = s1.apply(typ_env)
        #     typ_env_updated[expr.x] = generalise(typ_env, t1)
        #     s2, t2 = W(make_context(typ_env_updated), expr.e2)
        #     return s2.compose(s1), t2

        # raise Exception('Unknown expression type')

    raise Exception(f"Expected a Type Expression got: {type(expr).__name__}")