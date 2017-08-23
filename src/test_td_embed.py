import tensorflow as tf
import tensorflow_fold as td
import random

import lean

# Expressions
v1 = lean.mk_var(1)
v2 = lean.mk_var(2)
c_foo = lean.mk_constant(lean.name("foo"))
c_bar = lean.mk_constant(lean.name("bar"),
                         lean.list_level(lean.mk_level_one(),
                                         lean.list_level(lean.mk_level_zero(), lean.list_level())))
mv1 = lean.mk_metavar(lean.name("abc"), c_foo)
lam = lean.mk_lambda(lean.name("x"), v1, lean.mk_app(c_bar, lean.mk_var(0)))
pi1 = lean.mk_pi(lean.name("x"), v1, lean.mk_app(c_bar, lean.mk_var(0)))
let1 = lean.mk_let(lean.name("x"), c_foo, v1, lean.mk_app(c_bar, lean.mk_var(0)))


# Destructors
def destruct_var(expr):
    return expr.var_idx()


def destruct_constant(expr):
    return (expr.const_name(), expr.const_levels())


def destruct_lambda(expr):
    return (expr.binding_name(),
            expr.binding_domain(),
            expr.binding_info(),
            expr.binding_binder(),
            expr.binding_body())


def destruct_local(expr):
    return expr.local_info()


def destruct_metavar(expr):
    return (expr.mlocal_name(),
            expr.mlocal_type(),
            expr.mlocal_pp_name())


def destruct_macro(expr):
    return (expr.macro_def(),
            expr.macro_num_args(),
            expr.macro_arg())


def destruct_app(expr):
    return (expr.app_fn(),
            expr.app_arg())


def destruct_pi(expr):
    return (expr.binding_name(),
            expr.binding_domain(),
            expr.binding_info(),
            expr.binding_binder(),
            expr.binding_body())


def destruct_let(expr):
    return (expr.let_name(),
            expr.let_type(),
            expr.let_value(),
            expr.let_body())


def destruct_sort(expr):
    return expr.sort_level()


def switch_expr(expr):
    k = expr.kind()
    if k == lean.Var:
        print "Var"
    elif k == lean.Sort:
        print "Sort"
    elif k == lean.Constant:
        print "Constant"
    elif k == lean.Meta:
        print "Meta"
    elif k == lean.Local:
        print "Local"
    elif k == lean.App:
        print "App"
    elif k == lean.Lambda:
        print "Lambda"
    elif k == lean.Pi:
        print "Pi"
    elif k == lean.Let:
        print "Let"
    elif k == lean.Macro:
        print "Macro"
    else:
        print "Else"


def sexprify(expr):
    if expr.is_var():
        x = destruct_var(expr)
        return "Var(" + str(expr.var_idx()) + ")"
    elif expr.is_constant():
        c, lvl = destruct_constant(expr)
        return "Constant(" + str(c) + ", " + str(lvl) + ")"
    elif expr.is_local():
        li = destruct_local(expr)
        return "Local(" + str(li) + ")"
    elif expr.is_metavar():
        x, t, ppx = destruct_metavar(expr)
        return "Metavar(" + str(x) + ", " + str(t) + ", " + str(ppx) + ")"
    elif expr.is_macro():
        e, nargs, args = destruct_macro(expr)
        return "Macro(" + str(e) + ", " + str(nargs) + ", " + str(args) + ")"
    elif expr.is_app():
        e1, e2 = destruct_app(expr)
        return "App(" + sexprify(e1) + ", " + sexprify(e2) + ")"
    elif expr.is_lambda():
        x, bd, bi, b, e = destruct_lambda(expr)
        return "Lambda(" + str(b) + ", " + str(bd) + ", " + str(bi) + ", " + str(x) + ", " + sexprify(e) + ")"
    elif expr.is_pi():
        x, bd, bi, b, e = destruct_pi(expr)
        return "Pi(" + str(b) + ", " + str(bd) + ", " + str(bi) + ", " + str(x) + ", " + sexprify(e) + ")"
    elif expr.is_let():
        x, t, v, e = destruct_let(expr)
        return "Let(" + str(x) + ", " + str(t) + ", " + str(v) + ", " + sexprify(e) + ")"
    elif expr.is_sort():
        lvl = destruct_sort(expr)
        return "Sort(" + str(lvl) + ")"
    else:
        return "otherwise" + str(expr)


switch_expr(v1)
print(sexprify(v1))

switch_expr(v2)
print(sexprify(v2))

print(sexprify(mv1))
print(sexprify(c_foo))
print(sexprify(c_bar))

switch_expr(lam)
print(sexprify(lam))

switch_expr(pi1)
print(sexprify(pi1))

switch_expr(let1)
print(sexprify(let1))


# Embed




# Destructors

