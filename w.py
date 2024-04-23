# see: https://doi.org/10.1145/291891.291892
from typing import Tuple
from helpers import generalise, instantiate, unify, Substitution
from models import Context, VarExpr, AbsExpr, AppExpr, LetExpr,  Expr, \
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

        case LetExpr():
            S1, t1 = W(ctx, expr.e1)
            ctx = S1(ctx)
            ctx[expr.x] = generalise(ctx, t1)
            S2, t2 = W(ctx, expr.e2)
            return S2(S1), t2

    raise Exception(f"Expected a Type Expression got: {type(expr).__name__}")