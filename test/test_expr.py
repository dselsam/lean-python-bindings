from nose.tools import assert_equals, assert_not_equals, assert_false, assert_true

import lean

bi1 = lean.binder_info()
bi2 = lean.mk_implicit_binder_info()

assert_false(bi1.is_implicit())

assert_false(bi2.is_inst_implicit())

assert_true(bi2.is_implicit())

b1 = lean.binder(lean.name("x"), lean.expr(), bi2)
assert_equals(b1.get_name(), lean.name("x"))

v1 = lean.mk_var(1)
v2 = lean.mk_var(2)

c_foo = lean.mk_constant(lean.name("foo"))
c_bar = lean.mk_constant(lean.name("bar"),
                         lean.list_level(lean.mk_level_one(),
                                         lean.list_level(lean.mk_level_zero(), lean.list_level())))

assert_equals(c_foo.const_name(), lean.name("foo"))

assert_equals(str(c_bar.const_levels(), ), "(1 0)")

# Python lists to lean lists

levels = lean.list_level([lean.mk_level_one(), lean.mk_level_zero()])
assert_equals(str(levels), "(1 0)")

names = lean.list_name([lean.name("hello"), lean.name("world")])
assert_equals(str(names), "(hello world)")

expressions = lean.list_expr([lean.mk_constant(lean.name("true")), lean.mk_constant(lean.name("false"))])
assert_equals(str(expressions), "(true false)")

# Lean lists to Python lists

assert_equals(str(lean.list_level(list(levels))), "(1 0)")
assert_equals(str(lean.list_name(list(names))), "(hello world)")
assert_equals(str(lean.list_expr(list(expressions))), "(true false)")

lam = lean.mk_lambda(lean.name("x"), v1, lean.mk_app(c_bar, lean.mk_var(0)))
assert_equals(str(lam), "fun (x : #1), (bar.{1 0} x)")

pi = lean.mk_pi(lean.name("x"), v1, lean.mk_app(c_bar, lean.mk_var(0)))
assert_equals(str(pi), "Pi (x : #1), (bar.{1 0} x)")
