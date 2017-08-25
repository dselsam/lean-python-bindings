#import tensorflow as tf
#import tensorflow_fold as td
#import random

from lang.expr import *
from lang.name import *
from lang.level import *


# Expressions
v1 = lean.mk_var(1)
v2 = lean.mk_var(2)
c_foo = lean.mk_constant(lean.name("foo"))
lvls1 = mk_list_level_cons(lean.mk_level_one(), mk_list_level_cons(lean.mk_level_zero(), mk_list_level_nil()))
lvls1_p = [ lean.mk_level_one(), lean.mk_level_zero() ]
c_bar = lean.mk_constant(lean.name("bar"), lvls1)
#c_bar_p = lean.mk_constant(mk_name("bar"), lvls1_p)
mv1 = lean.mk_metavar(lean.name("abc"), c_foo)
lam = lean.mk_lambda(lean.name("x"), v1, lean.mk_app(c_bar, lean.mk_var(0)))
pi1 = lean.mk_pi(lean.name("x"), v1, lean.mk_app(c_bar, lean.mk_var(0)))
let1 = lean.mk_let(lean.name("x"), c_foo, v1, lean.mk_app(c_bar, lean.mk_var(0)))


print(to_expr_view(v1).to_sexpr())
print(to_expr_view(v2).to_sexpr())
print(to_expr_view(mv1).to_sexpr())
print(to_expr_view(c_foo).to_sexpr())
print(to_expr_view(c_bar).to_sexpr())
print(to_expr_view(lam).to_sexpr())
print(to_expr_view(pi1).to_sexpr())
print(to_expr_view(let1).to_sexpr())
