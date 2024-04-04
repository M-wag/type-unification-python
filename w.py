from helper import generalise, instantiate, make_substitution, new_type_var, Substitution, unify
from models import Context, Expression, make_context, MonoType

def W(typ_env: Context, expr: Expression) -> (Substitution, MonoType):
    # W(E, Var)
    if expr.type == "var":
        # Check the type var of expression
        value = typ_env.get(expr.x)
        # make_context assigns type variables
        if value is None:
            raise Exception(f"Undefined variable: {expr.x}")
        # Instantiate Type (ex: type-quant -> type-var)
        return (make_substitution({}), instantiate(value))

    # W(E, \x.e)
    if expr.type == "abs":
        beta = new_type_var()
        # Extend environment with x: beta
        s1, t1 = W(make_context({**typ_env, expr.x: beta}), expr.e)
        return s1, s1.apply({
            'type': 'ty-app',
            'C': '->',
            'mus': [beta, t1]
        })

    # W(E, e1 e2)
    if expr.type == "app":
        s1, t1 = W(typ_env, expr.e1)
        s2, t2 = W(s1.apply(typ_env), expr.e2)
        beta = new_type_var()

        s3 = unify(s2.apply(t1), {
            'type': 'ty-app',
            'C': '->',
            'mus': [t2, beta]
        })
        return s3.compose(s2.compose(s1)), s3.apply(beta)

    # W(E, let x = e1 in e2)
    if expr.type == "let":
        s1, t1 = W(typ_env, expr.e1)
        typ_env_updated = s1.apply(typ_env)
        typ_env_updated[expr.x] = generalise(typ_env, t1)
        s2, t2 = W(make_context(typ_env_updated), expr.e2)
        return s2.compose(s1), t2

    raise Exception('Unknown expression type')
