from nose.tools import assert_equals, assert_not_equals, assert_false, assert_true
import lean

lk1 = lean.level_kind.Zero
lk2 = lean.level_kind.Succ

assert_not_equals(lk1, lk2)

l0 = lean.mk_level_zero()
l1 = lean.mk_level_one()
l2 = lean.mk_succ(l1)
l3 = lean.mk_param_univ(lean.name("hello"))
l4 = lean.mk_max(l2, l3)

assert_true(l4.is_max())

assert_false(l4.is_imax())

assert_equals(str(l4.max_lhs()), "2")

assert_equals(str(l4.max_rhs()), "hello")

ln1 = lean.list_level()
ln2 = lean.list_level(lean.mk_param_univ(lean.name("head-of-list")), ln1)

assert_equals(str(ln2.head()), "head-of-list")
assert_true(ln2.tail().is_nil())
